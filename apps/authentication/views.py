
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .serializers import *
from .utils import *
from ..client.models import ClientProfile
from .models import StaffAccount,GeneralUserAccount
from ..send_email.utils import *
from ..payment_gateway.utils import *
import bcrypt
import logging
logger = logging.getLogger(__name__)
from datetime import timedelta
from django.utils import timezone
import random
#----------------------------------------------------------------------#

# Uising the get request, We are authenticating the plugin access permission and then returning the plugin url

@api_view(['GET'])
def get_plugin_url(request):
    data = request.GET
    user_id = data.get('user_id')
    email = data.get('email')
    if user_id == None:
        user_id = "anonymous"
    if email:
        user_id = email
    unique_key = data.get('api_key')
    domain = data.get('domain')
    client = authenticate_plugin_access_permission(unique_key,domain)
    if client is not None:
        return Response({'url':f'http://localhost:3000/get/services/{client.unique_key}/{client.domain}/{user_id}'})
    else:
        return Response({'status_code':400,'message':'Subscription Expired'})

# ************************************************************* GENERAL USER STARTS ***************************************************************


@api_view(['POST'])
def create_general_user_account(request):
    data = request.data
    email = data.get('email')
    existing_user = None
    try:
        existing_user = GeneralUserAccount.objects.get(email = email,is_active=True)
    except:
        pass
    if existing_user is None:
        name = data.get('name')
        password = data.get('password')
        otp = str(random.randint(0000, 9999)).zfill(4)
        otp_sent = send_otp_to_email(email,otp)
        if otp_sent:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user_obj = GeneralUserAccount(name=name,email=email,password=hashed_password)
            user_obj.save()
            token = encrypt_email_otp(user_obj,otp)
            response = Response({'status_code':200,'message':'An OTP has been sent to your email.'})
            response.set_cookie(
                key='gn_ur_otp_tn',
                value=token.decode(),
                httponly=True,
                secure=True, 
                samesite='None',
                max_age=1*86400
            )
            return response
        else:
            return Response({'status_code':400,'message':'An unwanted error occured.Please try again'})
    else:
        return Response({'status_code':402,'message':'An account with this email already exist'})


@api_view(['POST'])
def resend_general_user_otp(request):
    token =  request.COOKIES.get('gn_ur_otp_tn')
    token_name = "gn_ur_otp_tn"
    if token is None:
        token =  request.COOKIES.get('gn_ur_frg_otp_tn')
        token_name = "gn_ur_frg_otp_tn"
    if token is not None:
        required_values = decrypt_email_otp_token(token)
        existing_user = None
        try:
            existing_user = GeneralUserAccount.objects.get(email = required_values['email'])
        except:
            pass
        if existing_user is not None:
            existing_user.created_at = timezone.now()
            existing_user.save()
            otp = str(random.randint(0000, 9999)).zfill(4)
            otp_sent = send_otp_to_email(existing_user.email,otp)
            if otp_sent:
                token = encrypt_email_otp(existing_user,otp)
                response = Response({'status_code':200,'message':'An OTP has been sent to your email.'})
                response.set_cookie(
                    key='gn_ur_frg_otp_tn',
                    value='',
                    httponly=True,
                    secure=True, 
                    samesite='None',
                    max_age=0
                )
                response.set_cookie(
                    key='gn_ur_otp_tn',
                    value='',
                    httponly=True,
                    secure=True, 
                    samesite='None',
                    max_age=0
                )
                response.set_cookie(
                    key=f'{token_name}',
                    value=token.decode(),
                    httponly=True,
                    secure=True, 
                    samesite='None',
                    max_age=2*86400
                )
                return response
            else:
                return Response({'status_code':400,'message':'An unwanted error occured.Please try again'})
        else:
            return Response({'status_code':400,'message':'No user found with this email'})

        
    else:
        return Response({'status_code':403,'message':'Token Missing'})


