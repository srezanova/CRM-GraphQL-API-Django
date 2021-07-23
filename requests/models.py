from django.db import models
from users.models import User
from config import settings

class Request(models.Model):
    created_at = models.DateField(auto_now_add=True)
    client = models.ForeignKey(User, related_name='client', null=True, on_delete=models.SET_NULL)
    employee = models.ForeignKey(User, related_name='employee', null=True, on_delete=models.SET_NULL)
    product = models.CharField(blank=False, max_length=200)

    CONSULTING = 'Consulting'
    DIAGNOSIS = 'Diagnosis'
    REPAIR = 'Repair'
    REPLACEMENT = 'Replacement'
    RETURN = 'Return'
    COMPLAINT = 'Complaint'
    OTHER = 'Other'
    CATEGORY_CHOICES = [
        (CONSULTING, 'Consulting'),
        (DIAGNOSIS, 'Diagnosis'),
        (REPAIR, 'Repair'),
        (REPLACEMENT, 'Replacement'),
        (RETURN, 'Return'),
        (COMPLAINT, 'Complaint'),
        (OTHER, 'Other'),
    ]

    OPEN = 'Open'
    SCHEDULED = 'Scheduled'
    CANCELED = 'Canceled'
    CLOSED = 'Closed'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (SCHEDULED, 'Scheduled'),
        (CANCELED, 'Canceled'),
        (CLOSED, 'Closed'),
    ]

    category = models.CharField(blank=True, choices=CATEGORY_CHOICES, max_length=15)
    status = models.CharField(blank=True, choices=STATUS_CHOICES, max_length=15)
    problem = models.CharField(blank=False, max_length=255)
    solution = models.CharField(blank=True, max_length=255)
    contacts = models.CharField(blank=True, max_length=255)
