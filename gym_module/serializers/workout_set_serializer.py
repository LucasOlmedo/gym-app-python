from rest_framework import serializers
from gym_module.models import WorkoutSet

class WorkoutSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSet
        fields = '__all__'
