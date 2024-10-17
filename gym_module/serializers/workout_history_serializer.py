from rest_framework import serializers
from gym_module.models import WorkoutHistory
from .workout_set_serializer import WorkoutSetSerializer

class WorkoutHistorySerializer(serializers.ModelSerializer):
    sets = WorkoutSetSerializer(many=True)

    class Meta:
        model = WorkoutHistory
        fields = '__all__'
