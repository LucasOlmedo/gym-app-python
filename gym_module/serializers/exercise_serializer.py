from rest_framework import serializers
from gym_module.models import Exercise

class ExerciseSerializer(serializers.ModelSerializer):
    secondary_muscles = serializers.SerializerMethodField()
    instructions = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = '__all__'

    def get_secondary_muscles(self, obj):
        return obj.secondary_muscles.split('||') if obj.secondary_muscles else []

    def get_instructions(self, obj):
        return obj.instructions.split('||') if obj.instructions else []
