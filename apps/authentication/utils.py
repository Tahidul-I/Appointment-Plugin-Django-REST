from django.contrib.auth.models import User
import random
import string
import uuid
import json
from ..client.models import ClientProfile
from ..staff.models import StaffProfile
from django.utils import timezone
from cryptography.fernet import Fernet
from django.conf import settings
import logging
logger = logging.getLogger(__name__)


def generate_unique_username(name):
    base_username = name.lower().replace(' ', '_')
    username = base_username
    counter = 1

    while User.objects.filter(username=username).exists():
        username = f"{base_username}_{counter}"
        counter += 1

    return username


def generate_random_password():
    # Characters to include in the password
    special_chars = ',/#%'
    all_chars = string.ascii_letters + string.digits + special_chars

    # Generate a random 8-character part using letters, digits, and special characters
    random_part = ''.join(random.choice(all_chars) for _ in range(8))

    # Generate a 4-character unique UUID
    uuid_part = str(uuid.uuid4())[:4]

    # Combine both parts to form the final password
    password = random_part + uuid_part

    return password

def create_client_credentials(name):
    username  = generate_unique_username(name)
    password = generate_random_password()
    user = User.objects.create_user(username=username,password=password,is_active=True,is_staff=True)
    data = {'user_obj':user,'username':username,'password':password}
    return data


def encrypt_client_credentials(existing_user):
    fernet = Fernet(settings.FERNET_KEY)
    data = {
        "client_id":existing_user.client_profile.id,
        "user_id":existing_user.id
    }

    # Convert dictionary to JSON string
    data_json = json.dumps(data)
    token = fernet.encrypt(data_json.encode())
    return token

def encrypt_superuser_credentials(superuser_id):
    fernet = Fernet(settings.FERNET_KEY)
    data = {
        "superuser_id":superuser_id,
    }

    # Convert dictionary to JSON string
    data_json = json.dumps(data)
    token = fernet.encrypt(data_json.encode())
    return token

def get_superuser_obj(token):
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_data = fernet.decrypt(token)
    # Decode the JSON string
    data_json = decrypted_data.decode()
    # Parse the JSON string into a dictionary
    data = json.loads(data_json)
    user_id = data.get('superuser_id')
    user = None
    try:
        user = User.objects.get(id=user_id,is_superuser=True,is_active=True)
    except:
        pass
    return user

def get_client_obj(token):
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_data = fernet.decrypt(token)
    # Decode the JSON string
    data_json = None
    try:
        data_json = decrypted_data.decode()
    except:
        pass
    
    if data_json is not None:
        # Parse the JSON string into a dictionary
        data = json.loads(data_json)
        client_id = data.get('client_id')
        client = ClientProfile.objects.get(id=client_id)
        if client.user.is_active == True:
            return client
        else:
            return None
    else:
         return None

def get_user_obj(token):
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_data = fernet.decrypt(token)
    # Decode the JSON string
    data_json = decrypted_data.decode()
    # Parse the JSON string into a dictionary
    data = json.loads(data_json)
    user_id = data.get('user_id')
    user = User.objects.get(id=user_id)
    return user

def get_moderator_obj(token):
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_data = fernet.decrypt(token)
    data_json = None
    # Parse the JSON string into a dictionary
    data = json.loads(data_json)
    user_id = data.get('moderator_id')
    user = User.objects.get(id=user_id)
    return user

def encrypt_staff_credentials(client_id,staff_id):
    fernet = Fernet(settings.FERNET_KEY)
    data = {
        "client_id":client_id,
        "staff_id":staff_id
    }

    # Convert dictionary to JSON string
    data_json = json.dumps(data)
    token = fernet.encrypt(data_json.encode())
    return token

def get_staff_obj(token):
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_data = fernet.decrypt(token)
    try:
        # Decode the JSON string
        data_json = decrypted_data.decode()
    except:
        pass
    if data_json:
        # Parse the JSON string into a dictionary
        data = json.loads(data_json)
        staff_id = data.get('staff_id')
        client_id = data.get('client_id')
        client = ClientProfile.objects.get(id=client_id)
        if client.user.is_active == True:
            staff = StaffProfile.objects.get(client_id = client_id, id = staff_id)
            return staff
        else:
            None
    else:
        return None


def authenticate_plugin_access_permission(unique_key,domain):
    client = None
    try:
        client = ClientProfile.objects.get(unique_key=unique_key,domain=domain)
    except:
        pass
    if client.user.is_active == True:
        return client
    else:
        return None

def encrypt_email_otp(user_obj,otp):
    fernet = Fernet(settings.FERNET_KEY)
    data = {
        "email":user_obj.email,
        "otp":otp,
        "timestamp":user_obj.created_at.isoformat() 
    }

    # Convert dictionary to JSON string
    data_json = json.dumps(data)
    token = fernet.encrypt(data_json.encode())
    return token

def decrypt_email_otp_token(token):
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_data = fernet.decrypt(token)
    data_json = decrypted_data.decode()
    data = json.loads(data_json)
    email = data.get('email')
    otp = data.get('otp')
    timestamp = timezone.datetime.fromisoformat(data["timestamp"])
    return {'email':email,'otp':otp,'timestamp':timestamp}


def encrypt_general_user_token(user):
    fernet = Fernet(settings.FERNET_KEY)
    data = {
        "name":user.name,
        "email":user.email
    }
    data_json = json.dumps(data)
    token = fernet.encrypt(data_json.encode())
    return token

def decrypt_general_user_token(token):
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_data = fernet.decrypt(token)
    data_json = decrypted_data.decode()
    data = json.loads(data_json)
    name = data.get('name')
    email = data.get('email')
    return {'name':name,'email':email}