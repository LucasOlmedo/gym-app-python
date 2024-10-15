from rest_framework import viewsets
from .models import Exercise
from .serializers import ExerciseSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['body_part', 'equipment', 'target']
    search_fields = ['name', 'secondary_muscles']