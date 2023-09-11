import os
from dotenv import load_dotenv

load_dotenv()

DEVICE_ID = os.getenv('PUSHOVER_DEVICE_ID')
EMAIL_USERNAME = os.getenv('PUSHOVER_EMAIL_USERNAME')
PASSWORD = os.getenv('PUSHOVER_PASSWORD')

MESSAGE_URL = os.getenv('MESSAGE_URL', 'https://api.pushover.net/1/messages.json')
LOGIN_URL = os.getenv('LOGIN_URL', 'https://api.pushover.net/1/users/login.json')
DEVICE_REGISTRATION_URL = os.getenv('DEVICE_REGISTRATION_URL', 'https://api.pushover.net/1/devices.json')
CLEAR_MESSAGE_URL = os.getenv('DEVICE_REGISTRATION_URL',
                              'https://api.pushover.net/1/devices/{device_id}/update_highest_message.json')
