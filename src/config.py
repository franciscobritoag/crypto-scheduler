from dotenv import load_dotenv
import os

# Load environment variables from .env file

# Uncomment the following line for local execution
load_dotenv(dotenv_path='sendgrid.env')

# Now you can access environment variables
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDGRID_FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL')
SENDGRID_TO_EMAIL = os.getenv('SENDGRID_TO_EMAIL')