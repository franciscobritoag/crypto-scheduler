"""
config.py

This module loads environment variables for the application, particularly for
sending emails using SendGrid.

Environment variables:
- SENDGRID_API_KEY: The API key for SendGrid.
- SENDGRID_FROM_EMAIL: The sender's email address for sending forecasts.
- SENDGRID_TO_EMAIL: The recipient's email address for receiving forecasts.

Usage:
- Make sure to set up a .env file with the necessary keys or configure them in your system environment.
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path='sendgrid.env')

# Now you can access environment variables
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDGRID_FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL')
SENDGRID_TO_EMAIL = os.getenv('SENDGRID_TO_EMAIL')
