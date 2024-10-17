from django.db import models
from .workout_history import WorkoutHistory

class WorkoutSet(models.Model):
    workout_history = models.ForeignKey(WorkoutHistory, on_delete=models.CASCADE, related_name="sets")
    set_number = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    reps = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    rest_time = models.DurationField(blank=True, null=True)
