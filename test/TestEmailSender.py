import os
import sys
import unittest
import unittest.mock as mock
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.EmailSender import EmailSender

class TestEmailSender(unittest.TestCase):
    """Tests for EmailSender class"""

    @mock.patch("yagmail.SMTP")
    @mock.patch("logging.exception")
    def test_send_email_successful(self, mock_logging_exception, mock_yagmail_smtp):
        """It should send the given IP Address in e-mail content when yag.send() is successful."""

        #Arrage
        mock_yag = MagicMock()
        mock_yagmail_smtp.return_value = mock_yag

        new_ip = "192.168.127.12"
        sender="sender@gmail.com"
        sender_password="Sender1905!"
        receiver = "receiver@gmail.com"

        #Act
        send_result = EmailSender.send(new_ip, sender, sender_password, receiver)

        #Assert
        self.assertTrue(send_result)
        mock_logging_exception.assert_not_called()
        mock_yagmail_smtp.assert_called_with(sender, sender_password)
        mock_yag.send.assert_called_once()
        args, kwargs = mock_yag.send.call_args
        self.assertEqual(kwargs['to'], receiver)
        self.assertIn(new_ip, kwargs['contents'])

    @mock.patch("yagmail.SMTP")
    @mock.patch("logging.exception")
    def test_smtp_failed(self, mock_logging_exception, mock_yagmail_smtp):
        """When SMTP() raises an exception, it should log the exception and return False."""
        #Arrange
        mock_yagmail_smtp.side_effect = Exception()

        #Act
        send_result = EmailSender.send(new_ip="1.2.3.4")

        #Assert
        self.assertFalse(send_result)
        mock_logging_exception.assert_called_once()

    @mock.patch("yagmail.SMTP")
    @mock.patch("logging.exception")
    def test_send_failed(self, mock_logging_exception, mock_yagmail_smtp):
        """When SMTP.send() function raises an exception, it should log the exception and return False."""
        #Arrange
        mock_yag = MagicMock()
        mock_yag.send.side_effect = Exception("Send failed")
        mock_yagmail_smtp.return_value = mock_yag

        #Act
        send_result = EmailSender.send(new_ip="5.6.7.8")

        #Assert
        self.assertFalse(send_result)
        mock_logging_exception.assert_called_once()


if __name__ == '__main__':
    unittest.main()
