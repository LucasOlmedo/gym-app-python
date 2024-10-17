from rest_framework import serializers
from gym_module.models import WorkoutSession, WorkoutHistory, WorkoutSet
from .workout_history_serializer import WorkoutHistorySerializer

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

    def update(self, instance, validated_data):
        instance.session_name = validated_data.get('session_name', instance.session_name)
        instance.date = validated_data.get('date', instance.date)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.save()

        return instance
