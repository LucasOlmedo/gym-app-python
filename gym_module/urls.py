from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gym_module.views import ExerciseViewSet, PersonalInfoViewSet, WorkoutSessionViewSet

router = DefaultRouter()

router.register(r'exercises', ExerciseViewSet, basename='exercises')
router.register(r'personal-info', PersonalInfoViewSet, basename='personal-info')
router.register(r'workout-sessions', WorkoutSessionViewSet, basename='workout-sessions')

urlpatterns = [
    path('', include(router.urls)),
]
