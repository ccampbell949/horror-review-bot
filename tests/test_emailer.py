import pytest
from unittest.mock import patch, MagicMock
from horrorbot.emailer.client import EmailClient

def test_send_email():
    email_client = EmailClient("test@example.com", "password")
    
    with patch("smtplib.SMTP") as mock_smtp_class:
        mock_smtp_instance = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp_instance
        
        # Call the method
        result = email_client.send("subject", "body", "to@example.com", "test.jpg")
        
        # Check if login was called with the right credentials
        mock_smtp_instance.login.assert_called_once_with("test@example.com", "password")
        
        # Check if send_message was called
        assert mock_smtp_instance.send_message.called
        
        # Assert the method returns True (you'll need to adjust your Emailer method accordingly)
        assert result is True
