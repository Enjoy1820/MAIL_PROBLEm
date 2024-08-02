import datetime

from django.conf import settings
from django.core.exceptions import ValidationError

from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers, EmailMultiAlternatives
from .models import PostCategory, Post
from django.template.loader import render_to_string


def send_notifications(preview, pk, header, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=header,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.header, subscribers_emails)
