from django.db import models
from django.utils import timezone
from .personal_info import PersonalInfo

class WorkoutSession(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='workout_sessions')
    session_name = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)

    def __str__(self):
        return f"Workout Session on {self.date} for {self.personal_info}"
