from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from ..booking.models import AppointmentRelatedServices
import random
import logging
logger = logging.getLogger(__name__)

def send_client_crdential_email(username,password,client):
    context = {
            'username':username,
            'password':password,
            'client':client,
        }
    html_content = render_to_string('client_credentials.html',context=context)
    text_content = strip_tags(html_content)
    subject="Welcome To Appointment Plugin"
    sender = settings.EMAIL_HOST_USER
    receiver = [client.email, ]
    # send email
    email = EmailMultiAlternatives(
        subject,
        text_content,
        sender,
        receiver,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return 'success'


def send_otp_to_email(email,otp):
    sending_status = False
    try:
        html_content = render_to_string('send_otp.html',context={'otp':otp})
        text_content = strip_tags(html_content)
        subject="!! Verify Your Email !!"
        sender = settings.EMAIL_HOST_USER
        receiver = [email, ]
        email = EmailMultiAlternatives(
            subject,
            text_content,
            sender,
            receiver,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        sending_status = True
    except:
        pass

    return sending_status


def send_appointment_email(booking_obj):
    appointment_services = AppointmentRelatedServices.objects.filter(appointment=booking_obj)
    context = {
        'booking_obj':booking_obj,
        'appointment_services':appointment_services
    }
    
    html_content = render_to_string('send_appointment_email.html',context=context)
    text_content = strip_tags(html_content)
    subject="Appointment Booking Summary"
    sender = settings.EMAIL_HOST_USER
    receiver = [booking_obj.email, ]
    # send email
    email = EmailMultiAlternatives(
        subject,
        text_content,
        sender,
        receiver,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return 'success'