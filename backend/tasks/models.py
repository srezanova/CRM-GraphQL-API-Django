from django.db import models
from telegram import message
from users.models import User


class Customer(models.Model):
    telegram_id = models.PositiveIntegerField(
        verbose_name='Telegram ID',
        unique=True,
        blank=True,
        null=True,
    )
    phone = models.CharField(null=True, blank=False,
                             unique=True, max_length=20)
    name = models.CharField(null=True, blank=True, max_length=20)


class Task(models.Model):
    created_at = models.DateField(auto_now_add=True)
    employee = models.ForeignKey(
        User, related_name='tasks', blank=True, null=True, on_delete=models.SET_NULL)

    CONSULTING = 'CONSULTING'
    DIAGNOSIS = 'DIAGNOSIS'
    REPAIR = 'REPAIR'
    OTHER = 'OTHER'
    CATEGORY_CHOICES = [
        (CONSULTING, 'CONSULTING'),
        (DIAGNOSIS, 'DIAGNOSIS'),
        (REPAIR, 'REPAIR'),
        (OTHER, 'OTHER'),
    ]

    ACCEPTED = 'ACCEPTED'
    IN_PROGRESS = 'IN_PROGRESS'
    READY = 'READY'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = [
        (ACCEPTED, 'ACCEPTED'),
        (IN_PROGRESS, 'IN_PROGRESS'),
        (READY, 'READY'),
        (CLOSED, 'CLOSED'),
    ]

    category = models.CharField(
        blank=True, choices=CATEGORY_CHOICES, max_length=15, null=True)
    status = models.CharField(
        blank=True, choices=STATUS_CHOICES, max_length=15, null=True)
    description = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(
        Customer, related_name='tasks', blank=True, null=True, on_delete=models.SET_NULL)
