from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..client.utils import get_client
from ..services.models import ClientServices
from .models import AppointmentBooking,AppointmentRelatedServices
from datetime import date,datetime,timedelta
from django.db.models import Sum
from ..payment_gateway.utils import *
from ..payment_gateway.models import *
from ..authentication.utils import get_client_obj,get_staff_obj
from .serializers import *
# Create your views here.
@api_view(['POST'])
def book_appointment(request):
    data = request.data
    unique_key = data.get('api_key')
    domain = data.get('domain')
    client = get_client(unique_key, domain)
    if client is not None:
        staff_id = data.get('staff_id')
        service_ids = data.get('service_ids')
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        appointment_note = data.get('appointment_note')
        duration = int(data.get('duration'))
        time_slot = data.get('time_slot')
        selected_date = data.get('selected_date')
        user_id = data.get('user_id')
        appointment_obj = AppointmentBooking(
            client = client,
            staff_id = staff_id,
            name = name,
            phone = phone,
            email=email,
            start_time_slot = datetime.strptime(time_slot, "%I:%M%p").time(),
            end_time_slot =  (datetime.strptime(time_slot, "%I:%M%p")+timedelta(minutes=duration)).time(),
            selected_date = selected_date,
            appointment_note = appointment_note,
            user_id = user_id,
            total_amount = ClientServices.objects.filter(id__in=service_ids).aggregate(Sum('new_price'))['new_price__sum']
        )
        appointment_obj.save()
        appointment_services = [AppointmentRelatedServices(appointment=appointment_obj,service_id=i) for i in service_ids]
        AppointmentRelatedServices.objects.bulk_create(appointment_services)
        if data.get('payment_mode') == 'paypal':
            credentials = PaypalPaymentGateway.objects.get(client_id = appointment_obj.client.id)
            payment_url = get_client_paypal_payment_url(credentials.paypal_credentials,appointment_obj)
            return Response({'status_code':200,'payment_url':payment_url})
        if data.get('payment_mode') == 'stripe':
            credentials = StripePaymentGateway.objects.get(client_id = appointment_obj.client.id)
            payment_url = get_client_stripe_payment_url(credentials.stripe_secret_key,appointment_obj)
            return Response({'status_code':200,'payment_url':payment_url})
        


