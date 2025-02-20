# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from .models import Newsletter, Subscriber, EmailOpen, EmailClick
from .tasks import send_newsletter_email
from django.shortcuts import render, redirect
import datetime


def index(request):
    return render(request, "mailing/index.html")


def create_newsletter(request):
    subscribers = Subscriber.objects.all()  # Получаем подписчиков
    return render(request, 'mailing/create_newsletter.html', {'subscribers': subscribers})


@csrf_exempt
def create_newsletter(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        html_content = request.POST.get('html_content')
        scheduled_time_str = request.POST.get('scheduled_time')  # Формат: 'YYYY-MM-DD HH:MM:SS'
        scheduled_time = datetime.datetime.strptime(scheduled_time_str, '%Y-%m-%dT%H:%M')

        newsletter = Newsletter.objects.create(
            subject=subject,
            html_content=html_content,  # Используйте body или html_content в зависимости от вашей логики
            send_at=scheduled_time
        )

        # Получаем всех подписчиков
        subscribers = Subscriber.objects.all()

        # Планируем отправку писем с использованием Celery (отложенная отправка с помощью параметра eta)
        for subscriber in subscribers:
            send_newsletter_email.apply_async(args=[newsletter.id, subscriber.id], eta=scheduled_time)

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'POST required'})


def email_opened(request, newsletter_id, subscriber_id):
    """
    Отслеживаем открытие письма. Это представление вызывается, когда
    в письме загружается невидимый пиксель (1x1 gif).
    """
    try:
        subscriber = Subscriber.objects.get(id=subscriber_id)
        # Увеличиваем счетчик открытий
        subscriber.open_count += 1
        subscriber.save()
    except Subscriber.DoesNotExist:
        pass

    # Отдаем прозрачный 1x1 gif
    gif_data = b'GIF89a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00\xFF\xFF\xFF!' \
               b'\xF9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01' \
               b'\x00\x00\x02\x02L\x01\x00;'
    return HttpResponse(gif_data, content_type='image/gif')


def track_open(request, newsletter_id, subscriber_id):
    try:
        newsletter = Newsletter.objects.get(id=newsletter_id)
        subscriber = Subscriber.objects.get(id=subscriber_id)
        EmailOpen.objects.create(subscriber=subscriber, newsletter=newsletter)
    except (Newsletter.DoesNotExist, Subscriber.DoesNotExist):
        return HttpResponse(status=404)

    return HttpResponse(status=200)


def track_click(request, newsletter_id, subscriber_id):
    url = request.GET.get('url')
    try:
        newsletter = Newsletter.objects.get(id=newsletter_id)
        subscriber = Subscriber.objects.get(id=subscriber_id)
        EmailClick.objects.create(subscriber=subscriber, newsletter=newsletter, link_url=url)
    except (Newsletter.DoesNotExist, Subscriber.DoesNotExist):
        return HttpResponse(status=404)

    return redirect(url)