@api_view(['POST'])
def verify_general_user_email(request):
    token =  request.COOKIES.get('gn_ur_otp_tn')
    indicator = None
    if token is None:
        token =  request.COOKIES.get('gn_ur_frg_otp_tn')
        indicator = 1
    sent_otp = request.data.get('otp')
    if token is not None:
        required_values = decrypt_email_otp_token(token)
        existing_user = None
        try:
            existing_user = GeneralUserAccount.objects.get(email = required_values['email'])
        except:
            pass
        if existing_user is not None:
            current_time = timezone.now()
            token_time = required_values['timestamp']
            time_difference = current_time - token_time
            if time_difference > timedelta(minutes=5):
                return Response({'status_code':402,'message':'Your OTP has expired. Please resend the OTP'})
            if  required_values['otp'] == sent_otp:
                existing_user.is_active = True
                existing_user.save()
                response = Response({
                    'status_code':200,
                    'message': 'Email has been verified'
                })
                response.set_cookie(
                        key='gn_ur_otp_tn',
                        value='',
                        httponly=True,
                        secure=True, 
                        samesite='None',
                        max_age=0
                    )
                response.set_cookie(
                        key='gn_ur_frg_otp_tn',
                        value='',
                        httponly=True,
                        secure=True, 
                        samesite='None',
                        max_age=0
                    )
                if indicator is not None:
                    token = encrypt_email_otp(existing_user,123)
                    response.set_cookie(
                        key='cng_usr_pswrd',
                        value=token.decode(),
                        httponly=True,
                        secure=True, 
                        samesite='None',
                        max_age=2*86400
                    )
                return response
            else:
                return Response({'status_code':400,'message':'Incorrect OTP'})
        else:

            return Response({'status_code':400,'message':'No User Found With This Email'})
    else:
        return Response({'status_code':403,'message':'Token Missing'})


@api_view(['POST'])
def login_general_user(request):
    data = request.data
    email = data.get('email')
    user = None
    try:
        user = GeneralUserAccount.objects.get(email=email,is_active=True)
    except:
        pass

    if user is not None:
        password = data.get('password')
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            encrypted_token = encrypt_general_user_token(user)
            max_age = 86400*30
            response = Response({'status_code':200,'user_info':{'name':user.name,'email':user.email}})
            response.set_cookie(key='gn_ur_acs_tn', value=encrypted_token.decode(), httponly=True, secure=True, samesite='None',max_age=max_age)
            return response
        else:
            return Response({'status_code':400,'message':'Incorrect password'})
        

    else:
        return Response({'status_code':400,'message':'Invalid Email'})


@api_view(['POST'])
def forget_general_user_password(request):
    email = request.data.get('email')
    existing_user = None
    try:
        existing_user = GeneralUserAccount.objects.get(email = email,is_active=True)
    except:
        pass
    if existing_user is not None:
        otp = str(random.randint(0000, 9999)).zfill(4)
        existing_user.created_at = timezone.now()
        existing_user.save()
        otp_sent = send_otp_to_email(existing_user.email,otp)
        if otp_sent:
            token = encrypt_email_otp(existing_user,otp)
            response = Response({'status_code':200,'message':'An OTP has been sent to your email.'})
            response.set_cookie(
                key='gn_ur_frg_otp_tn',
                value=token.decode(),
                httponly=True,
                secure=True, 
                samesite='None',
                max_age=1*86400
            )
            return response
        else:
            return Response({'status_code':400,'message':'An unwanted error occured.Please try again'})
    else:
        return Response({'status_code':402,'message':'No active account found with this email'})


@api_view(['POST'])
def change_general_user_password(request):
    token =  request.COOKIES.get('cng_usr_pswrd')
    if token is not None:
        data = request.data
        required_values = decrypt_email_otp_token(token)
        existing_user = None
        try:
            existing_user =  GeneralUserAccount.objects.get(email = required_values['email'],is_active=True)
        except:
            pass
        if existing_user is not None:
            password = data.get('password')
            existing_user.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            existing_user.save()
            response = Response({'status_code':200,'message':'Password changed successfully'})
            response.set_cookie(
                key='cng_usr_pswrd',
                value='',
                httponly=True,
                secure=True, 
                samesite='None',
                max_age=0
            )
            return response
        else:
            return Response({'status_code':400,'message':'No active account found with this email'})
    
@api_view(['POST'])
def logout_general_user(request):
    response = Response({
        'status_code':200,
        'message': 'Logout successful'
    })
    response.delete_cookie('gn_ur_acs_tn')
    response.set_cookie(
                key='gn_ur_acs_tn',
                value="",
                httponly=True,
                secure=True, 
                samesite='None',
                max_age=0
            )
    return response

