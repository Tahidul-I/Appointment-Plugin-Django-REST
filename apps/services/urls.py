from django.urls import path
from . import views

urlpatterns = [
    path('v1/save-company-services/',views.save_company_services,name="save_company_services"),
    path('v1/get-all-services/',views.get_all_services,name="get_all_services"),
    path('v1/get-service-related-staffs/',views.get_service_related_staffs,name="get_service_related_staffs"),
    path('v1/get-selected-service-details/',views.get_selected_service_details,name="get_selected_service_details"),
    path('v1/update-service-details/',views.update_service_details,name="update_service_details"),
    path('v1/get-client-related-services/',views.get_client_related_services,name="get_client_related_services"),
    path('v1/get-service-recommendation/',views.get_service_recommendation,name="get_service_recommendation"),
    path('v1/add-service-related-staff/',views.add_service_related_staff,name="add_service_related_staff"),
    path('v1/get-service-related-staff-recommendation/',views.get_service_related_staff_recommendation,name="get_service_related_staff_recommendation"),
    path('v1/delete-service-related-staff/',views.delete_service_related_staff,name="delete_service_related_staff"),
    path('v1/delete-service/',views.delete_service,name="delete_service"),
    path('v1/get-your-services/',views.get_your_services,name="get_your_services"),
]
