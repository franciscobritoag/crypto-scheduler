import pytest
from unittest.mock import patch, Mock
import requests
from src.email_sender import send_email, validate_email_parameters, generate_html_content

# Sample configuration values for testing
SENDGRID_API_KEY = 'fake_api_key'
SENDGRID_FROM_EMAIL = 'test@example.com'
SENDGRID_TO_EMAIL = 'recipient@example.com'

# Mock configurations for testing
@patch('src.email_sender.SENDGRID_API_KEY', SENDGRID_API_KEY)
@patch('src.email_sender.SENDGRID_FROM_EMAIL', SENDGRID_FROM_EMAIL)
@patch('src.email_sender.SENDGRID_TO_EMAIL', SENDGRID_TO_EMAIL)
class TestEmailSender:

    @patch('src.email_sender.sendgrid.SendGridAPIClient')
    @patch('src.email_sender.Mail')
    def test_send_email_success(self, MockMail, MockSendGridAPIClient):
        mock_response = Mock()
        mock_response.status_code = 202
        MockSendGridAPIClient.return_value.send.return_value = mock_response

        response = send_email('Test Subject', 'Test Content')

        assert response is not None
        assert response.status_code == 202

    def test_validate_email_parameters(self):
        # Test valid parameters
        try:
            validate_email_parameters('Subject', 'Content')
        except ValueError:
            pytest.fail("validate_email_parameters raised ValueError unexpectedly")

        # Test missing subject
        with pytest.raises(ValueError):
            validate_email_parameters('', 'Content')

        # Test missing content
        with pytest.raises(ValueError):
            validate_email_parameters('Subject', '')

    @patch('src.email_sender.sendgrid.SendGridAPIClient')
    def test_send_email_request_exception(self, MockSendGridAPIClient):
        MockSendGridAPIClient.side_effect = requests.exceptions.RequestException("Request failed")

        with patch('src.email_sender.logger') as mock_logger:
            response = send_email('Test Subject', 'Test Content')
            assert response is None
            mock_logger.error.assert_called_with("Request error: %s", MockSendGridAPIClient.side_effect)

    @patch('src.email_sender.sendgrid.SendGridAPIClient')
    def test_send_email_unexpected_exception(self, MockSendGridAPIClient):
        MockSendGridAPIClient.side_effect = Exception("Unexpected error")

        with patch('src.email_sender.logger') as mock_logger:
            response = send_email('Test Subject', 'Test Content')
            assert response is None
            mock_logger.error.assert_called_with("Unexpected error sending email: %s", MockSendGridAPIClient.side_effect)

    def test_generate_html_content(self):
        subject = 'Test Subject'
        content = '<p>Test Content</p>'
        html_content = generate_html_content(subject, content)

        assert '<h2>Test Subject</h2>' in html_content
        assert '<p>Test Content</p>' in html_content
