from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import AuthServiceUser
from .utils import encrypt_client_id,get_client_from_client_id
from ..client.models import ClientProfile
from ..authentication.utils import encrypt_email_otp,decrypt_email_otp_token
from ..send_email.utils import send_otp_to_email
import random
import bcrypt
# Create your views here.
@api_view(['POST'])
def change_auth_service_usage_status(request):
    username = request.data.get('username')
    client = ClientProfile.objects.get(user__username = username)
    if client.using_auth_service:
        client.using_auth_service = False
        client.save()
    else:
        client.using_auth_service = True
        client.save()
    return Response({'status_code':200,'message':'Status Changed'})


@api_view(['GET'])
def get_signup_url(request):
    data = request.GET
    unique_key = data.get('api_key')
    domain = data.get('domain')
    client = ClientProfile.objects.get(unique_key=unique_key,domain=domain)
    if client.user.is_active:
        if client.using_auth_service:
            token = encrypt_client_id(client.id)
            response = Response({'status_code':200,'url':'http://localhost:3000/signup/'})
            response.set_cookie(
                key='clnt_idfn_tkn',
                value=token.decode(),
                httponly=True,
                secure=True, 
                samesite='None',
                max_age=1*86400
            )
            return response
        else:
            return Response({'status_code':400,'message':'Auth service is not enabled'})
    else:
        return Response({'status_code':400,'message':'Subscription Expired'})



@api_view(['POST'])
def signup(request):
    data = request.data
    email = data.get('email')
    existing_user = None
    try:
        existing_user = AuthServiceUser.objects.get(email=email,is_active=True)
    except:
        pass
    if existing_user is None:
        otp = str(random.randint(0000, 9999)).zfill(4)
        otp_sent = send_otp_to_email(email,otp)
        if otp_sent:
            name = data.get('name')
            phone = data.get('phone')
            password = data.get('password')
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            client = get_client_from_client_id(request.COOKIES.get('clnt_idfn_tkn'))
            user_obj = AuthServiceUser(client=client,name=name,email=email,phone=phone,password=hashed_password)
            user_obj.save()
            token = encrypt_email_otp(user_obj,otp)
            response = Response({'status_code':200,'message':'An OTP has been sent to your email.'})
            response.set_cookie(
                key='ur_otp_tkn',
                value=token.decode(),
                httponly=True,
                secure=True, 
                samesite='None',
                max_age=1*86400
            )
            return response
        else:
            return Response({'status_code':400,'message':'Error occured'})
    else:
        return Response({'status_code':400,'message':'Email Already Exist'})