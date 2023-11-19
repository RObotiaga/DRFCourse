from django.urls import path

from .apps import HabitsConfig
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, UsersHabitListAPIView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')
urlpatterns = [
    path('user/habits/', UsersHabitListAPIView.as_view(), name='user-habits'),
] + router.urls
