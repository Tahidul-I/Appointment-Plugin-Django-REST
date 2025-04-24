from django.shortcuts import redirect
import stripe
import paypalrestsdk
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from ..send_email.utils import *
from ..authentication.utils import get_client_obj,get_superuser_obj
from cryptography.fernet import Fernet
from django.conf import settings
from .models import *
from .utils import *
from ..orders.models import Order 
from ..client.models import ClientProfile
from ..booking.models import AppointmentBooking
from ..authentication.utils import create_client_credentials
from django.utils import timezone
from django.contrib.auth.models import User
stripe.api_key = settings.STRIPE_SECRET_KEY
import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def stripe_payment_success(request):
    if request.method == 'GET':
        session_id = request.GET.get('session_id')
        session = stripe.checkout.Session.retrieve(session_id)
        order_id = int(session.metadata.get('order_id'))
        order_obj = Order.objects.get(id=order_id)
        order_obj.is_successful = True
        order_obj.save()
        required_data = create_client_credentials(order_obj.company_name)
        client = ClientProfile(
            user=required_data['user_obj'],
            company_name=order_obj.company_name,
            domain=order_obj.domain,
            email=order_obj.email,
            address=order_obj.address,
            city = order_obj.city,
            country = order_obj.country,
            created_at = timezone.now()
            )
        client.save()
        send_credential_email = send_client_crdential_email(required_data['username'],required_data['password'],client)
        if send_credential_email == 'success':
            return redirect('https://www.freepik.com/free-photos-vectors/nature-wallpaper',status=200)
        else:
            return redirect('https://codersquad.io')


def stripe_payment_cancel(request):
    return redirect('https://stock.adobe.com/search?k=nature+wallpaper+hd')

@api_view(['GET'])
def paypal_payment_success(request):
    paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
    })
    payment_id = request.GET.get('paymentId')  # Get paymentId from the query parameters
    payer_id = request.GET.get('PayerID')      # Get PayerID from the query parameters
    payment = paypalrestsdk.Payment.find(payment_id) # Get the whole paypal session

    if payment.execute({"payer_id": payer_id}):  #If its True, means payment successful
        order_id = None
        for transaction in payment.transactions:
            order_id = int(transaction['custom'])  # Retrieve custom field
            break;
        order_obj = Order.objects.get(id=order_id)
        order_obj.is_successful = True
        order_obj.save()
        required_data = create_client_credentials(order_obj.company_name)
        client = ClientProfile(
            user=required_data['user_obj'],
            company_name=order_obj.company_name,
            domain=order_obj.domain,
            email=order_obj.email,
            address=order_obj.address,
            city = order_obj.city,
            country = order_obj.country,
            created_at = timezone.now()
            )
        client.save()
        send_credential_email = send_client_crdential_email(required_data['username'],required_data['password'],client)
        if send_credential_email == 'success':
            return Response({'status_code':200,'message':'Please check your email for details. Thanks for your purchase'})
        else:
            return Response({'status_code':400,'message':'Something went wrong'})
    else:
        return Response({'status_code':400,'message':'Payment Error'})
    
def paypal_payment_cancel(request):
    return redirect('https://stock.adobe.com/search?k=nature+wallpaper+hd')


@csrf_exempt
def client_stripe_payment_success(request):
    if request.method == 'GET':
        session_id = request.GET.get('session_id')
        session = stripe.checkout.Session.retrieve(session_id)
        appoint_id = int(session.metadata.get('appoint_id'))
        appoinment_obj = AppointmentBooking.objects.get(id=appoint_id)
        appoinment_obj.is_success = True
        appoinment_obj.save()
        send_booking_email = send_appointment_email(appoinment_obj)
        if send_booking_email == 'success':
            return redirect('http://localhost:3000/payment-success',status=200)
        else:
            return Response({'status_code':400,'message':'Something went wrong'})


@api_view(['GET'])
def client_paypal_payment_success(request):
    appoint_id = int(request.GET.get('appoint_id'))
    appoinment_obj = AppointmentBooking.objects.get(id=appoint_id)
    encrypted_paypal_credentials = PaypalPaymentGateway.objects.get(client = appoinment_obj.client)
    decrypted_paypal_credentials = decrypt_paypal_credentials(encrypted_paypal_credentials.paypal_credentials)
    paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": decrypted_paypal_credentials['paypal_client_id'],
    "client_secret": decrypted_paypal_credentials['paypal_secret']
    })
    payment_id = request.GET.get('paymentId')  # Get paymentId from the query parameters
    payer_id = request.GET.get('PayerID')      # Get PayerID from the query parameters
    payment = paypalrestsdk.Payment.find(payment_id) # Get the whole paypal session
    if payment.execute({"payer_id": payer_id}):  #If its True, means payment successful
       appoinment_obj.is_success = True
       appoinment_obj.save()
       send_booking_email = send_appointment_email(appoinment_obj)
       if send_booking_email == 'success':
           return redirect('http://localhost:3000/payment-success',status=200)
       else:
           return Response({'status_code':400,'message':'Something went wrong'})


# Saving Client's payment credentials

@api_view(['POST'])
def save_client_stripe_account_credentials(request):
    superuser_access_token = request.COOKIES.get('sp_acs_tkn')
    superuser = get_superuser_obj(superuser_access_token)
    if superuser is not None:
        data = request.data
        client_id = int(data.get('client_id'))
        stripe_secret_key = data.get('stripe_secret_key')
        encrypted_stripe_secret_key = encrypt_stripe_credentials(stripe_secret_key)
        StripePaymentGateway(
            client_id = client_id,
            stripe_secret_key = encrypted_stripe_secret_key
        ).save()
        return Response({'status_code':200,'message':'Stripe Credentials Saved Successfully'})
    else:
        return Response({'status_code':400,'message':'Access Denied'})




@api_view(['POST'])
def save_client_paypal_account_credentials(request):
    superuser_access_token = request.COOKIES.get('sp_acs_tkn')
    superuser = get_superuser_obj(superuser_access_token)
    if superuser is not None:
        data = request.data
        client_id = int(data.get('client_id'))
        paypal_client_id = data.get('paypal_client_id')
        paypal_secret = data.get('paypal_secret')
        encrypted_paypal_credentials = encrypt_paypal_credentials(paypal_client_id,paypal_secret)
        PaypalPaymentGateway(
            client_id = client_id,
            paypal_credentials = encrypted_paypal_credentials
        ).save()

        return Response({'status_code':200,'message':'Paypal Credentials Saved Successfully'})
    else:
        return Response({'status_code':400,'message':'Access Denied'})

@api_view(['POST'])
def check_token_validity(request):
    token = request.data.get('token')
    str_length = len(token)

    return Response({'length':str_length})