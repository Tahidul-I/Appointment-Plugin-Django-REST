from django.urls  import path
from . import views

urlpatterns = [
    path('v1/save-plugin-checkout-info/',views.save_plugin_checkout_info,name="save_plugin_checkout_info"),
    path('v1/get-orders/',views.get_orders,name="get_orders"),
    path('v1/get-order-details/',views.get_order_details,name="get_order_details"),
    path('v1/get-abandoned-orders/',views.get_abandoned_orders,name="get_abandoned_orders"),
]