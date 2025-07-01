import time
import logging
from src.InternetChecker import InternetChecker
from src.EmailSender import EmailSender

class IpChangeEmailNotifier(object):
    """Checks IP changes periodically and sends the new IP address via e-mail."""
    def __init__(self, receiver_email="receiver@gmail.com", ip_check_period_in_seconds=10):
        self.receiver_email = receiver_email
        self.ip_check_period_in_seconds = ip_check_period_in_seconds
        self.last_ip = None

    def check_and_notify(self):
        if not InternetChecker.has_internet():
            logging.error("Internet is not available!")
            return

        current_ip = InternetChecker.get_public_ip_address()
        if not current_ip:
            logging.error("Could not fetch IP Address!")
            return

        if current_ip == self.last_ip:
            logging.info(f"IP {current_ip} unchanged.")
            return

        email_send_result = EmailSender.send(new_ip=current_ip, receiver=self.receiver_email)
        if not email_send_result:
            logging.error(f"Could not send IP change ({current_ip}) to {self.receiver_email}!")
            return

        logging.info(f"IP changed: {current_ip} (email sent).")
        self.last_ip = current_ip

    def run(self):
        logging.info("Starting IP change notifier.")
        while True:
            try:
                self.check_and_notify()
            except Exception:
                logging.exception("Error in check_and_notify function.")

            time.sleep(self.ip_check_period_in_seconds)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    ip_change_notifier = IpChangeEmailNotifier()
    ip_change_notifier.run()
