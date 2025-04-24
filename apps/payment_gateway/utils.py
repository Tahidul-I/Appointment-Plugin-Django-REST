import base64
from cryptography.fernet import Fernet
from django.conf import settings
import json
import stripe
import paypalrestsdk

def encrypt_stripe_credentials(secret_key):
    fernet = Fernet(settings.FERNET_KEY)
    
    # Convert dictionary to JSON string
    data = {
        "stripe_secret_key": secret_key
    }
    data_json = json.dumps(data)
    
    # Encrypt the data
    encrypted_bytes = fernet.encrypt(data_json.encode())  # Encrypted bytes
    
    # Encode encrypted data in Base64 for safe storage
    encrypted_base64 = base64.b64encode(encrypted_bytes).decode()  # String for storage
    return encrypted_base64

def encrypt_paypal_credentials(paypal_client_id,paypal_secret):
    fernet = Fernet(settings.FERNET_KEY)
    data = {
        "paypal_client_id":paypal_client_id,
        "paypal_secret":paypal_secret
    }

    # Convert dictionary to JSON string
    data_json = json.dumps(data)
    encrypted_bytes = fernet.encrypt(data_json.encode()) 
    encrypted_base64 = base64.b64encode(encrypted_bytes).decode()  # String for storage
    return encrypted_base64



def decrypt_stripe_credentials(encrypted_stripe_credential):
    fernet = Fernet(settings.FERNET_KEY)
    
    # Decode from Base64 to get the original encrypted bytes
    encrypted_bytes = base64.b64decode(encrypted_stripe_credential)
    
    # Decrypt the bytes
    decrypted_data = fernet.decrypt(encrypted_bytes).decode()  # Decrypted JSON string
    
    # Parse JSON to get the original data
    data = json.loads(decrypted_data)
    stripe_secret_key = data.get("stripe_secret_key")
    return stripe_secret_key


def decrypt_paypal_credentials(encrypted_paypal_credential):
    fernet = Fernet(settings.FERNET_KEY)
    encrypted_bytes = base64.b64decode(encrypted_paypal_credential)
    decrypted_data = fernet.decrypt(encrypted_bytes).decode() 
    data = json.loads(decrypted_data)
    return data

def get_client_stripe_payment_url(encrypted_stripe_secret_key,appointment_obj):
    stripe_secret_key = decrypt_stripe_credentials(encrypted_stripe_secret_key)
    stripe.api_key = stripe_secret_key
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Example Product',
                },
                'unit_amount': int(appointment_obj.total_amount*100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://appointment.abroadportals.com/api/v1/client-stripe-payment-success/?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='https://appointment.abroadportals.com/cancel',
        metadata={
            'appoint_id': appointment_obj.id
        }
    )

    return session.url


def get_client_paypal_payment_url(encrypted_paypal_credentials,appointment_obj):
    print("*********************************** API CREDENTIALS ************************")
    print(encrypted_paypal_credentials)
    decrypted_paypal_credentials = decrypt_paypal_credentials(encrypted_paypal_credentials)
    print(decrypted_paypal_credentials['paypal_client_id'])
    print(decrypted_paypal_credentials['paypal_secret'])
    paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": decrypted_paypal_credentials['paypal_client_id'],
    "client_secret": decrypted_paypal_credentials['paypal_secret']
    })

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url":  f"https://appointment.abroadportals.com/api/v1/client-paypal-payment-success/?appoint_id={appointment_obj.id}",  # PayPal will redirect to this URL after approval
            "cancel_url": "https://appointment.abroadportals.com"  # Redirect on cancel
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Test Item",
                    "sku": "12345",
                    "price": f"{appointment_obj.total_amount}",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": f"{appointment_obj.total_amount}",
                "currency": "USD"
            },
            "description":"Test Api"
        }]
    })

    if payment.create():
        print("*********************************** PAYMENT URL CREATED *****************************")
        # Find and return the approval URL
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = link.href
                return approval_url
    else:
        print("*********************************** PAYMENT URL NOT CREATED *****************************")
        print(payment.error)
        return None

def get_stripe_payment_url_for_purchasing_plugin(order):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Example Product',
                },
                'unit_amount': int(order.total_amount) * 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://appointment.codersquad.io/api/v1/stripe-payment-success/?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='https://appointment.codersquad.io/stripe-payment-cancel/',
        metadata={
            'order_id': order.id, 
        }
    )

    return session.url


def get_paypal_payment_url_for_purchasing_plugin(order):
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,  # sandbox or live
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })
    
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "https://appointment.abroadportals.com/api/v1/paypal-payment-success/",  # PayPal will redirect to this URL after approval
            "cancel_url": "https://appointment.abroadportals.com/api/v1/paypal-payment-cancel/"  # Redirect on cancel
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Test Item",
                    "sku": "12345",
                    "price": f"{order.total_amount}",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": f"{order.total_amount}",
                "currency": "USD"
            },
            "description": "Payment for Test Item",
            "custom": str(order.id)  # Use the 'custom' field to pass order_id
        }]
    })

    if payment.create():
        # Find and return the approval URL
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = link.href
                return approval_url
    else:
        print("**************************** PAYMENT CREATION FAILED *******************************")
        print(payment.error)  # Print the error for debugging
        return None





# 2024-12-10 Scheduled Date
# 2024-12-09 Scheduled Date
# 2024-12-08 Today

# email will be sent to those which exceeds 