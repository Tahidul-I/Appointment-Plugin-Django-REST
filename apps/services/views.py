from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from ..staff.models import StaffProfile
from ..staff.serializers import StaffRecommendationSerializer,StaffProfileSerializer
from ..authentication.utils import get_client_obj
from .serializers import *
from ..client.utils import get_client

@api_view(['POST'])
def save_company_services(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    data = request.data
    total_minutes = int(data.get('total_minutes'))
    hours, minutes = divmod(total_minutes, 60)
    formatted_duration = f"{hours} hr {minutes} min" if hours else f"{minutes} min"
    service = ClientServices(
                client = client,
                name = data.get('service_name'),
                description = data.get('description'),
                old_price = float(data.get('old_price')),
                new_price = float(data.get('new_price')),
                image_url = data.get('image_url'),
                duration = formatted_duration,
                total_minutes = total_minutes
            )
    service.save()
    return Response({'status_code':200,'message':'Service Added'})


@api_view(['POST'])
def add_service_related_staff(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    data = request.data
    service_id  = data.get('service_id')
    staff_ids = data.get('staff_ids')
    service = ClientServices.objects.get(client=client,id=service_id)
    service_related_staffs = [ ServiceRelatedStaff(service=service, staff_id=staff_id) for staff_id in staff_ids]
    ServiceRelatedStaff.objects.bulk_create(service_related_staffs)
    return Response({'status_code':200,'message':'Staff Added Successfully'})

@api_view(['GET'])
def get_all_services(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    all_services = ClientServices.objects.filter(client = client)
    serializer = ClientServicesSerializer(all_services,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_selected_service_details(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    service_id = request.GET.get('service_id')
    selected_service = ClientServices.objects.get(client = client, id = service_id)
    serializer = ClientServicesSerializer(selected_service,many=False)
    return Response(serializer.data)

@api_view(['GET'])
def get_service_related_staffs(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    service_id = request.GET.get('service_id')
    related_staff_ids = ServiceRelatedStaff.objects.filter(service__client=client, service_id=service_id).values_list('staff_id', flat=True)
    related_staffs = StaffProfile.objects.filter(id__in = related_staff_ids)
    serializer = StaffRecommendationSerializer(related_staffs,many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def update_service_details(request):
    data = request.data
    service_id = data.get('service_id')
    total_minutes = int(data.get('total_minutes'))
    hours, minutes = divmod(total_minutes, 60)
    formatted_duration = f"{hours} hr {minutes} min" if hours else f"{minutes} mins"
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    service = ClientServices.objects.get(client=client, id=service_id)
    service.name = data.get('name')
    service.description = data.get('description')
    service.old_price = float(data.get('old_price'))
    service.new_price = float(data.get('new_price'))
    service.image_url = data.get('image_url')
    service.duration = formatted_duration
    service.total_minutes = total_minutes
    service.save()
    return Response({'status_code':200,'message':'Update Successful'})


@api_view(['PUT'])
def update_service_related_staffs(request):
    data = request.data
    staff_ids = data.get('staff_ids')
    service_id = data.get('service_id')
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    service = ClientServices.objects.get(client = client, id = service_id)
    ServiceRelatedStaff.objects.filter(service = service).delete()
    service_related_staffs = [ ServiceRelatedStaff(service=service, staff_id=staff_id) for staff_id in staff_ids]
    ServiceRelatedStaff.objects.bulk_create(service_related_staffs)
    return Response({'status_code':200,'message':'Update Successfull'})

@api_view(['GET'])
def get_service_recommendation(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    service = ClientServices.objects.filter(client = client)
    serializer = ClientServicesSerializerForSelect(service,many=True)
    return Response(serializer.data)


# get client reated services for plugin interface

@api_view(['GET'])
def get_client_related_services(request):
    data = request.GET
    unique_key = data.get('api_key')
    domain = data.get('domain')
    client = get_client(unique_key,domain)
    if client is not None:
        services = ClientServices.objects.filter(client=client)
        serializer = ClientServicesSerializer(services,many=True)
        return Response(serializer.data)
    else:
        return Response({'status_code':400})

# get  staff information for plugin interface
    
# getting all staffs

@api_view(['GET'])
def get_all_staff_info(request):
    data = request.GET
    unique_key = data.get('api_key')
    domain = data.get('domain')
    client = get_client(unique_key,domain)
    if client is not None:
        staff_profiles = StaffProfile.objects.filter(client=client).prefetch_related('date_related_staff__date_related_time')
        serializer = StaffProfileSerializer(staff_profiles, many=True)
        return Response(serializer.data)
    else:
        return Response({'status_code':400})
    

@api_view(['GET'])
def get_service_related_staff_recommendation(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    service_id = request.GET.get('service_id')
    related_staff_ids = ServiceRelatedStaff.objects.filter(service__client=client, service_id=service_id).values_list('staff_id', flat=True)
    related_staffs = StaffProfile.objects.exclude(id__in = related_staff_ids)
    serializer = StaffRecommendationSerializer(related_staffs,many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_service_related_staff(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    data = request.GET
    service_id = data.get('service_id')
    staff_id = data.get('staff_id')
    ServiceRelatedStaff.objects.get(service_id=service_id,staff_id = staff_id, service__client=client).delete()
    return Response({'status_code':200,'message':'Staff Removed From Service'})


@api_view(['DELETE'])
def delete_service(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    service_id = request.GET.get('service_id')
    ClientServices.objects.get(client=client,id = service_id).delete()
    return Response({'status_code':200,'message':'Service Removed'})


@api_view(['GET'])
def get_your_services(request):
    data = request.GET
    unique_key = data.get('api_key')
    domain = data.get('domain')
    client = get_client(unique_key,domain)
    if client is not None:
        services = ClientServices.objects.filter(client=client)
        serializer = ClientServicesSerializer(services,many=True)
        return Response(serializer.data)
    else:
        return Response({'status_code':400})