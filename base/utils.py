import random
import string
from datetime import timedelta
from .models import CustomUser
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils import timezone


def superuser_required(function):
    return user_passes_test(lambda u: u.is_superuser, login_url='login')(function)


def generate_verification_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

def send_verification_email(user):
    token = generate_verification_token()
    user.verification_token = token
    user.token_created_at = timezone.now()
    user.save()

    subject = 'Verify your email'
    base_url = "http://127.0.0.1:8000/"
    verification_url = base_url + reverse('verify_email', kwargs={'token': token})
    message = f'Hello {user.name},\n\nPlease click the link below to verify your email address:\n\n{verification_url}\n\nThank you!'
    from_email = f"EC <{settings.EMAIL_HOST_USER}>"
    send_mail(
        subject,
        message,
        from_email,
        [user.email],
        fail_silently=False,
    )

def verify_email(token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        if user.token_created_at and timezone.now() > user.token_created_at + timedelta(minutes=10):
            user.verification_token = None
            user.token_created_at = None
            user.save()
            return None
        user.email_verified = True
        user.verification_token = None
        user.token_created_at = None
        user.save()
        return user
    except CustomUser.DoesNotExist:
        return None


def send_welcome_email(user):
    subject = "Welcome to EC!"
    message = f"Dear {user.name},\n\nCongratulations! Your account is now active.\n\nWe are glad you are here."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)

