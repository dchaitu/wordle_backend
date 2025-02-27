import json
import random

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from wordle.interactor.match_word_interactor import MatchWordInteractor
from wordle.models import Word, GuessedWord, CorrectWord
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from wordle.serializers import UserSerializer, LoginSerializer, GuessedWordSerializer
from wordle.storage.storage_implementation import StorageImplementation



class GetWordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        user = request.user
        words = Word.objects.all()
        print("user", user)
        if user.is_authenticated:
            word = random.choice(words)
            CorrectWord.objects.create(word=word)
            print(word)

            return JsonResponse({
                "status": status.HTTP_201_CREATED,
                "response":"Word is selected"})

        return JsonResponse({
            "status": status.HTTP_404_NOT_FOUND,
            "response": "No words available"
        }, status=404)




class CorrectWordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        storage = StorageImplementation()
        interactor = MatchWordInteractor(storage=storage)
        correct_word = interactor.get_correct_word()
        return JsonResponse({
            "status": "success",
            "answer": correct_word
        })




class GuessedWordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
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

                username = request.user.username
                guessed_word = serializer.validated_data['content']
                color_dict =interactor.check_is_word_matched(username,guessed_word)
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
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=data['username'])
            user.set_password(data['password'])
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
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user_obj = authenticate(username=username, password=password)
            print(username, password)
            if user_obj is not None:
                refresh = RefreshToken.for_user(user_obj)
                user_serializer = UserSerializer(user_obj)
                # Verification of user
                if not user_obj.is_authenticated:
                    return Response({
                        "status": "error",
                        "data": "User is not verified"
                    }, status=status.HTTP_400_BAD_REQUEST)

                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": user_serializer.data
                })

        return Response({
                "status": "error",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)








