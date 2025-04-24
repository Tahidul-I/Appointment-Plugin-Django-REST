from django.urls import path
from . import views

urlpatterns = [
    path('v1/get-company-profile-info/',views.get_company_profile_info,name="get_company_profile_info"),
    path('v1/save-company-profile-info/',views.save_company_profile_info,name="save_company_profile_info"),
    path('v1/update-company-profile-info/',views.update_company_profile_info,name="update_company_profile_info"),
    path('v1/get-registered-clients/',views.get_registered_clients,name="get_registered_clients"),
    path('v1/get-company-profile-details/',views.get_company_profile_details,name="get_company_profile_details"),
]