@api_view(['GET'])
def get_all_bookings(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    data = request.GET
    client = get_client_obj(encrypted_token)
    
    if client is not None:
        staff_id = data.get('staff_id')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        customer_name = data.get('customer_name')
        customer_email = data.get('customer_email')
        bookings = AppointmentBooking.objects.filter(client=client,is_success=True).order_by('-selected_date')
        if staff_id:
            bookings = bookings.filter(staff_id=staff_id)
        # if start_date_str and end_date_str:
        #     start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        #     end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        #     bookings = bookings.filter(selected_date__range=(start_date, end_date))
        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            bookings = bookings.filter(selected_date__gte= start_date)
        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            bookings = bookings.filter(selected_date__lte= end_date)
        if customer_name:
            bookings = bookings.filter(name__icontains = customer_name)
        if customer_email:
            bookings = bookings.filter(email__icontains = customer_email)

        serializer = BookingSerializer(bookings,many=True)
        return Response({'status_code':200,'booking_data':serializer.data})
    else:
        return Response({'status_code':400,'message':'Access Denied'})


@api_view(['GET'])
def get_staff_bookings(request):
    encrypted_token = request.COOKIES.get('stf_acs_tkn')
    data = request.GET
    staff = get_staff_obj(encrypted_token)
    if staff:
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        customer_name = data.get('customer_name')
        customer_email = data.get('customer_email')
        bookings = AppointmentBooking.objects.filter(staff=staff,is_success=True).order_by('-selected_date')
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            bookings = bookings.filter(selected_date__range=(start_date, end_date))
        if customer_name:
            bookings = bookings.filter(name__icontains = customer_name)
        if customer_email:
            bookings = bookings.filter(email__icontains = customer_email)
        serializer = BookingSerializer(bookings,many=True)
        return Response({'status_code':200,'booking_data':serializer.data})
    else:
        return Response({'status_code':400,'message':'Access Denied'})



@api_view(['GET'])
def get_upcoming_ten_days_bookings_for_staff(request):
    encrypted_token = request.COOKIES.get('stf_acs_tkn')
    staff = get_staff_obj(encrypted_token)
    if staff:
        initial_date = date.today() +  timedelta(days=1)
        ten_days_later = initial_date + timedelta(days=10)
        bookings = AppointmentBooking.objects.filter(staff=staff,is_success=True,selected_date__range=(initial_date, ten_days_later)).order_by('-selected_date')
        serializer = BookingSerializer(bookings,many=True)
        return Response({'status_code':200,'booking_data':serializer.data})
    else:
        return Response({'status_code':400,'message':'Access Denied'})



@api_view(['GET'])
def get_archive_bookings(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    data = request.GET
    client = get_client_obj(encrypted_token)
    if client:
        # current date and time
        present_date = date.today()
        bookings = AppointmentBooking.objects.filter(client=client,is_success=True,selected_date__lt=present_date).order_by('-selected_date')
        staff_id = data.get('staff_id')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        customer_name = data.get('customer_name')
        customer_email = data.get('email')
        if staff_id:
            bookings = bookings.filter(staff_id=staff_id)
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            bookings = bookings.filter(created_at__date__range=(start_date, end_date))
        if customer_name:
            bookings = bookings.filter(name__icontains = customer_name)
        if customer_email:
            bookings = bookings.filter(email = customer_email)
        serializer = BookingSerializer(bookings,many=True)
        return Response({'status_code':200,'booking_data':serializer.data})
    else:
        return Response({'status_code':400,'message':'Access Denied'})


@api_view(['GET'])
def get_upcoming_ten_days_bookings(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    if client:
        initial_date = date.today() +  timedelta(days=1)
        ten_days_later = initial_date + timedelta(days=10)
        bookings = AppointmentBooking.objects.filter(client=client,is_success=True,selected_date__range=(initial_date, ten_days_later)).order_by('-selected_date')
        data = request.GET
        staff_id = data.get('staff_id')
        customer_name = data.get('customer_name')
        customer_email = data.get('customer_email')
        if staff_id:
            bookings = bookings.filter(staff_id=staff_id)
        if customer_name:
            bookings = bookings.filter(name__icontains = customer_name)
        if customer_email:
            bookings = bookings.filter(email = customer_email)

        serializer = BookingSerializer(bookings,many=True)
        return Response({'status_code':200,'booking_data':serializer.data})
    else:
        return Response({'status_code':400,'message':'Access Denied'})


@api_view(['GET'])
def get_abandoned_bookings(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    if client:
        bookings = AppointmentBooking.objects.filter(client=client,is_success=False).order_by('-selected_date')
        serializer = BookingSerializer(bookings,many=True)
        return Response({'status_code':200,'booking_data':serializer.data})
    else:
        return Response({'status_code':400,'message':'Access Denied'})


@api_view(['POST'])
def test_bookings(request):
    all_count = AppointmentBooking.objects.all().count()
    success_count = AppointmentBooking.objects.filter(is_success = True).count()
    return Response({'all_count':all_count,'success_count':success_count})


@api_view(['GET'])
def get_user_appointment_history(request):
    data = request.GET
    unique_key = data.get('api_key')
    domain = data.get('domain')
    client = get_client(unique_key, domain)
    if client:
        email = data.get('email')
        user_id = data.get('user_id')
        
        if email or user_id:
            appointment_history = None
            if email:
                appointment_history = AppointmentBooking.objects.filter(client = client,email=email,is_success=True)
            else:
                appointment_history = AppointmentBooking.objects.filter(client = client,user_id=user_id,is_success=True)
            serializer = UserBookingSerializer(appointment_history,many=True)
            return Response({'status_code':200,'user_appointment_history':serializer.data})
        else:
            return Response({'status_code':400,'message':'Query Parameters (user_id or email) are missing'})
    else:
        return Response({'status_code':401,'message':'Unauthorized.Api key and domain are incorrect or missing'})
        

@api_view(['GET'])
def get_booking_details(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    if client:
        booking_id = int(request.GET.get('booking_id'))
        booking_obj = AppointmentBooking.objects.get(id=booking_id,client = client,is_success=True)
        serializer = BookingSerializer(booking_obj,many=False)
        return Response({'status_code':200,'booking_details':serializer.data})
    else:
        return Response({'status_code':400,'message':'Access Denied'})
