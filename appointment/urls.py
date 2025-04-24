from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include("apps.payment_gateway.urls")),
    path('api/',include("apps.client.urls")),
    path('api/',include("apps.staff.urls")),
    path('api/',include("apps.services.urls")),
    path('api/',include("apps.schedule.urls")),
    path('api/',include("apps.authentication.urls")),
    path('api/',include("apps.domain.urls")),
    path('api/',include("apps.booking.urls")),
    path('api/',include("apps.booking.urls")),
    path('api/',include("apps.orders.urls")),
    path('api/',include("apps.auth_service.urls")),
    path('',include("apps.core.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)