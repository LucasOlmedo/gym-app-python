from rest_framework import viewsets
from gym_module.models import PersonalInfo
from gym_module.serializers import PersonalInfoSerializer

class PersonalInfoViewSet(viewsets.ModelViewSet):
    queryset = PersonalInfo.objects.all()
    serializer_class = PersonalInfoSerializer
