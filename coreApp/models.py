from django.db import models
import datetime
from django.db.models.deletion import CASCADE
from userApp.models import *

FREQUENCY_CHOICES = [
    ('One Time', 'One Time'),
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
    ('Yearly', 'Yearly')
]

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    frequency = models.CharField(max_length=255, choices=FREQUENCY_CHOICES, default="One Time")
    completed = models.BooleanField(default=False)
    dueDate = models.DateField()
    user = models.ForeignKey(User, related_name='theUser', on_delete=CASCADE)
    lastCompleted = models.DateField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class History(models.Model):
    dateCompleted = models.DateField()
    task = models.ForeignKey(Task, related_name='theTask', on_delete=CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)