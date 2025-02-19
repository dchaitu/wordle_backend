import json
import random

from django.contrib.auth.models import User
from django.http import JsonResponse

from wordle.interactor.match_word_interactor import MatchWordInteractor
from wordle.models import Word, GuessedWord, CorrectWord
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from wordle.serializers import UserSerializer, LoginSerializer, GuessedWordSerializer
from wordle.storage.storage_implementation import StorageImplementation



class GetWordView(APIView):
    def get(self, request):
        words = Word.objects.all()
        word = random.choice(words)
        print(f"word:- {word.content}")
        CorrectWord.objects.create(word=word)

        return JsonResponse({"word":word.content})



class GuessedWordView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))  # ✅ Ensure JSON parsing
            print(f"Request body: {data.get('content')}")  # ✅ Debugging
            print("request data", data)
            print("guessed word data", data.get('content'))
            storage = StorageImplementation()
            interactor = MatchWordInteractor(storage=storage)
            serializer = GuessedWordSerializer(data=data)
            if serializer.is_valid():

                username = serializer.validated_data['username']
                guessed_word = serializer.validated_data['content']
                storage.store_guessed_word(username=username, guessed_word=guessed_word)
                color_dict =interactor.check_is_word_matched(guessed_word)
                print(f"color_dict {color_dict}")

                return Response({
                    "status": "success",
                    "data": color_dict
                })

            return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "data": serializer.errors
                })
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON"}, status=400)


class SignupAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user": serializer.data
            })

        return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "data": serializer.errors
            })


class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        print(data)
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "status": "error",
                "data": serializer.errors
            })

        username = serializer.data['username']
        password = serializer.data['password']

        user_obj = authenticate(username=username, password=password)
        print(username, password)
        if user_obj:
            token, _ = Token.objects.get_or_create(user=user_obj)
            print(token)
            return Response({
                "status": "success",
                "data": {
                    "token": {
                        str(token)},
                }
            })


        return Response({
            "status": "Invalid Credentials",
        })
