from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['title','image', 'url', 'description','date', 'user']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image', 'bio','date']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'profile', 'posts','email']