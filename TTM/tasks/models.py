from django.db import models
from django.utils import timezone
from django.conf import settings

class Task(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        DESIGNED = "DESIGNED", "Designed"
        IN_PROGRESS = "IN_PROGRESS", "In progress"
        DONE = "DONE", "Done"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.OPEN,
        )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="owned_tasks",
        )
    
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        related_name="assigned_tasks", 
        null=True, 
        blank=True
        )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == self.Status.DONE and self.completed_at is None:
            self.completed_at = timezone.now()

        if self.status != self.Status.DONE:
            self.completed_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title