from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import *
# Create your views here.
def home(request):
    return render(request,'home.html')

@api_view(['POST'])
def remove_browser_identifier_token(request):
    response = Response({"status_code":200})
    response.delete_cookie('br_idf_tn')
    return response


@api_view(['POST'])
def check_for_browser_identification_token(request):
    encrypted_browser_token = request.COOKIES.get('br_idf_tn')
    if encrypted_browser_token is not None:
        return Response({'status_code':200})
    else:
        response = Response({'status_code': 200})
        token = generate_random_token()
        encrypted_token = encrypt_browser_token(token)
        max_age = 86400 * 30
        response.set_cookie(
            key='br_idf_tn',
            value=encrypted_token.decode(),
            httponly=True,
            secure=True,
            samesite='None',
            max_age=max_age
        )
        return response