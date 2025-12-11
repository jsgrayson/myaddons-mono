#!/usr/bin/env python3
"""
One-time script to authorize Gmail API access.
Run this once to generate the refresh token.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ml.pipeline.gmail_oauth import GmailOAuth2
from loguru import logger

def main():
    logger.info("Starting Gmail OAuth2 authorization...")
    logger.info("This will open your browser to sign in to Google.")
    logger.info("")
    
    gmail = GmailOAuth2()
    
    if gmail.authenticate():
        logger.success("✅ Authorization successful!")
        logger.info("Token saved to: backend/config/gmail_token.pickle")
        logger.info("")
        logger.info("You can now send emails via Gmail API.")
        logger.info("This token will auto-refresh, no need to re-authorize.")
    else:
        logger.error("❌ Authorization failed.")
        logger.error("Make sure gmail_credentials.json exists in backend/config/")
        sys.exit(1)

if __name__ == "__main__":
    main()
