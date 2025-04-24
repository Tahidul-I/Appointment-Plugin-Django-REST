
import socket

def check_domain_validity(domain):
    ip_address = None
    try:
        ip_address = socket.gethostbyname(domain) # It returns the IP address of a domain
    except:
        pass
    if ip_address is not None:
        return True 
    else:
        return False  