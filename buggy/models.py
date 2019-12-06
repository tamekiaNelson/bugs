from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Bugs(models.Model):
    user_ticket_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    posted = models.DateTimeField(default=timezone.now)
    user_assigned_ticket = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned',
    )
    user_completed_ticket = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='complete',
    )
    new = 'N'
    in_progress = 'P'
    done = 'D'
    invalid = 'I'
    status_selection = [
        (new, 'New'),
        (in_progress, 'In Progress'),
        (done, 'Done'),
        (invalid, 'Invalid')
    ]
    status = models.CharField(
        max_length=1, choices=status_selection, default=new)
