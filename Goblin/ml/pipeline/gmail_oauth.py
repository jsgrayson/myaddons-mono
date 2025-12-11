import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from loguru import logger

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GmailOAuth2:
    """Handle Gmail OAuth2 authentication and email sending."""
    
    def __init__(self, credentials_path: str = None, token_path: str = None):
        self.credentials_path = credentials_path or os.path.join(
            os.path.dirname(__file__), 
            "../../backend/config/gmail_credentials.json"
        )
        self.token_path = token_path or os.path.join(
            os.path.dirname(__file__),
            "../../backend/config/gmail_token.pickle"
        )
        self.service = None
        
    def authenticate(self) -> bool:
        """Authenticate with Gmail API using OAuth2."""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, request user authorization
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing Gmail OAuth2 token...")
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    logger.error(f"Gmail credentials not found at {self.credentials_path}")
                    logger.error("Download credentials.json from Google Cloud Console")
                    return False
                    
                logger.info("Starting Gmail OAuth2 authorization flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
                logger.info("Gmail OAuth2 token saved.")
        
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail API authenticated successfully.")
            return True
        except Exception as e:
            logger.error(f"Gmail authentication error: {e}")
            return False
    
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send an email via Gmail API."""
        if not self.service:
            if not self.authenticate():
                return False
        
        try:
            message = MIMEText(body)
            message['to'] = to_email
            message['subject'] = subject
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            send_message = {'raw': raw_message}
            
            self.service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
