from django.urls import path

from wordle import views
from wordle.views import LoginAPI, SignupAPI, GuessedWordView, GetWordView

urlpatterns = [
    path('word/', GetWordView.as_view()),
    path('guess/', GuessedWordView.as_view()),
    path('login/', LoginAPI.as_view()),
    path('signup/', SignupAPI.as_view()),

]