from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Bugs(models.Model):
    Title = models.CharField(max_length=100)
    Description = models.TextField()
    Posted = models.DateTimeField(default=timezone.now)
    user_ticket_creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Created',
        blank=True,
        null=True
    )
    user_assigned_ticket = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Assigned',
        blank=True,
        null=True
    )
    user_completed_ticket = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Complete',
        blank=True,
        null=True
    )
    New = 'New'
    In_Progress = 'In_Progress'
    Done = 'Done'
    Invalid = 'Invalid'
    Status_Selection = [
        (New, 'New'),
        (In_Progress, 'In_Progress'),
        (Done, 'Done'),
        (Invalid, 'Invalid')
    ]
    Status = models.CharField(
        max_length=100,
        choices=Status_Selection,
        default=New)

    def __str__(self):
        return f"(self.Title, self.Status)"
