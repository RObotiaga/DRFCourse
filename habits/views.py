from decouple import config
import telebot
from django.shortcuts import HttpResponse
from rest_framework import viewsets, generics
from .models import Habit
from users.models import CustomUser
from .serializers import HabitSerializer
import datetime
import random
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsOwner, IsManager
from .pagination import HabitPagination
from .services import create_periodic_task


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    queryset = Habit.objects.filter(public='public')

    def perform_create(self, serializer):
        habit = serializer.save(creator=self.request.user)
        if habit.pleasantness == 'unpleasant':
            create_periodic_task(habit)

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsOwner | IsAdminUser | IsManager, ]
        elif self.action == 'delete' or self.action == 'create':
            permission_classes = [IsOwner, IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [IsOwner | IsAdminUser, IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class UsersHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(creator=user)
