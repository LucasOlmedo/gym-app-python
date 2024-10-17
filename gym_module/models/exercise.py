from django.db import models

class Exercise(models.Model):

    body_part = models.CharField(max_length=100)
    equipment = models.CharField(max_length=100)
    gif_url = models.CharField(max_length=100)
    ref_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    secondary_muscles = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.name
