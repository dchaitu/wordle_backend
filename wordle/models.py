from django.db import models

# Create your models here.

class Word(models.Model):
    content = models.CharField(max_length=5)

    def __str__(self):
        return self.content


# class User(models.Model):
#     user = models.CharField(max_length=20)
