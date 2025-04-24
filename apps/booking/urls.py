from django.urls import path
from . import views

urlpatterns = [
    path('v1/book-appointment/',views.book_appointment,name="book_appointment"),
    path('v1/get-all-bookings/',views.get_all_bookings,name="get_all_bookings"),
    path('v1/get-abandoned-bookings/',views.get_abandoned_bookings,name="get_abandoned_bookings"),
    path('v1/get-upcoming-ten-days-bookings/',views.get_upcoming_ten_days_bookings,name="get_upcoming_ten_days_bookings"),
    path('v1/get-archive-bookings/',views.get_archive_bookings,name="get_archive_bookings"),
    path('v1/get-staff-bookings/',views.get_staff_bookings,name="get_staff_bookings"),
    path('v1/get-upcoming-ten-days-bookings-for-staff/',views.get_upcoming_ten_days_bookings_for_staff,name="get_upcoming_ten_days_bookings_for_staff"),
    path('v1/get-user-appointment-history/',views.get_user_appointment_history,name="get_user_appointment_history"),
    path('v1/get-booking-details/',views.get_booking_details,name="get_booking_details"),
    path('v1/test-bookings/',views.test_bookings,name="test_bookings"),
]
