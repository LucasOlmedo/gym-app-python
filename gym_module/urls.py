from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExerciseViewSet, PersonalInfoViewSet

router = DefaultRouter()

router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'personal-info', PersonalInfoViewSet, basename='personal-info')

urlpatterns = [
    path('', include(router.urls)),
]
