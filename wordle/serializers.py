from django.contrib.auth.models import User
from rest_framework import serializers

from wordle.models import GuessedWord


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password','email']



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class GuessedWordSerializer(serializers.Serializer):
    username = serializers.CharField()
    content = serializers.CharField()

