from .models import ClientProfile

def get_client(unique_key,domain):
    client = None
    try:
        client = ClientProfile.objects.get(unique_key=unique_key,domain=domain)
    except:
        pass
    if client.user.is_active == True:

        return client
    else:
        return None