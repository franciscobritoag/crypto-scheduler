import sendgrid
from sendgrid.helpers.mail import Mail
from src.config import SENDGRID_API_KEY, SENDGRID_FROM_EMAIL, SENDGRID_TO_EMAIL
import logging
from jinja2 import Template
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests

logger = logging.getLogger(__name__)

def validate_environment_variables():
    if not SENDGRID_API_KEY:
        raise EnvironmentError("SendGrid API Key is not set.")
    if not SENDGRID_FROM_EMAIL:
        raise EnvironmentError("Sender email (SENDGRID_FROM_EMAIL) is not set.")
    if not SENDGRID_TO_EMAIL:
        raise EnvironmentError("Recipient email (SENDGRID_TO_EMAIL) is not set.")

html_template = Template('''
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
''')

def generate_html_content(subject, content):
    return html_template.render(subject=subject, content=content)

def validate_email_parameters(subject, content):
    if not subject or not content:
        raise ValueError("Subject and content cannot be empty.")

@retry(
    stop=stop_after_attempt(3),  
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(requests.exceptions.RequestException),
    reraise=True
)
def send_email(subject, content):
    try:
        validate_environment_variables()
        validate_email_parameters(subject, content)
        html_content = generate_html_content(subject, content)

        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        email = Mail(
            from_email=SENDGRID_FROM_EMAIL,
            to_emails=SENDGRID_TO_EMAIL,
            subject=subject,
            html_content=html_content
        )

        response = sg.send(email)
        logger.info(f"Email sent successfully with status code {response.status_code}.")
        return response

    except requests.exceptions.RequestException as req_ex:
        logger.error(f"Network error while sending email: {req_ex}")
        raise

    except ValueError as val_ex:
        logger.error(f"Value error while sending email: {val_ex}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error while sending email: {e}")
        raise
