import random

from django.http import HttpResponse, JsonResponse
from wordle.models import Word


# Create your views here.

def index(request):
    words = Word.objects.all()
    return HttpResponse(words)


def get_word(request):
    words = Word.objects.all()
    word = random.choice(words)
    print(f"word:- {word.content}")
    return JsonResponse({"word":word.content})