@api_view(['POST'])
def save_general_user_social_auth_info(request):
    data = request.data
    email = data.get('email')
    name = data.get('name')
    user = None
    try:
        user =  GeneralUserAccount.objects.get(email = email,is_active=True)
    except:
        pass
    if user:
        pass
    else:
        user = GeneralUserAccount(name=name,email=email,is_active=True)
        user.save()
    encrypted_token = encrypt_general_user_token(user)
    max_age = 86400*30
    response = Response({'status_code':200,'message':'Login Successfull'})
    response.set_cookie(key='gn_ur_acs_tn', value=encrypted_token.decode(), httponly=True, secure=True, samesite='None',max_age=max_age)
    return response



@api_view(['GET'])
def get_general_user_info(request):
    token =  request.COOKIES.get('gn_ur_acs_tn')
    info = None
    if token:
        info = decrypt_general_user_token(token)
        
    return Response({'status_code':200,'user_info':info})

# ****************************************************** GENERAL USER ENDS *************************************

# if existing_staff is not None:
#         password = data.get('password')
#         saved_password = existing_staff.password
#         if bcrypt.checkpw(password.encode('utf-8'), saved_password.encode('utf-8')):
#             encrypted_token = encrypt_staff_credentials(existing_staff.client.id,existing_staff.staff.id)
#             max_age = 86400*5
#             response = Response({'status_code':200,'message':'Login Successfull'})
#             response.set_cookie(key='staff_access_token', value=encrypted_token.decode(), httponly=True, secure=True, samesite='None',max_age=max_age)
#             return response
#         else:
#             return Response({'status_code':400,'message':'Incorrect Password'})


# ************************************************* Superuser Section Starts**************************************** 

@api_view(['POST'])
def login_super_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    existing_user = None
    try:
        existing_user = User.objects.get(username = username,is_superuser = True,is_active = True)
    except:
        pass
    if existing_user is not None:
        if check_password(password, existing_user.password):
            encrypted_token = encrypt_superuser_credentials(existing_user.id)
            max_age = 86400*5
            response = Response({'status_code':200,'username':existing_user.username,'role':'admin'})
            response.set_cookie(key='sp_acs_tkn', value=encrypted_token.decode(), httponly=True, secure=True, samesite='None',max_age=max_age)
            return response
        else:
            return Response({'status_code':200,'message':'Incorrect Password'})
    else:
        return Response({'status_code':200,'message':'Invalid Username'})


@api_view(['POST'])
def logout_super_user(request):
    response = Response({
        'status':200,
        'message': 'Logout successful'
    })
    response.delete_cookie('sp_acs_tkn')
    return response

@api_view(['GET'])
def get_superuser_info(request):
    encrypted_token =  request.COOKIES.get('sp_acs_tkn')
    user = get_superuser_obj(encrypted_token)
    return Response({'status_code':200,'name':user.first_name})


# ********************************************************* Superuser Section Ends ******************************************************


