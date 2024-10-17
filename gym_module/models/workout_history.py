from django.db import models
from django.utils import timezone
from .exercise import Exercise
from .workout_session import WorkoutSession

class WorkoutHistory(models.Model):
    workout_session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name="workout_histories")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    duration = models.DurationField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.personal_info} - {self.exercise} - {self.date}"
