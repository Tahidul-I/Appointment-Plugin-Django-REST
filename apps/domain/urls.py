from django.urls import path
from . import views

urlpatterns = [
    path('v1/check-domain/',views.check_domain,name="check_domain")
]
