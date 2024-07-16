from django.core.mail import send_mail
import secrets


def send_email(subject, message, from_email, recipient_list):
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        auth_user='your_email@example.com',
        auth_password='your_email_password',
        fail_silently=False,
    )


def generate_confirmation_code():
    return secrets.token_urlsafe(16)