import datetime

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from users.models import User


@shared_task
def send_mainling(course):
    emails = [subscribe.user.email for subscribe in course.subscribes.all()]
    if emails:
        subject = f'Обновление курса {course.title}'
        message = f'Курс {course.title} обновлен. Скорее посмотри обновления!'
        send_mail(subject=subject, message=message,
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=emails)


@shared_task
def check_activity():
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    for user in inactive_users:
        user.is_active = False
        user.save()
