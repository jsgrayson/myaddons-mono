import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from loguru import logger
from typing import List, Dict, Any

class NotificationService:
    def __init__(self, discord_webhook: str = None, email_config: dict = None):
        self.discord_webhook = discord_webhook or os.getenv("DISCORD_WEBHOOK_URL")
        self.email_config = email_config or {}
        
    def send_discord(self, message: str, title: str = "Goblin Alert") -> bool:
        """Send a message to Discord via webhook."""
        if not self.discord_webhook:
            logger.warning("Discord webhook not configured. Skipping Discord notification.")
            return False
            
        try:
            payload = {
                "embeds": [{
                    "title": title,
                    "description": message,
                    "color": 3066993,  # Green
                    "footer": {"text": "Goblin AI Gold Making System"}
                }]
            }
            response = requests.post(self.discord_webhook, json=payload, timeout=5)
            if response.status_code == 204:
                logger.info("Discord notification sent successfully.")
                return True
            else:
                logger.error(f"Discord webhook failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Discord notification error: {e}")
            return False
    
    def send_email(self, subject: str, body: str, to_email: str = None) -> bool:
        """Send an email notification using OAuth2 or SMTP."""
        # Try OAuth2 first
        try:
            from .gmail_oauth import GmailOAuth2
            gmail = GmailOAuth2()
            if gmail.authenticate():
                to_email = to_email or self.email_config.get("to_email", "")
                if to_email:
                    return gmail.send_email(to_email, subject, body)
        except Exception as e:
            logger.warning(f"OAuth2 failed, falling back to SMTP: {e}")
        
        # Fallback to SMTP
        if not self.email_config:
            logger.warning("Email not configured. Skipping email notification.")
            return False
            
        try:
            smtp_server = self.email_config.get("smtp_server")
            smtp_port = self.email_config.get("smtp_port", 587)
            username = self.email_config.get("username")
            password = self.email_config.get("password")
            from_email = self.email_config.get("from_email", username)
            to_email = to_email or self.email_config.get("to_email")
            
            if not all([smtp_server, username, password, to_email]):
                logger.warning("Incomplete email configuration. Skipping.")
                return False
            
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
                
            logger.info(f"Email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Email notification error: {e}")
            return False
    
    def send_opportunity_alert(self, opportunities: List[Dict[str, Any]], total_count: int):
        """Send alerts about found opportunities."""
        if not opportunities:
            logger.info("No opportunities to report.")
            return
            
        # Prepare Discord message
        top_5 = opportunities[:5]
        discord_msg = f"🎯 **Found {total_count} Flip Opportunities!**\n\n"
        discord_msg += "**Top 5 Deals:**\n"
        for i, opp in enumerate(top_5, 1):
            item_id = opp.get('item_id')
            current_price = opp.get('price', 0) / 10000  # Copper to gold
            predicted_price = opp.get('predicted_price', 0) / 10000
            discount = opp.get('discount_pct', 0)
            discord_msg += f"{i}. Item #{item_id}: {current_price:.0f}g → {predicted_price:.0f}g ({discount:.1f}% profit)\n"
        
        discord_msg += f"\nMore details in `opportunities.json`"
        
        # Prepare email message
        email_body = f"Goblin AI found {total_count} profitable flip opportunities!\n\n"
        email_body += "Top 5 Opportunities:\n"
        email_body += "="*50 + "\n"
        for i, opp in enumerate(top_5, 1):
            item_id = opp.get('item_id')
            current_price = opp.get('price', 0) / 10000
            predicted_price = opp.get('predicted_price', 0) / 10000
            discount = opp.get('discount_pct', 0)
            email_body += f"{i}. Item ID: {item_id}\n"
            email_body += f"   Current Price: {current_price:.0f} gold\n"
            email_body += f"   Predicted Value: {predicted_price:.0f} gold\n"
            email_body += f"   Potential Profit: {discount:.1f}%\n\n"
        
        # Send notifications
        self.send_discord(discord_msg, f"💰 {total_count} Flip Opportunities")
        self.send_email(
            subject=f"Goblin Alert: {total_count} Flip Opportunities Found",
            body=email_body
        )
