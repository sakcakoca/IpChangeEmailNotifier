# IpChangeEmailNotifier

**IpChangeEmailNotifier** is a Python utility that monitors your public IP address and automatically sends an email notification whenever your IP changes. This is especially useful for home servers, Raspberry Pi devices, or any system running on a dynamic IP address, ensuring you always know how to reach your device remotely.

---

## Features

- **Periodic IP Monitoring:** Checks your public IP address at a configurable interval.
- **Email Notifications:** Sends an email to a specified recipient when the IP address changes.
- **Robust Logging:** Logs all actions and errors for easy troubleshooting.
- **Customizable:** Easily configure the recipient email and check interval.

---

## How It Works

The main class, `IpChangeEmailNotifier`, periodically checks your public IP address using the `InternetChecker` module. If the IP address has changed since the last check, it sends an email notification using the `EmailSender` module and updates its record of the last known IP.

---

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/sakcakoca/IpChangeEmailNotifier.git
    cd IpChangeEmailNotifier
    ```

2. **Install dependencies:**
    ```sh
    pip install requests yagmail
    ```

3. **Configure your email credentials:**
    - Edit `src/EmailSender.py` to set your sender email and password, or use environment variables for better security.

---

## Usage

Run the notifier with default settings:

```sh
python -m src.IpChangeEmailNotifier
```

## Requirements

- Python 3.7+
- [requests](https://pypi.org/project/requests/)
- [yagmail](https://pypi.org/project/yagmail/)
- [ipaddress](https://pypi.org/project/ipaddress/)

---

## Project Structure

src/ 
├── IpChangeEmailNotifier.py
├── InternetChecker.py
└── EmailSender.py
