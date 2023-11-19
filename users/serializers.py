from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('user_id', 'password',)


class UserSerializerForOthers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('user_id', 'password',)


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('user_id', 'password',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
