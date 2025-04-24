from cryptography.fernet import Fernet
from django.conf import settings
import json
from ..client.models import ClientProfile

def encrypt_client_id(client_id):
    fernet = Fernet(settings.FERNET_KEY)
    data = {
        "client_id":client_id
    }
    # Convert dictionary to JSON string
    data_json = json.dumps(data)
    token = fernet.encrypt(data_json.encode())
    return token


def get_client_from_client_id(token):
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_data = fernet.decrypt(token)
    data_json = decrypted_data.decode()
    data = json.loads(data_json)
    client_id = data.get('client_id')
    client = ClientProfile.objects.get(id=client_id)
    if client.user.is_active and client.using_auth_service:
        return client
    else:
        return None