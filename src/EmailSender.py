import logging
import yagmail

class EmailSender(object):
    """EmailSender class for sending IP Address via e-mail."""

    @staticmethod
    def send(new_ip, sender="user@gmail.com", sender_password="1234567", receiver="receiver@gmail.com"):
        """Send an IP Address via e-mail to receiver."""

        try:
            yag = yagmail.SMTP(sender, sender_password)
            yag.send(
                to=receiver,
                subject="Public IP Changed",
                contents=f"Your new public IP address is: {new_ip}"
            )
            return True
        except Exception:
            logging.exception("EmailSender::send function failed!")
            return False
