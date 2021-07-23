from django.db import models
from users.models import User


class Client(models.Model):
    phone = models.CharField(null=True, blank=False,
                             unique=True, max_length=20)
    first_name = models.CharField(null=True, blank=True, max_length=20)
    last_name = models.CharField(null=True, blank=True, max_length=20)


class Request(models.Model):
    created_at = models.DateField(auto_now_add=True)
    employee = models.ForeignKey(
        User, related_name='employee', blank=True, null=True, on_delete=models.SET_NULL)

    CONSULTING = 'CONSULTING'
    DIAGNOSIS = 'DIAGNOSIS'
    REPAIR = 'REPAIR'
    REPLACEMENT = 'REPLACEMENT'
    RETURN = 'RETURN'
    CATEGORY_CHOICES = [
        (CONSULTING, 'CONSULTING'),
        (DIAGNOSIS, 'DIAGNOSIS'),
        (REPAIR, 'REPAIR'),
        (REPLACEMENT, 'REPLACEMENT'),
        (RETURN, 'RETURN'),
    ]

    ACCEPTED = 'ACCEPTED'
    IN_PROCCESS = 'IN_PROCCESS'
    READY = 'READY'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = [
        (ACCEPTED, 'ACCEPTED'),
        (IN_PROCCESS, 'IN_PROCCESS'),
        (READY, 'READY'),
        (CLOSED, 'CLOSED'),
    ]

    category = models.CharField(
        blank=True, choices=CATEGORY_CHOICES, max_length=15, null=True)
    status = models.CharField(
        blank=True, choices=STATUS_CHOICES, max_length=15, null=True)
    description = models.TextField(blank=True, null=True)
    client = models.ForeignKey(
        Client, related_name='client', blank=True, null=True, on_delete=models.SET_NULL)
