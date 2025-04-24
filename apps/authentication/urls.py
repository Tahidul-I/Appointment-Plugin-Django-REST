from django.urls import path
from . import views

urlpatterns = [
    path('v1/change-client-password/',views.change_client_password,name="change_client_password"),
    path('v1/login-client/',views.login_client,name="login_client"),
    path('v1/login-super-user/',views.login_super_user,name="login_super_user"),
    path('v1/get-client-info/',views.get_client_info,name="get_client_info"),
    path('v1/create-staff-account/',views.create_staff_account,name="create_staff_account"),
    path('v1/login-staff/',views.login_staff,name="login_staff"),
    path('v1/get-staff-info/',views.get_staff_info,name="get_staff_info"),
    path('v1/get-plugin-url/',views.get_plugin_url,name="get_plugin_url"),
    path('v1/create-general-user-account/',views.create_general_user_account,name="create_general_user_account"),
    path('v1/verify-general-user-email/',views.verify_general_user_email,name="verify_general_user_email"),
    path('v1/resend-general-user-otp/',views.resend_general_user_otp,name="resend_general_user_otp"),
    path('v1/login-general-user/',views.login_general_user,name="login_general_user"),
    path('v1/forget-general-user-password/',views.forget_general_user_password,name="forget_general_user_password"),
    path('v1/change-general-user-password/',views.change_general_user_password,name="change_general_user_password"),
    path('v1/logout-general-user/',views.logout_general_user,name="logout_general_user"),
    path('v1/get-general-user-info/',views.get_general_user_info,name="get_general_user_info"),
    path('v1/save-general-user-social-auth-info/',views.save_general_user_social_auth_info,name="save_general_user_social_auth_info"),
    path('v1/get-client-credentials-for-admin/',views.get_client_credentials_for_admin,name="get_client_credentials_for_admin"),
    path('v1/change-client-active-status/',views.change_client_active_status,name="change_client_active_status"),
]