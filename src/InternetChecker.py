import requests
import logging

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
    def get_public_ip_address(services=(
            "https://api.ipify.org",
            "https://ifconfig.me/ip",
            "https://ipecho.net/plain",
            "https://checkip.amazonaws.com")):

        for service in services:
            try:
                ip = requests.get(service, timeout=5).text.strip()
                if ip:
                    return ip
            except requests.RequestException:
                logging.exception(f"Could not get successful reply to request from {service}!")
                continue
            except Exception:
                logging.exception("InternetChecker::get_public_ip_address failed!")
                return None

        return None
