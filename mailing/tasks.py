# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import shared_task
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from .models import Newsletter, Subscriber
import datetime
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_newsletter_email(newsletter_id, subscriber_id):
    """ Отправляет email одному подписчику с HTML-шаблоном. """
    try:
        newsletter = Newsletter.objects.get(id=newsletter_id)
        subscriber = Subscriber.objects.get(id=subscriber_id)
    except (Newsletter.DoesNotExist, Subscriber.DoesNotExist):
        return "Ошибка: Рассылка или подписчик не найдены."

    # Персонализация письма
    greeting = "Доброе утро"  # Предустановленное приветствие
    if subscriber.birthday and subscriber.birthday.month == datetime.datetime.now().month and subscriber.birthday.day == datetime.datetime.now().day:
        greeting = "С днём рождения, {}!".format(subscriber.first_name or 'друг')

    context = {
        'subscriber': subscriber,
        'newsletter': newsletter,
        'greeting': greeting,
    }
    html_content = render_to_string('mailing/newsletter_email.html', context)

    subject = newsletter.subject
    from_email = 'noreply@example.com'
    to_email = [subscriber.email]

    msg = EmailMultiAlternatives(subject, '', from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return "Письмо отправлено {}".format(subscriber.email)


@shared_task
def send_newsletter(newsletter_id):
    """ Отправляет рассылку всем подписчикам. """
    try:
        newsletter = Newsletter.objects.get(id=newsletter_id)

        if not newsletter.subscribers.exists():
            return "Нет подписчиков для отправки."

        for subscriber in newsletter.subscribers.all():
            message_body = newsletter.body or ""
            formatted_body = message_body.format(
                first_name=subscriber.first_name or "",
                last_name=subscriber.last_name or "",
                birthday=subscriber.birthday or ""
            )

            try:
                send_mail(
                    subject=newsletter.subject,
                    message=formatted_body,
                    from_email="noreply@yourdomain.com",
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )
                logger.info("Рассылка '{}' отправлена {}.".format(newsletter.subject, subscriber.email))
            except Exception as e:
                logger.error("Ошибка при отправке письма {}: {}".format(subscriber.email, e))

        return "Рассылка '{}' отправлена {} подписчикам.".format(newsletter.subject, newsletter.subscribers.count())

    except Newsletter.DoesNotExist:
        return "Ошибка: Рассылка не найдена."


@shared_task
def check_scheduled_newsletters():
    """ Проверяет запланированные рассылки и запускает их отправку. """
    now = datetime.datetime.now()
    newsletters = Newsletter.objects.filter(scheduled_time__lte=now)

    for newsletter in newsletters:
        send_newsletter.delay(newsletter.id)