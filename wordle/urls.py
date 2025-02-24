from django.urls import path

from wordle.views import LoginAPI, SignupAPI, GuessedWordView, GetWordView

urlpatterns = [
    path('word/', GetWordView.as_view()),
    path('guess/', GuessedWordView.as_view()),
    path('login/', LoginAPI.as_view(), name='token_login'),
    path('signup/', SignupAPI.as_view(),name='token_signup'),

]