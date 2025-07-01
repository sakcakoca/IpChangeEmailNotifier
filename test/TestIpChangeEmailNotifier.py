import os
import sys
import unittest
import unittest.mock as mock
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.IpChangeEmailNotifier import IpChangeEmailNotifier


class TestIpChangeEmailNotifier(unittest.TestCase):
    """Tests for IpChangeEmailNotifier class."""

    @mock.patch('src.IpChangeEmailNotifier.InternetChecker')
    @mock.patch('src.IpChangeEmailNotifier.EmailSender')
    @mock.patch('logging.error')
    def test_no_internet(self, mock_logging_error, mock_email_sender, mock_internet_checker):
        """When there is no internet, it logs error and doesn't send email."""
        #Arrange
        mock_internet_checker.has_internet.return_value = False
        notifier = IpChangeEmailNotifier()

        #Act
        notifier.check_and_notify()

        #Assert
        mock_logging_error.assert_called_with("Internet is not available!")
        mock_email_sender.send.assert_not_called()

    @mock.patch('src.IpChangeEmailNotifier.InternetChecker')
    @mock.patch('src.IpChangeEmailNotifier.EmailSender')
    @mock.patch('logging.error')
    def test_cannot_fetch_ip(self, mock_logging_error, mock_email_sender, mock_internet_checker):
        """"When there is internet but can't get IP Address, it logs error and doesn't send email."""
        #Arrange
        mock_internet_checker.has_internet.return_value = True
        mock_internet_checker.get_public_ip_address.return_value = None
        notifier = IpChangeEmailNotifier()

        #Act
        notifier.check_and_notify()

        #Assert
        mock_logging_error.assert_called_with("Could not fetch IP Address!")
        mock_email_sender.send.assert_not_called()

    @mock.patch('src.IpChangeEmailNotifier.InternetChecker')
    @mock.patch('src.IpChangeEmailNotifier.EmailSender')
    @mock.patch('logging.error')
    @mock.patch('logging.info')
    def test_ip_unchanged(self, mock_logging_info, mock_logging_error, mock_email_sender, mock_internet_checker):
        """When IP is unchanged, it logs info and doesn't send email."""
        #Arrange
        test_ip = "1.2.3.4"
        test_receiver_email_email = "test@gmail.com"
        mock_internet_checker.has_internet.return_value = True
        mock_internet_checker.get_public_ip_address.return_value = test_ip
        mock_email_sender.send.return_value = True
        notifier = IpChangeEmailNotifier(receiver_email=test_receiver_email_email)

        #Act: First call (should send email)
        notifier.check_and_notify()
        #Act: Second call (IP unchanged)
        notifier.check_and_notify()

        #Assert
        mock_email_sender.send.assert_called_once_with(new_ip=test_ip, receiver=test_receiver_email_email)
        mock_logging_info.assert_any_call(f"IP changed: {test_ip} (email sent).")
        mock_logging_info.assert_any_call(f"IP {test_ip} unchanged.")
        mock_logging_error.assert_not_called()

    @mock.patch('src.IpChangeEmailNotifier.InternetChecker')
    @mock.patch('src.IpChangeEmailNotifier.EmailSender')
    @mock.patch('logging.error')
    @mock.patch('logging.info')
    def test_ip_changed_and_email_sent(self, mock_logging_info, mock_logging_error, mock_email_sender, mock_internet_checker):
        """When IP is changed, it sends the IP info via e-mail."""
        #Arrange
        test_ip = "102.221.33.4"
        test_receiver_email_email = "test@gmail.com"
        mock_internet_checker.has_internet.return_value = True
        mock_internet_checker.get_public_ip_address.return_value = test_ip
        mock_email_sender.send.return_value = True
        notifier = IpChangeEmailNotifier(receiver_email=test_receiver_email_email)

        #Act
        notifier.check_and_notify()

        #Assert
        mock_email_sender.send.assert_called_once_with(new_ip=test_ip, receiver=test_receiver_email_email)
        mock_logging_info.assert_any_call(f"IP changed: {test_ip} (email sent).")
        mock_logging_error.assert_not_called()

    @mock.patch('src.IpChangeEmailNotifier.InternetChecker')
    @mock.patch('src.IpChangeEmailNotifier.EmailSender')
    @mock.patch('logging.error')
    @mock.patch('logging.info')
    def test_email_sent_twice_with_different_ips(self, mock_logging_info, mock_logging_error, mock_email_sender, mock_internet_checker):
        """Test that EmailSender.send is called twice with different IP addresses when the public IP changes twice."""
        #Arrange
        test_ip1 = "1.2.3.4"
        test_ip2 = "5.6.7.8"
        test_receiver_email = "receiver@gmail.com"

        mock_internet_checker.has_internet.return_value = True
        #Simulate two different IPs on two consecutive calls
        mock_internet_checker.get_public_ip_address.side_effect = [test_ip1, test_ip2]
        mock_email_sender.send.return_value = True

        notifier = IpChangeEmailNotifier(receiver_email=test_receiver_email)

        #Act: First call with first IP
        notifier.check_and_notify()
        #Act: Second call with second IP
        notifier.check_and_notify()

        #Assert: send called twice, each with the correct IP
        expected_calls = [
            mock.call(new_ip=test_ip1, receiver=test_receiver_email),
            mock.call(new_ip=test_ip2, receiver=test_receiver_email)
        ]
        self.assertEqual(mock_email_sender.send.call_args_list, expected_calls)
        mock_logging_info.assert_any_call(f"IP changed: {test_ip1} (email sent).")
        mock_logging_info.assert_any_call(f"IP changed: {test_ip2} (email sent).")
        mock_logging_error.assert_not_called()

    @mock.patch('src.IpChangeEmailNotifier.InternetChecker')
    @mock.patch('src.IpChangeEmailNotifier.EmailSender')
    @mock.patch('logging.error')
    def test_ip_changed_but_cannot_send_email(self, mock_logging_error, mock_email_sender, mock_internet_checker):
        """When cannot send email, it logs error."""
        #Arrange
        test_ip = "4.5.6.7"
        test_receiver_email_email = "test@gmail.com"
        mock_internet_checker.has_internet.return_value = True
        mock_internet_checker.get_public_ip_address.return_value = test_ip
        mock_email_sender.send.return_value = False
        notifier = IpChangeEmailNotifier(receiver_email=test_receiver_email_email)

        #Act
        notifier.check_and_notify()

        #Assert
        mock_email_sender.send.assert_called_once_with(new_ip=test_ip, receiver=test_receiver_email_email)
        mock_logging_error.assert_called_with(f"Could not send IP change ({test_ip}) to {test_receiver_email_email}!")

    @mock.patch('src.IpChangeEmailNotifier.InternetChecker')
    @mock.patch('src.IpChangeEmailNotifier.EmailSender')
    @mock.patch('logging.error')
    @mock.patch('logging.info')
    def test_email_send_failure_retries_on_same_ip(self, mock_logging_info, mock_logging_error, mock_email_sender, mock_internet_checker):
        """
        Test that if sending the email fails (EmailSender.send returns False),
        the notifier does not update last_ip and will attempt to send the email again
        on the next check, even if the IP address has not changed.
        """
        #Arrange
        test_ip = "1.9.0.5"
        test_receiver_email_email = "test@gmail.com"
        mock_internet_checker.has_internet.return_value = True
        mock_internet_checker.get_public_ip_address.return_value = test_ip

        #First call: send fails, Second call: send succeeds
        mock_email_sender.send.side_effect = [False, True]

        notifier = IpChangeEmailNotifier(receiver_email=test_receiver_email_email)

        #Act: First call (send fails)
        notifier.check_and_notify()
        #Act: Second call (send succeeds)
        notifier.check_and_notify()

        #Assert: send called twice with same arguments
        self.assertEqual(2, mock_email_sender.send.call_count)
        expected_call = mock.call(new_ip=test_ip, receiver=test_receiver_email_email)
        self.assertEqual(mock_email_sender.send.call_args_list, [expected_call, expected_call])

        #Assert: last_ip is updated only after successful send
        self.assertEqual(notifier.last_ip, test_ip)

        #Assert: correct logging
        mock_logging_error.assert_any_call(f"Could not send IP change ({test_ip}) to {test_receiver_email_email}!")
        mock_logging_info.assert_called_with(f"IP changed: {test_ip} (email sent).")

if __name__ == '__main__':
    unittest.main()
