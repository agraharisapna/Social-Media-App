from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "username", "email"]

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    #Optional - Adding this purposely as username looking empty at backend
    username = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username']

    def create(self, validated_data):
        register_user = User.objects.create(
            email = validated_data['email'],
            username=validated_data['username']
        )
        register_user.set_password(validated_data['password'])
        register_user.save()
        return register_user







