from django.urls import path
from . import views

urlpatterns = [
    path('v1/save-schedule-for-staff/',views.save_schedule_for_staff,name="save_schedule_for_staff"),
    path('v1/delete-staff-schedule/',views.delete_staff_schedule,name="delete_staff_schedule"),
    path('v1/get-staff-schedule/',views.get_staff_schedule,name="get_staff_schedule"),
    path('v1/remove-whole-month-staff-schedule/',views.remove_whole_month_staff_schedule,name="remove_whole_month_staff_schedule"),
    path('v1/get-time-slots/',views.get_time_slots,name="get_time_slots"),
    path('v1/set-time-on-hold/',views.set_time_on_hold,name="set_time_on_hold"),

]