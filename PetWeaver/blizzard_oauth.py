#!/usr/bin/env python3
"""
Blizzard OAuth 2.0 Authentication Handler
Implements Authorization Code Flow for WoW Profile API access
"""

import json
import os
import secrets
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode, parse_qs, urlparse
import requests
from datetime import datetime, timedelta


class BlizzardOAuth:
    """Handles Blizzard OAuth 2.0 flow"""
    
    # OAuth endpoints
    AUTH_URL = "https://oauth.battle.net/authorize"
    TOKEN_URL = "https://oauth.battle.net/token"
    
    # Configuration
    REDIRECT_URI = "http://localhost:8080/callback"
    SCOPE = "wow.profile"
    TOKEN_FILE = "token.json"
    
    def __init__(self, client_id, client_secret, region="us"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region
        self.state = secrets.token_urlsafe(16)
        self.authorization_code = None
        self.token_data = None
        
    def load_token(self):
        """Load token from file if it exists and is valid"""
        if not os.path.exists(self.TOKEN_FILE):
            return False
            
        try:
            with open(self.TOKEN_FILE, 'r') as f:
                self.token_data = json.load(f)
                
            # Check if token is expired
            expires_at = datetime.fromisoformat(self.token_data.get('expires_at', '2000-01-01'))
            if datetime.now() >= expires_at:
                print("⚠️  Token expired, need to re-authenticate")
                return False
                
            print("✅ Loaded existing valid token")
            return True
            
        except Exception as e:
            print(f"⚠️  Error loading token: {e}")
            return False
    
    def save_token(self):
        """Save token to file"""
        if not self.token_data:
            return
            
        # Calculate expiration time
        expires_in = self.token_data.get('expires_in', 3600)
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        self.token_data['expires_at'] = expires_at.isoformat()
        
        with open(self.TOKEN_FILE, 'w') as f:
            json.dump(self.token_data, f, indent=2)
            
        print(f"✅ Token saved to {self.TOKEN_FILE}")
    
    def get_authorization_url(self):
        """Generate the OAuth authorization URL"""
        params = {
            'client_id': self.client_id,
            'scope': self.SCOPE,
            'state': self.state,
            'redirect_uri': self.REDIRECT_URI,
            'response_type': 'code'
        }
        return f"{self.AUTH_URL}?{urlencode(params)}"
    
    def start_callback_server(self):
        """Start local HTTP server to receive OAuth callback"""
        oauth = self
        
        class CallbackHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass  # Suppress server logs
                
            def do_GET(self):
                # Parse query parameters
                query = parse_qs(urlparse(self.path).query)
                
                if 'code' in query and 'state' in query:
                    # Verify state to prevent CSRF
                    if query['state'][0] != oauth.state:
                        self.send_error(400, "Invalid state parameter")
                        return
                    
                    oauth.authorization_code = query['code'][0]
                    
                    # Send success response
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write("""
    <html>
    <body style=\"font-family: Arial; text-align: center; padding: 50px;\">
        <h1 style=\"color: green;\">✅ Authorization Successful!</h1>
        <p>You can close this window and return to the terminal.</p>
    </body>
    </html>
""".encode())
                else:
                    self.send_error(400, "Missing code or state parameter")
        
        server = HTTPServer(('localhost', 8080), CallbackHandler)
        print("🌐 Starting callback server on http://localhost:8080")
        print("⏳ Waiting for OAuth callback...")
        
        # Handle one request then shutdown
        server.handle_request()
        return self.authorization_code
    
    def exchange_code_for_token(self, code):
        """Exchange authorization code for access token"""
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.REDIRECT_URI,
            'scope': self.SCOPE
        }
        
        response = requests.post(
            self.TOKEN_URL,
            data=data,
            auth=(self.client_id, self.client_secret)
        )
        
        if response.status_code != 200:
            raise Exception(f"Token exchange failed: {response.text}")
        
        self.token_data = response.json()
        return self.token_data
    
    def authenticate(self):
        """Complete OAuth flow"""
        # Try to load existing token
        if self.load_token():
            return self.token_data['access_token']
        
        # Generate authorization URL
        auth_url = self.get_authorization_url()
        
        print("\n" + "="*60)
        print("🔐 BLIZZARD OAUTH AUTHENTICATION")
        print("="*60)
        print("\nOpening browser for Battle.net login...")
        print(f"If browser doesn't open, visit:\n{auth_url}\n")
        
        # Open browser
        webbrowser.open(auth_url)
        
        # Start callback server
        code = self.start_callback_server()
        
        if not code:
            raise Exception("Failed to receive authorization code")
        
        print("✅ Authorization code received")
        print("🔄 Exchanging code for access token...")
        
        # Exchange code for token
        token_data = self.exchange_code_for_token(code)
        
        print(f"✅ Access token obtained (expires in {token_data.get('expires_in', 0)}s)")
        
        # Save token
        self.save_token()
        
        return token_data['access_token']
    
    def get_access_token(self):
        """Get valid access token (from file or new auth)"""
        if self.load_token():
            return self.token_data['access_token']
        return self.authenticate()


def main():
    """Example usage"""
    print("\n" + "="*60)
    print("🎮 BLIZZARD API - OAUTH SETUP")
    print("="*60)
    
    # Check for credentials
    client_id = os.getenv('BLIZZARD_CLIENT_ID')
    client_secret = os.getenv('BLIZZARD_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("\n⚠️  Missing API credentials!")
        print("\nYou need to create a Blizzard API client:")
        print("1. Visit: https://develop.battle.net/access/clients")
        print("2. Create a new client")
        print("3. Set redirect URL to: http://localhost:8080/callback")
        print("4. Save your Client ID and Client Secret")
        print("\nThen run:")
        print("  export BLIZZARD_CLIENT_ID='your_client_id'")
        print("  export BLIZZARD_CLIENT_SECRET='your_client_secret'")
        
        # Prompt for manual entry
        print("\nOr enter them now:")
        client_id = input("Client ID: ").strip()
        client_secret = input("Client Secret: ").strip()
        
        if not client_id or not client_secret:
            print("❌ Invalid credentials provided")
            return
    
    # Create OAuth handler
    oauth = BlizzardOAuth(client_id, client_secret, region="us")
    
    # Authenticate
    try:
        access_token = oauth.authenticate()
        print("\n" + "="*60)
        print("✅ AUTHENTICATION SUCCESSFUL!")
        print("="*60)
        print(f"\nAccess Token (first 20 chars): {access_token[:20]}...")
        print(f"\nToken saved to: {BlizzardOAuth.TOKEN_FILE}")
        print("\nYou can now use this token to fetch your WoW data!")
        
    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")


if __name__ == "__main__":
    main()
