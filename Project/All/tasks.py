import datetime

from celery import shared_task
from django.core.mail import send_mail

from .models import Advertisement, Subscription


@shared_task
def send_notification_to_subscribers(article_id):
    article = Advertisement.objects.get(id=article_id)
    Subscription = article.subscribers.all()
    subject = f'Привет, у нас свежие новости: {article.title}'
    message = f'{article.body[:100]}'
    send_mail(
        subject=subject,
        message=message,
        from_email='news@example.com',
        recipient_list=[subscriber.email for subscriber in Subscription],
        fail_silently=False,
    )


@shared_task
def send_weekly_newsletter():
    this_monday = datetime.date.today() + datetime.timedelta(days=1)
    last_monday = this_monday - datetime.timedelta(days=7)
    articles = Advertisement.objects.filter(created_at__range=[last_monday, this_monday])
    Subscription = Subscriber.objects.all()
    subject = 'Недельный обзор новостей, взгляни может что пропустил'
    message = '\n\n'.join([f'{article.title}\n{article.body[:100]}\n' for article in articles])
    send_mail(
        subject=subject,
        message=message,
        from_email='news@example.com',
        recipient_list=[subscriber.email for subscriber in Subscription],
        fail_silently=False,
    )
