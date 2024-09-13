"""
email_sender.py

This module handles sending forecast results via email using the SendGrid API.

Functions:
- send_email(subject, content): Sends an email with the provided subject and content.
- generate_html_content(subject, content): Generates HTML content for the email.
- validate_email_parameters(subject, content): Validates the subject and content before sending.
  
Dependencies:
- sendgrid: SendGrid API for sending emails.
- jinja2: For templating HTML content for the email.
"""

import sendgrid
from sendgrid.helpers.mail import Mail
from src.config import SENDGRID_API_KEY, SENDGRID_FROM_EMAIL, SENDGRID_TO_EMAIL
import logging
from jinja2 import Template
import requests

logger = logging.getLogger(__name__)

def generate_html_content(subject, content):
    html_template = '''
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 800px;
                margin: auto;
                padding: 20px;
                background-color: #f9f9f9;
                border: 1px solid #ddd;
            }
            h2 {
                color: #333;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            table, th, td {
                border: 1px solid #ddd;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            p {
                margin: 0;
                padding: 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>{{ subject }}</h2>
            {{ content|safe }}
        </div>
    </body>
    </html>
    '''
    template = Template(html_template)
    return template.render(subject=subject, content=content)

def validate_email_parameters(subject, content):
    if not subject or not content:
        raise ValueError("Subject and content cannot be empty.")

def send_email(subject, content):
    try:
        validate_email_parameters(subject, content)
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        
        # Construct HTML content
        html_content = generate_html_content(subject, content)
        
        email = Mail(
            from_email=SENDGRID_FROM_EMAIL,
            to_emails=SENDGRID_TO_EMAIL,
            subject=subject,
            html_content=html_content
        )
        response = sg.send(email)
        return response
    except requests.exceptions.RequestException as req_ex:
        logger.error("Request error: %s", req_ex)
    except ValueError as val_ex:
        logger.error("Value error: %s", val_ex)
    except Exception as e:
        logger.error("Unexpected error sending email: %s", e)
    return None