# ************************************************************ Client Section Starts*******************************************************
@api_view(['POST'])
def login_client(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    existing_user = None
    try:
        existing_user = User.objects.get(username = username,is_staff = True,is_active = True)
    except:
        pass
    if existing_user is not None:
        if check_password(password, existing_user.password):
            encrypted_token = encrypt_client_credentials(existing_user)
            max_age = 86400*8
            response = Response({'status_code':200,'message':'Login Successfull','company_name':existing_user.client_profile.company_name,'role':'owner'})
            response.set_cookie(key='clnt_acs_tkn', value=encrypted_token.decode(), httponly=True, secure=True, samesite='None',max_age=max_age)
            return response
        else:
            return Response({'status_code':400,'message':'Invalid Username or Password'})
    else:
        return Response({'status_code':400,'message':'No active account found'})
    
@api_view(['POST'])
def logout_client(request):
    response = Response({
        'status':200,
        'message': 'Logout successful'
    })
    response.delete_cookie('clnt_acs_tkn')
    return response


@api_view(['POST'])
def change_client_password(request):
    data = request.data
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    user = None
    try:
        user = User.objects.get(username = username,is_active=True,is_staff=True)
    except:
        pass
    if user is not None:
        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            return Response({'status_code':200,'message':'Password Changed Successfully'})
        else:
            return Response({'status_code':200,'message':'Invalid old password'})
    else:
        return Response({'status_code':400,'message':'Invalid username or old password'})

@api_view(['GET'])
def get_client_info(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    return Response({'status_code':200,'name':client.name})

# ***************************************************** CLient Section Ends ********************************************

# ***************************************************** Staff Section Starts **********************************************************
@api_view(['POST'])
def create_staff_account(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    if client is not None:
        if StaffAccount.objects.filter(client=client).count()+1 > client.staff_limit:
            return Response({'status_code':400,'message':'Staff account limit exceeded'})
        data = request.data
        username = data.get('username')
        staff_id = data.get('staff_id')
        existing_username = None
        existing_staff = None
        try:
            existing_username = StaffAccount.objects.get(username=username)
            existing_staff = StaffAccount.objects.get(staff_id = staff_id)
        except:
            pass
        if existing_username is None:
            if existing_staff is not None:
                return Response({'status_code':200,'message':'Staff account already exist'})
            password = data.get('password')
            # Hash the password and decode it to store as a string
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            staff_credentials = StaffAccount(client=client,staff_id = staff_id, username=username,password = hashed_password)
            staff_credentials.save()
            return Response({'status_code':200,'message':'Staff Account Created Successfully'})
        else:
            return Response({'status_code':400,'message':'This username is not available'})
    else:
        return Response({'status_code':400,'message':'Subscription Expired'})


@api_view(['POST'])
def login_staff(request):
    data = request.data
    username = data.get('username')
    existing_staff = None
    try:
        existing_staff = StaffAccount.objects.get(username=username,is_active=True)
    except:
        pass

    if existing_staff is not None:
        password = data.get('password')
        saved_password = existing_staff.password
        if bcrypt.checkpw(password.encode('utf-8'), saved_password.encode('utf-8')):
            encrypted_token = encrypt_staff_credentials(existing_staff.client.id,existing_staff.staff.id)
            max_age = 86400*5
            response = Response({'status_code':200,'message':'Login Successfull','name':existing_staff.staff.name,'role':'staff'})
            response.set_cookie(key='stf_acs_tkn', value=encrypted_token.decode(), httponly=True, secure=True, samesite='None',max_age=max_age)
            return response
        else:
            return Response({'status_code':400,'message':'Invalid Username or Password'})
    else:
        return Response({'status_code':400,'message':'No Active Account Found'})


@api_view(['POST'])
def logout_staff(request):
    response = Response({
            'status':200,
            'message': 'Logout successful'
        })
    response.delete_cookie('stf_acs_tkn')
    return response


@api_view(['GET'])
def get_staff_info(request):
    encrypted_token =  request.COOKIES.get('stf_acs_tkn')
    staff = get_staff_obj(encrypted_token)
    return Response({'status_code':200,'name':staff.name,'image_url':staff.image_url})

#is_staff,is_active ----------> Client 
#is_active ---------> staff
#is_superuser,is_staff,is_active ----------> admin
# ---------------------------------- ADMIN DAHSBOARD STARTS ------------------------------------------ #
@api_view(['POST'])
def change_client_active_status(request):
    encrypted_token =  request.COOKIES.get('sp_acs_tkn')
    superuser = get_superuser_obj(encrypted_token)
    if superuser:
        username = request.data.get('username')
        user = User.objects.get(username = username)
        client  = ClientProfile.objects.get(user=user)
        related_staff_accounts = StaffAccount.objects.filter(client=client)
        if user.is_active:
            user.is_active = False
            user.save()
            related_staff_accounts.update(is_active=False)
        else:
            user.is_active = True
            user.save()
            related_staff_accounts.update(is_active=True)
        return Response({'status_code':200,'message':'Status Changed Successfully'})
    else:
        return Response({'status_code':400,'message':'Access Denied'})


@api_view(['GET'])
def get_client_credentials_for_admin(request):
    encrypted_token =  request.COOKIES.get('sp_acs_tkn')
    superuser = get_superuser_obj(encrypted_token)
    if superuser:
        client_credentials = ClientProfile.objects.all().order_by('company_name')
        data = request.GET
        username = data.get('username')
        domain = data.get('domain')
        company_name = data.get('company_name')
        email = data.get('email')
        if username:
            client_credentials = client_credentials.filter(user__username__icontains = username)
        if domain:
            client_credentials = client_credentials.filter(domain__icontains = domain)
        if company_name:
            client_credentials = client_credentials.filter(company_name__icontains = company_name)
        if email:
            client_credentials = client_credentials.filter(email__icontains=email)
        serilizer = ClientCredentialSerializer(client_credentials,many=True)
        return Response({'status_code':200,'client_credentials':serilizer.data})
    else:
        return Response({'status_code':400,'message':'Access Denied'})
# ---------------------------------- ADMIN DASHBOARD ENDS -------------------------------------------- #