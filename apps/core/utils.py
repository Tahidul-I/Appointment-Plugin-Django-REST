import uuid
import json
from cryptography.fernet import Fernet
from django.conf import settings

def generate_random_token():
    token = str(uuid.uuid4()).replace('-', '')
    return token

def encrypt_browser_token(token):
    fernet = Fernet(settings.FERNET_KEY)
    data = {
        "browser_token":token,
    }
    data_json = json.dumps(data)
    token = fernet.encrypt(data_json.encode())
    return token

def decrypt_browser_token(token):
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_data = fernet.decrypt(token)
    data_json = None
    try:
        data_json = decrypted_data.decode()
    except:
        pass
    if data_json is not None:
        data = json.loads(data_json)
        browser_token = data.get('browser_token')
        return browser_token
    else:
        return None
    
def encrypt_time_slot(time_slot):
    fernet = Fernet(settings.FERNET_KEY)
    data = {
        "time_slot":token,
    }
    data_json = json.dumps(data)
    token = fernet.encrypt(data_json.encode())
    return token


def decrypt_time_slot_token(token):
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_data = fernet.decrypt(token)
    data_json = None
    try:
        data_json = decrypted_data.decode()
    except:
        pass
    if data_json is not None:
        data = json.loads(data_json)
        browser_token = data.get('time_slot')
        return browser_token
    else:
        return None