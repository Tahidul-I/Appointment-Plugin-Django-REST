
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..client.models import ClientProfile
from .utils import check_domain_validity
# Create your views here.
@api_view(['POST'])
def check_domain(request):
    domain = request.data.get('domain')
    is_valid = check_domain_validity(domain)
    if is_valid == True:
        existing_client = None
        try:
            existing_client = ClientProfile.objects.get(domain=domain)
        except:
            pass
        if existing_client is None:
            return Response({'status_code':200})
        else:
            return Response({'status_code':200,'message':'Your domain is already registered'})
    else:
        return Response({'status_code':400,'message':'The domain is invalid'})