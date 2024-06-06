from django.core.mail import send_mail, send_mass_mail
from .models import Newsletter, User


def send_confirmation_code(email, code):
    subject = 'Код подтверждения'
    message = f'Ваш код подтверждения: {code}'
    from_email = 'k030kp@bk.ru'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def send_newsletters():
    newsletters = Newsletter.objects.all()
    users = User.objects.all()
    messages = []
    for newsletter in newsletters:
        for user in users:
            message = (newsletter.subject, newsletter.message, 'from@example.com', [user.email])
            messages.append(message)
    send_mass_mail(messages)