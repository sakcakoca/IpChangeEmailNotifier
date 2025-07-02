import requests
import logging
import ipaddress

class InternetChecker(object):

    @staticmethod
    def has_internet():
        try:
            requests.get("https://www.google.com", timeout=5)
            return True
        except Exception as e:
            logging.exception("InternetChecker::has_internet failed!")
            return False

    @staticmethod
    def is_valid_ip(ip):
        try:
            return isinstance(ipaddress.ip_address(ip), ipaddress.IPv4Address)
        except Exception:
            return False

    @classmethod
    def get_public_ip_address(cls, services=(
            "https://api.ipify.org",
            "https://ifconfig.me/ip",
            "https://ipecho.net/plain",
            "https://checkip.amazonaws.com")):

        for service in services:
            try:
                ip = requests.get(service, timeout=5).text.strip()
                if cls.is_valid_ip(ip):
                    return ip
                else:
                    logging.error(f"Service ({service}) returned an invalid IP: {ip}")
            except requests.RequestException:
                logging.exception(f"Could not get successful reply to request from {service}!")
                continue
            except Exception:
                logging.exception("InternetChecker::get_public_ip_address failed!")
                return None

        return None
