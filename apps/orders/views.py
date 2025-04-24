from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..client.models import ClientProfile
from .models import *
from ..payment_gateway.utils import *
from ..authentication.utils import get_superuser_obj
from ..payment_gateway.utils import get_paypal_payment_url_for_purchasing_plugin,get_stripe_payment_url_for_purchasing_plugin
from .serializers import *
from datetime import datetime
# Create your views here.

@api_view(['POST'])
def save_plugin_checkout_info(request):
    data = request.data
    domain = data.get('domain')
    company_name = data.get('company_name')
    email = data.get('email')
    address = data.get('address')
    city = data.get('city')
    country = data.get('country')
    phone = data.get('phone')
    amount = float(data.get('amount'))
    order_obj = Order(company_name=company_name,domain=domain,email=email,address=address,city=city,country=country,phone=phone,total_amount=amount)
    order_obj.save()
    payment_url = None
    if data.get('payment_mode') == 'stripe':
        payment_url = get_stripe_payment_url_for_purchasing_plugin(order_obj)
    else:
        payment_url = get_paypal_payment_url_for_purchasing_plugin(order_obj)
    if payment_url:
        return Response({'status_code':200,'payment_url':payment_url})
    else:
        return Response({'status_code':400,'message':'Unwanted Error Occured. Please Try Again'})
    


# po0&^mI%
# sb-jozmy33129688@business.example.com


# ---------------------------------- ADMIN SECTION STARTS ---------------------------- #

@api_view(['GET'])
def get_orders(request):
    encrypted_token =  request.COOKIES.get('sp_acs_tkn')
    super_user = get_superuser_obj(encrypted_token)
    if super_user:
        data = request.GET
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        company_name = data.get('company_name')
        domain = data.get('domain')
        email = data.get('email')
        orders  = Order.objects.filter(is_successful=True).order_by('-created_at')
        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            orders = orders.filter(created_at__date__gte=start_date)
        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            orders = orders.filter(created_at__date__lte= end_date)
        if company_name:
            orders = orders.filter(company_name__icontains = company_name)
        if domain:
            orders = orders.filter(domain__icontains = domain)
        if email:
            orders = orders.filter(email__icontains = email)
        serializer = OrderSerializer(orders,many=True)
        return Response({'status_code':200,'orders':serializer.data})
    else:
        return Response({'status_code':400,'message':'Access Denied'})


@api_view(['GET'])
def get_order_details(request):
    encrypted_token =  request.COOKIES.get('sp_acs_tkn')
    super_user = get_superuser_obj(encrypted_token)
    if super_user:
        order_id = request.GET.get('order_id')
        order = Order.objects.get(id=order_id,is_successful=True)
        serializer = OrderDetailSerializer(order,many=False)
        return Response({'status_code':200,'order_details':serializer.data})
    else:
        return Response({'status_code':400,'message':'Access Denied'})


@api_view(['GET'])
def get_abandoned_orders(request):
    encrypted_token =  request.COOKIES.get('sp_acs_tkn')
    super_user = get_superuser_obj(encrypted_token)
    if super_user:
        data = request.GET
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        company_name = data.get('company_name')
        domain = data.get('domain')
        email = data.get('email')
        orders  = Order.objects.filter(is_successful=False).order_by('-created_at')
        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            orders = orders.filter(created_at__date__gte=start_date)
        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            orders = orders.filter(created_at__date__lte= end_date)
        if company_name:
            orders = orders.filter(company_name__icontains = company_name)
        if domain:
            orders = orders.filter(domain__icontains = domain)
        if email:
            orders = orders.filter(email__icontains = email)
        serializer = OrderSerializer(orders,many=True)
        return Response({'status_code':200,'orders':serializer.data})
    else:
        return Response({'status_code':400,'message':'Access Denied'})
# ---------------------------------- ADMIN SECTION ENDS -------------------------------#