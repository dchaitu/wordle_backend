from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Word(models.Model):
    content = models.CharField(max_length=5)

    def __str__(self):
        return self.content


class GuessedWord(models.Model):
    user  = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.CharField(max_length=5)

    def __str__(self):
        return str(self.content)


class CorrectWord(models.Model):
    word = models.ForeignKey('Word', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.word.content)
