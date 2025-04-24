from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..authentication.utils import get_client_obj
from .serializers import *
from .models import *
from ..client.utils import get_client
import logging
from django.utils import timezone
logger = logging.getLogger(__name__)
from ..core.utils import decrypt_browser_token
from datetime import timedelta,datetime
from .utils import *

@api_view(['POST', 'PUT'])
def save_schedule_for_staff(request):
    data = request.data
    staff_id = data.get('staff_id')
    encrypted_token = request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    schedule = data.get('schedule')

    responses = []
    shift_start_time_str, shift_end_time_str = schedule['time']['shift'].split('-')
    break_start_time_str, break_shift_end_time_str = schedule['time']['break_period'].split('-')
    if break_start_time_str == "00:00AM" and break_shift_end_time_str == "00:00AM":
            break_time_starts = None
            break_time_ends = None
    else:
        break_time_starts = datetime.strptime(break_start_time_str, '%I:%M%p').time()
        break_time_ends = datetime.strptime(break_shift_end_time_str, '%I:%M%p').time()
    for date_schedule in schedule['date']:
        # Extract start and end times for the break period

        # Set break times based on condition
        

        # Use update_or_create to handle both create and update
        existing_schedule, created = StaffSchedule.objects.update_or_create(
            client=client,
            staff_id=staff_id,
            scheduled_date=date_schedule,
            defaults={
                'shift_starts': datetime.strptime(shift_start_time_str, '%I:%M%p').time(),
                'shift_ends': datetime.strptime(shift_end_time_str, '%I:%M%p').time(),
                'break_time_starts': break_time_starts,
                'break_time_ends': break_time_ends,
            }
        )

        # Append response message
        if created:
            responses.append({'status_code':200,'message': 'Schedule Saved'})
        else:
            responses.append({'status_code':200,'message': 'Schedule Updated'})

    return Response({'status_code': 200, 'messages': responses})

    
@api_view(['DELETE']) # In use From Dashboard
def delete_staff_schedule(request): 
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    if client is not None:
        data = request.GET
        schedule_id = data.get('schedule_id')
        StaffSchedule.objects.get(id=schedule_id).delete()
        return Response({'status_code':200,'message':'Schedule Removed'})
    else:
        return Response({'message':'Access Denied'})


@api_view(['GET']) # In use From Dashboard
def get_staff_schedule(request):
    data = request.GET
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    if client is not None:
        staff_id = data.get('staff_id')
        date_string = data.get('date')
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        # Filter StaffSchedule objects by year and month
        schedule = StaffSchedule.objects.filter(client=client,staff_id=staff_id,scheduled_date__year=date_obj.year, scheduled_date__month=date_obj.month)
        serializer = StaffScheduleSerializer(schedule,many=True)
        return Response({'status_code':200,'schedule':serializer.data})
    else:
        return Response({'status_code':400,'message':'Who Are You ?'})



# from dashboard
@api_view(['DELETE']) # In Use
def remove_whole_month_staff_schedule(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    data = request.GET
    staff_id = data.get('staff_id')
    date_string = data.get('date')
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    # Extract year and month
    year = date_obj.year
    month = date_obj.month
    # Filter StaffSchedule objects by year and month
    StaffSchedule.objects.filter(client=client,staff_id=staff_id,scheduled_date__year=year, scheduled_date__month=month).delete()
    return Response({'status_code':200,'message':'Monthly Schedule Removed'})

# 10:10   now 10:25, 10:25-10mins = 10:15
# 10:10   now 10:20, 10:20-10mins = 10:10



# To be used originally
@api_view(['GET'])
def get_time_slots(request):
    ten_minutes_ago = timezone.now() - timedelta(minutes=2)
    data = request.GET
    unique_key = data.get('api_key')
    domain = data.get('domain')
    client = get_client(unique_key, domain)
    if client is None:
        return Response({'status_code': 403, 'message': 'Access Denied'})
    duration = int(data.get('duration'))
    staff_id = data.get('staff_id')
    date_string = data.get('date')
    BaseTimeSlot.objects.filter(client=client,staff_id=staff_id,created_at__lte=ten_minutes_ago).delete()
    existing_base_time = None
    schedule_obj = StaffSchedule.objects.get(client=client,staff_id=staff_id,scheduled_date=date_string)
    try:
        existing_base_time = BaseTimeSlot.objects.get(client=client,staff_id=staff_id,date_str=date_string)
    except:
        pass
    if existing_base_time is None:
        time_slots = generate_time_slots(schedule_obj.shift_starts,schedule_obj.shift_ends,schedule_obj.break_time_starts,schedule_obj.break_time_ends,duration,schedule_obj.scheduled_date)
        return Response({'status_code':200,'time_slots':time_slots})
    else:
        start_time = datetime.combine(datetime.today(), existing_base_time.start)+timedelta(minutes=existing_base_time.duration+10)
        time_slots = generate_time_slots(start_time.time(),schedule_obj.shift_ends,schedule_obj.break_time_starts,schedule_obj.break_time_ends,duration,schedule_obj.scheduled_date)
    
    return Response({'status_code':200,'time_slots':time_slots}) 


@api_view(['POST'])
def set_time_on_hold(request):
    ten_minutes_ago = timezone.now() - timedelta(minutes=2)
    data = request.data
    unique_key = data.get('api_key')
    domain = data.get('domain')
    client = get_client(unique_key, domain)
    logger.warning("*********************************** TIME HOLD **********************************************")
    logger.warning(unique_key)
    if client is None:
        return Response({'status_code': 403, 'message': 'Access Denied'})
    duration = int(data.get('duration'))
    staff_id = data.get('staff_id')
    date_string = data.get('date')
    selected_time_slot_24hr = datetime.strptime(data.get('selected_time'), "%I:%M%p").time()
    # OnHoldTimeSlots.objects.filter(client=client,staff=staff_id,date_schedule=date_string,created_at__lte=ten_minutes_ago).delete()
    BaseTimeSlot.objects.filter(client=client,staff_id=staff_id,created_at__lte=ten_minutes_ago).delete()
    # encrypted_browser_token = request.COOKIES.get('br_idf_tn')
    # decrypted_browser_token = decrypt_browser_token(encrypted_browser_token)
    existing_base_time = None
    try:
        existing_base_time = BaseTimeSlot.objects.get(client=client,staff_id=staff_id,date_str=date_string)
    except:
        pass
    if existing_base_time is None:
        BaseTimeSlot(
            client = client,
            staff_id = staff_id,
            date_str = datetime.strptime(date_string, "%Y-%m-%d").date(),
            start = selected_time_slot_24hr,
            duration = duration,
            created_at = timezone.now()
        ).save()

        return Response({'status_code':200})
    else:
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
        if datetime.combine(date_object, selected_time_slot_24hr)<datetime.combine(date_object, existing_base_time.start):
            if datetime.combine(date_object, selected_time_slot_24hr)+timedelta(minutes=(duration+10))<=datetime.combine(date_object, existing_base_time.start):
                return Response({'status_code':200})
            else:
                return Response({'status_code':400,'message':'This time slot is no longer available'})
        elif datetime.combine(date_object, selected_time_slot_24hr)>datetime.combine(date_object, existing_base_time.end):
            return Response({'status_code':200})
        else:
            return Response({'status_code':400,'message':'This time slot is no longer available'})