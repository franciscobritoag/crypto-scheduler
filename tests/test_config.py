import os
import tempfile
import pytest
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def cleanup_env_files():
    """Fixture to clean up environment files after each test."""
    yield
    # Remove any files that were created during tests
    for file in ['invalid_format.env', 'sendgrid.test.env']:
        if os.path.exists(file):
            os.remove(file)

def clear_environment():
    """Helper function to clear environment variables."""
    for key in ['SENDGRID_API_KEY', 'SENDGRID_FROM_EMAIL', 'SENDGRID_TO_EMAIL']:
        os.environ.pop(key, None)  # Safely remove environment variables if they exist

def create_env_file(content):
    """Helper function to create a temporary .env file with specific content."""
    temp_env_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.env')
    temp_env_file.write(content)
    temp_env_file.close()
    return temp_env_file.name

def test_environment_variables_loading(cleanup_env_files):
    clear_environment()  # Clear environment variables before the test

    env_content = """SENDGRID_API_KEY=test_api_key
SENDGRID_FROM_EMAIL=test_from_email@example.com
SENDGRID_TO_EMAIL=test_to_email@example.com
"""
    temp_env_file = create_env_file(env_content)
    
    try:
        # Load environment variables from the test file
        result = load_dotenv(dotenv_path=temp_env_file)
        assert result, "Failed to load environment variables from the .env file"

        # Fetch environment variables
        api_key = os.getenv('SENDGRID_API_KEY')
        from_email = os.getenv('SENDGRID_FROM_EMAIL')
        to_email = os.getenv('SENDGRID_TO_EMAIL')

        # Assertions to verify environment variables are correctly loaded
        assert api_key == 'test_api_key', f"Expected 'test_api_key' but got {api_key}"
        assert from_email == 'test_from_email@example.com', f"Expected 'test_from_email@example.com' but got {from_email}"
        assert to_email == 'test_to_email@example.com', f"Expected 'test_to_email@example.com' but got {to_email}"

        # Log environment variables for debugging purposes
        logger.info(f"SENDGRID_API_KEY: {api_key}")
        logger.info(f"SENDGRID_FROM_EMAIL: {from_email}")
        logger.info(f"SENDGRID_TO_EMAIL: {to_email}")
    
    finally:
        os.remove(temp_env_file)  # Cleanup the temp file

def test_missing_env_file(cleanup_env_files):
    clear_environment()  # Clear environment variables before the test

    # Test behavior when the .env file is missing
    result = load_dotenv(dotenv_path='missing.env')
    assert not result, "Expected load_dotenv to return False when the file is missing"

def test_invalid_env_file_format(cleanup_env_files):
    clear_environment()  # Clear environment variables before the test

    invalid_env_content = "SENDGRID_API_KEY=test_api_key\nSENDGRID_FROM_EMAIL\nSENDGRID_TO_EMAIL=\n"
    temp_invalid_env_file = create_env_file(invalid_env_content)

    try:
        # Load the invalid .env file
        result = load_dotenv(dotenv_path=temp_invalid_env_file)

        # Fetch environment variables
        api_key = os.getenv('SENDGRID_API_KEY')
        from_email = os.getenv('SENDGRID_FROM_EMAIL')
        to_email = os.getenv('SENDGRID_TO_EMAIL')

        # Check if load_dotenv returned True, meaning the file was loaded
        assert result, "Expected load_dotenv to return True even with invalid format"

        # Assert environment variables
        assert api_key == 'test_api_key', f"Expected 'test_api_key' but got {api_key}"
        
        # Check that improperly formatted variables are not set
        assert from_email is None, f"Expected None but got {from_email}"
        assert to_email == '', f"Expected empty string but got {to_email}"
    
    finally:
        os.remove(temp_invalid_env_file)  # Cleanup the invalid file
