from django.contrib import admin
from django.urls import path

from wordle import views

urlpatterns = [
# path('words/', views.index),
path('word/', views.get_word),

]