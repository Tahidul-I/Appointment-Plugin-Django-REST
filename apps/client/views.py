from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from ..authentication.utils import get_client_obj,get_superuser_obj
from .serializers import *
from .utils import get_client
from ..staff.models import StaffProfile
from ..staff.serializers import StaffRecommendationSerializer

# Logically, this api is not needed
@api_view(['POST'])
def save_company_profile_info(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    client_info = None
    try:
        client_info = CompanyProfile.objects.get(client = client)
    except:
        pass
    if client_info is None:
        data = request.data
        name = data.get('name')
        address = data.get('address')
        logo = data.get('logo')
        description = data.get('description')
        CompanyProfile(
            client = client,
            name =name,
            address = address,
            logo = logo,
            description = description
        ).save()

        return Response({'status_code':200,'message':'Company Information Saved'})
    else:
        return Response({'status_code':400})


@api_view(['GET'])
def get_company_profile_info(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    profile_info = ClientProfile.objects.get(id = client.id)
    serializer = ClientProfileSerializerForClientDashboard(profile_info,many=False)
    return Response(serializer.data)


@api_view(['POST'])
def update_company_profile_info(request):
    encrypted_token =  request.COOKIES.get('clnt_acs_tkn')
    client = get_client_obj(encrypted_token)
    client_info = None
    try:
        client_info = ClientProfile.objects.get(id = client.id)
    except:
        pass
    if client_info is not None:
        data = request.data
        client_info.company_name = data.get('company_name')
        client_info.address = data.get('address')
        client_info.logo = data.get('logo')
        client_info.description = data.get('description')
        client_info.email = data.get('email')
        client_info.country = data.get('country')
        client_info.phone = data.get('phone')
        client_info.city = data.get('city')
        client_info.save()
        return Response({'status_code':200,'message':'Update Successful'})
    else:
        return Response({'status_code':400})
    
# ----------------------------------------- ADMIN SECTION STARTS ----------------------------------- #

@api_view(['GET'])
def get_registered_clients(request):
    encrypted_token =  request.COOKIES.get('sp_acs_tkn')
    superuser = get_superuser_obj(encrypted_token)
    if superuser:
        data = request.GET
        company_name = data.get('company_name')
        email = data.get('email')
        domain = data.get('domain')
        client_profiles = ClientProfile.objects.all().order_by('-created_at')
        if company_name:
            client_profiles = client_profiles.filter(company_name__icontains = company_name)
        if email:
            client_profiles = client_profiles.filter(email__icontains = email)
        if domain:
            client_profiles = client_profiles.filter(domain__icontains = domain)
        serializer = ClientProfileSerializerForAdminDashboard(client_profiles,many=True)
        return Response({'status_code':200,'profile_info':serializer.data})
    else:
        return Response({'status_code':400,'message':'Access Denied'})


@api_view(['GET'])
def get_company_profile_details(request):
    encrypted_token =  request.COOKIES.get('sp_acs_tkn')
    superuser = get_superuser_obj(encrypted_token)
    if superuser:
        profile_id = request.GET.get('profile_id')
        client_profile = ClientProfile.objects.get(id=profile_id)
        staffs = StaffProfile.objects.filter(client=client_profile)
        client_serializer = ClientDetailSerializerForAdminDashboard(client_profile,many=False)
        staff_serializer = StaffRecommendationSerializer(staffs,many=True)
        return Response({'status_code':200,'client_profile_details':client_serializer.data,'client_staff_details':staff_serializer.data})
    else:
        return Response({'status_code':400,'message':'Access Denied'})


# ----------------------------------------- ADMIN SECTION ENDS ------------------------------------- #