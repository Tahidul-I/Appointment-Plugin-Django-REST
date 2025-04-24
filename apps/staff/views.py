from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..authentication.utils import get_client_obj
from .models import *
from .serializers import *
from ..client.utils import get_client
from ..schedule.models import *
from ..schedule.serializers import *
from ..schedule.utils import *
from ..services.models import ServiceRelatedStaff
from django.db.models import Count, Q
from ..core.utils import *
from datetime import timedelta,datetime
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)

@api_view(['POST'])  # In use
def save_staff_profile(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    if StaffProfile.objects.filter(client=client).count()+1 > client.staff_limit:
        return Response({'status_code':400,'message':'Staff account limit exceeded'})
    data = request.data
    name = data.get('name')
    description = data.get('description')
    image_url = data.get('image_url')
    StaffProfile(
        client = client,
        name = name,
        description = description,
        image_url = image_url
    ).save()

    return Response({'status_code':200,'message':'Staff Information Saved'})

@api_view(['GET'])
def get_all_staff_info(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    all_staffs = StaffProfile.objects.filter(client=client)
    serializer = StaffProfileSerializer(all_staffs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_selected_staff_info(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    staff_id = int(request.GET.get('staff_id'))
    selected_staff = StaffProfile.objects.get(client=client,id=staff_id)
    serializer = StaffProfileSerializer(selected_staff, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def get_staff_recommendation(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    all_staffs = StaffProfile.objects.filter(client=client)
    serializer = StaffRecommendationSerializer(all_staffs,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def update_staff_profile(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    data = request.data
    staff_id = data.get('staff_id')
    staff = None
    try:
        staff = StaffProfile.objects.get(client=client,id=staff_id)
    except:
        pass
    if staff is not None:
        staff.name = data.get('name')
        staff.description = data.get('description')
        staff.image_url = data.get('image_url')
        staff.save()
        return Response({'status_code':200,'message':'Update Successful'})
    else:
        return Response({'status_code':400})        

# For Plugin  UI. to be modified, have to collect  the service ids also

@api_view(['GET'])
def get_all_staff_informations_for_plugin(request):
    data = request.GET
    unique_key = data.get('api_key')
    domain = data.get('domain')
    client = get_client(unique_key,domain)
    if client is not None:
        staffs = StaffProfile.objects.filter(client=client)
        staff_serializer = StaffProfileSerializer(staffs,many=True)
        return Response(staff_serializer.data)
    else:
        return Response({'status_code':400})


@api_view(['DELETE'])
def delete_staff(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    staff_id = request.GET.get('staff_id')
    StaffProfile.objects.get(client=client,id=staff_id).delete()
    return Response({'status_code':200,'message':'Staff Deleted'})

@api_view(['GET'])
def get_selected_staff_info_for_plugin(request):
    data = request.GET
    unique_key = data.get('api_key')
    domain = data.get('domain')
    staff_id = data.get('staff_id')
    client = get_client(unique_key,domain)
    if client is not None:
        ten_minutes_ago = timezone.now() - timedelta(minutes=2)
        staff_profile = StaffProfile.objects.get(client=client,id=staff_id)
        BaseTimeSlot.objects.filter(client=client,staff_id=staff_id,created_at__lte=ten_minutes_ago).delete()
        staff_info_serializer = StaffProfileSerializer(staff_profile, many=False)
        staff_schedule = StaffSchedule.objects.filter(client = client,staff_id = staff_id).values_list('scheduled_date',flat=True)
        # staff_schedule_serializer = SelectedStaffScheduleSerializer(staff_schedule,many=True)
        return Response({'status_code':200,'staff_info':staff_info_serializer.data,'staff_schedule':staff_schedule})   
    else:
        return Response({'status_code':400})

# In Use on Plugin
@api_view(['POST'])
def get_available_staffs_for_selected_service(request):
    data = request.data
    unique_key = data.get('api_key')
    domain = data.get('domain')
    client = get_client(unique_key,domain)
    service_ids = data.get('service_ids')
    staff_queryset = ServiceRelatedStaff.objects.filter(
    service__client = client,service_id__in=service_ids
    ).values('staff').annotate(
        service_count=Count('service', filter=Q(service_id__in=service_ids), distinct=True)
    ).filter(
        service_count=len(service_ids)
    )
    staff_profiles = StaffProfile.objects.filter(id__in=[staff['staff'] for staff in staff_queryset])
    serializer = StaffRecommendationSerializer(staff_profiles,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_staffs_for_selected_service(request):
    data = request.data
    unique_key = data.get('api_key')
    domain = data.get('domain')
    client = get_client(unique_key,domain)
    service_ids = data.get('service_ids')
    staff_queryset = ServiceRelatedStaff.objects.filter(
    service__client = client,service_id__in=service_ids
    ).values('staff').annotate(
        service_count=Count('service', filter=Q(service_id__in=service_ids), distinct=True)
    ).filter(
        service_count=len(service_ids)
    )
    staff_profiles = StaffProfile.objects.filter(id__in=[staff['staff'] for staff in staff_queryset])
    serializer = StaffRecommendationSerializer(staff_profiles,many=True)
    return Response(serializer.data)
