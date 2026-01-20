from django.db import models
from django.contrib.auth.models import User 

class Task(models.Model):
    # This says "A task belongs to one user. If the user is deleted, delete their tasks too."
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)

    @property
    def is_overdue(self):
        from django.utils import timezone
        if self.due_date and not self.completed:
            return timezone.now() > self.due_date
        return False

    @property
    def due_soon(self):
        from django.utils import timezone
        from datetime import timedelta
        if self.due_date and not self.completed:
            now = timezone.now()
            five_hours_from_now = now + timedelta(hours=5)
            # True if the task is due between now and 5 hours from now
            return now < self.due_date <= five_hours_from_now
        return False

    def __str__(self):
        return self.title