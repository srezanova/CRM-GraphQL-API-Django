from django.db import models


class Request(models.Model):
    created_at = models.DateField(auto_now_add = True)
    #client
    #employee

    CONSULTING = 'CNSL'
    DIAGNOSIS = 'DGNS'
    REPAIR = 'REPA'
    REPLACEMENT = 'RPLC'
    RETURN = 'RTRN'
    COMPLAINT = 'CMPL'
    OTHER = 'OTHER'
    CATEGORY_CHOICES = [
        (CONSULTING, 'Consulting'),
        (DIAGNOSIS, 'Diagnosis'),
        (REPAIR, 'Repair'),
        (REPLACEMENT, 'Replacement'),
        (RETURN, 'Return'),
        (COMPLAINT, 'Complaint'),
        (OTHER, 'Other'),
    ]

    OPEN = 'OPEN'
    SCHEDULED = 'SCHEDULED'
    CANCELED = 'CANCELED'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (SCHEDULED, 'Scheduled'),
        (CANCELED, 'Canceled'),
        (CLOSED, 'Closed'),
    ]

    category = models.CharField(blank=False, choices=CATEGORY_CHOICES, max_length=15)
    status = models.CharField(blank=False, choices=STATUS_CHOICES, max_length=15)
    problem = models.CharField(blank=False, max_length=255)
    solution = models.CharField(blank=False, max_length=255)
