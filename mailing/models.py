# -*- coding: utf-8 -*-
from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    birthday = models.DateField(null=True, blank=True)
    # Для отслеживания открытий письма
    open_count = models.IntegerField(default=0)

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    html_content = models.TextField(blank=True, null=True)
    subscribers = models.ManyToManyField(Subscriber)  # Добавили список подписчиков
    send_at = models.DateTimeField()

    def __str__(self):
        return self.subject


class EmailOpen(models.Model):
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE)
    newsletter = models.ForeignKey('Newsletter', on_delete=models.CASCADE)
    opened_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} opened {} at {}".format(self.subscriber.email, self.newsletter.subject, self.opened_at)


class EmailClick(models.Model):
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE)
    newsletter = models.ForeignKey('Newsletter', on_delete=models.CASCADE)
    clicked_at = models.DateTimeField(auto_now_add=True)
    link_url = models.URLField()

    def __str__(self):
        return "{} clicked {} in {} at {}".format(self.subscriber.email, self.link_url, self.newsletter.subject, self.clicked_at)