import os
import sys
import requests
import unittest
import unittest.mock as mock
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.InternetChecker import InternetChecker

class TestInternetChecker(unittest.TestCase):
    """Tests for InternetChecker class"""

    def test_has_internet_real(self):
        """Doesn't mock anything and calls the real test_has_internet_real() function."""
        self.assertTrue(InternetChecker.has_internet())

    @mock.patch("requests.get")
    @mock.patch("logging.exception")
    def test_has_internet_successful(self, mock_logging_exception, mock_requests_get):
        """When requests.get is successful, it should return True."""
        #Arrange
        mock_requests_get.return_value.ok = True

        #Act
        result_has_internet = InternetChecker.has_internet()

        # Assert
        self.assertTrue(result_has_internet)
        mock_requests_get.assert_called_once()
        mock_logging_exception.assert_not_called()

    @mock.patch("requests.get")
    @mock.patch("logging.exception")
    def test_has_internet_fails(self, mock_logging_exception, mock_requests_get):
        """When get raises an Exception, it should log the exception and return False."""

        #Arrange
        mock_requests_get.side_effect = Exception()

        #Act
        result_has_internet = InternetChecker.has_internet()

        #Assert
        self.assertFalse(result_has_internet)
        mock_requests_get.assert_called_once()
        mock_logging_exception.assert_called_once()

    def test_get_public_ip_address_real(self):
        """Doesn't mock anything and calls the real get_public_ip_address() function."""
        self.assertTrue(InternetChecker.get_public_ip_address())

    @mock.patch("requests.get")
    @mock.patch("logging.exception")
    def test_get_public_ip_address_successful(self, mock_logging_exception, mock_requests_get):
        """When requests.get is successful for the server then it should parse the IP Address and return it."""

        #Arrange
        test_ip = "203.0.113.42"
        mock_response = MagicMock()
        mock_response.text = test_ip
        mock_requests_get.return_value = mock_response

        #Act
        result_public_ip = InternetChecker.get_public_ip_address()

        #Assert
        self.assertEqual(test_ip, result_public_ip)
        mock_requests_get.assert_called_once()
        mock_logging_exception.assert_not_called()

    @mock.patch("requests.get")
    @mock.patch("logging.exception")
    def test_get_public_ip_address_get_fails_until_last_service(self, mock_logging_exception, mock_requests_get):
        """When a service raises RequestException, it should try to connect to the next service from services list."""

        #Arrange
        test_ip = '203.0.113.42'
        services=("dummy_service1.com", "dummy_service2.com", "dummy_service3.com", "successful_service.com")
        num_services = len(services)

        #First (num_services - 1) calls raise, last returns mock with test_ip
        side_effects = [requests.RequestException("fail")] * (num_services - 1)
        mock_response = MagicMock()
        mock_response.text = test_ip
        side_effects.append(mock_response)
        mock_requests_get.side_effect = side_effects

        #Act
        result_public_ip = InternetChecker.get_public_ip_address()

        #Assert
        self.assertEqual(test_ip, result_public_ip)
        self.assertEqual(mock_requests_get.call_count, num_services)
        self.assertEqual(mock_logging_exception.call_count, num_services - 1)

    @mock.patch("requests.get")
    @mock.patch("logging.exception")
    def test_get_public_ip_address_get_fails_for_all_services(self, mock_logging_exception, mock_requests_get):
        """When all services raises RequestException, it should log all RequestExceptions and return None."""

        #Arrange
        services = ("dummy_service1.com", "dummy_service2.com", "dummy_service3.com", "dummy_service4.com")
        num_services = len(services)

        side_effects = [requests.RequestException("fail")] * num_services
        mock_requests_get.side_effect = side_effects

        #Act
        result_public_ip = InternetChecker.get_public_ip_address()

        #Assert
        self.assertFalse(result_public_ip)
        self.assertEqual(mock_requests_get.call_count, num_services)
        self.assertEqual(mock_logging_exception.call_count, num_services)

    @mock.patch("requests.get")
    @mock.patch("logging.exception")
    def test_get_public_ip_address_throws_exception(self, mock_logging_exception, mock_requests_get):
        """When generic exception (not RequestException) is raised, it should log the exception and return directly."""

        #Arrange
        mock_requests_get.side_effect = Exception()

        #Act
        result_public_ip = InternetChecker.get_public_ip_address()

        #Assert
        self.assertFalse(result_public_ip)
        mock_requests_get.assert_called_once()
        mock_logging_exception.assert_called_once()

if __name__ == '__main__':
    unittest.main()
