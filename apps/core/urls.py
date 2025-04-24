from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('api/v1/check-for-browser-identification-token/',views.check_for_browser_identification_token,name="check_for_browser_identification_token"),
]
