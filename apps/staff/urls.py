from django.urls import path
from . import views

urlpatterns = [
    path('v1/save-staff-profile/',views.save_staff_profile,name="save_staff_profile"),
    path('v1/get-staff-recommendation/',views.get_staff_recommendation,name="get_staff_recommendation"),
    path('v1/get-all-staff-info/',views.get_all_staff_info,name="get_all_staff_info"),
    path('v1/get-selected-staff-info/',views.get_selected_staff_info,name="get_selected_staff_info"),
    path('v1/update-staff-profile/',views.update_staff_profile,name="update_staff_profile"),
    path('v1/delete-staff/',views.delete_staff,name="delete_staff"),
    path('v1/get-all-staff-informations-for-plugin/',views.get_all_staff_informations_for_plugin,name="get_all_staff_informations_for_plugin"),
    path('v1/get-available-staffs-for-selected-service/',views.get_available_staffs_for_selected_service,name="get_available_staffs_for_selected_service"),
    path('v1/get-selected-staff-info-for-plugin/',views.get_selected_staff_info_for_plugin,name="get_selected_staff_info_for_plugin"),
    
]
