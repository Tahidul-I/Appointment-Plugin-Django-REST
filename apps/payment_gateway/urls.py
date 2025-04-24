from django.urls import path
from . import views
urlpatterns = [
    path('v1/stripe-payment-success/',views.stripe_payment_success,name="stripe_payment_success"),
    path('v1/stripe-payment-cancel/',views.stripe_payment_cancel,name="stripe_payment_cancel"),
    path('v1/paypal-payment-success/',views.paypal_payment_success,name="paypal_payment_success"),
    path('v1/paypal-payment-cancel/',views.paypal_payment_cancel,name="paypal_payment_cancel"),
    path('v1/save-client-stripe-account-credentials/',views.save_client_stripe_account_credentials,name="save_client_stripe_account_credentials"),
    path('v1/save-client-paypal-account-credentials/',views.save_client_paypal_account_credentials,name="save_client_paypal_account_credentials"),
    path('v1/client-stripe-payment-success/',views.client_stripe_payment_success,name="client_stripe_payment_success"),
    path('v1/client-paypal-payment-success/',views.client_paypal_payment_success,name="client_paypal_payment_success"),
]
