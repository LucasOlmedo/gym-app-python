from rest_framework import serializers
from .models import Exercise, PersonalInfo, WorkoutSession, WorkoutHistory, WorkoutSet

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

class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = '__all__'

class WorkoutSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSet
        fields = '__all__'

class WorkoutHistorySerializer(serializers.ModelSerializer):
    sets = WorkoutSetSerializer(many=True)

    class Meta:
        model = WorkoutHistory
        fields = '__all__'

class WorkoutSessionSerializer(serializers.ModelSerializer):
    workout_histories = WorkoutHistorySerializer(many=True)

    class Meta:
        model = WorkoutSession
        fields = '__all__'

    def create(self, validated_data):
        workout_histories_data = validated_data.pop('workout_histories')
        workout_session = WorkoutSession.objects.create(**validated_data)

        for workout_history_data in workout_histories_data:
            sets_data = workout_history_data.pop('sets')
            workout_history = WorkoutHistory.objects.create(workout_session=workout_session, **workout_history_data)

            for set_data in sets_data:
                WorkoutSet.objects.create(workout_history=workout_history, **set_data)

        return workout_session
