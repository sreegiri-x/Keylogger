# Educational Keylogger – Awareness Tool (v1)

**⚠️ WARNING: For educational and authorised testing only.  
Unauthorised use is illegal and unethical.**

This project demonstrates how keystroke logging works on Windows, macOS, and Linux.  
It is intended to raise awareness about cybersecurity risks and promote safe practices.

## Features
- Cross‑platform (Python + pynput)
- Logs keystrokes locally with timestamps
- Optional email exfiltration (configurable)

## How to Run
1. Install Python 3.6+ and `pip install pynput`
2. Configure settings at the top of `keylogger.py`
3. Run: `python keylogger.py`
4. Press `ESC` to stop.

## Configuration
- `LOG_FILE` – path to log file
- `SEND_EMAIL` – set `True` to enable email sending
- `EMAIL_INTERVAL` – seconds between reports
- Fill in SMTP credentials **only in a safe, isolated environment**

## Disclaimer
This software is provided solely for educational purposes.  
The author is not responsible for any misuse. By using this code, you agree to comply with all applicable laws.

## License
MIT (or your chosen license)