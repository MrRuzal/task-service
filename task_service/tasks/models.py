from django.db import models


class Task(models.Model):
    STATUSES = [
        ('created', 'Created'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]

    number = models.IntegerField(unique=True)
    status = models.CharField(
        max_length=20, choices=STATUSES, default='created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
