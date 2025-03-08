from django.contrib.auth.models import User

from wordle.interactor.storage_interface.storage_interface import StorageInterface
from wordle.models import Word, CorrectWord, GuessedWord


class StorageImplementation(StorageInterface):

    def get_all_words(self):
        words = Word.objects.all()
        return words

    def store_correct_word(self, content:str):
        word = Word.objects.get(content=content)
        CorrectWord.objects.create(word=word)

    def store_guessed_word(self, username:str, guessed_word:str):
        user = User.objects.get(username=username)
        GuessedWord.objects.create(user=user, content=guessed_word)


    def get_latest_word(self):
        correct_word_obj = CorrectWord.objects.last()
        correct_word = correct_word_obj.word.content
        print("Current Word ", correct_word)
        return correct_word

    def get_user_by_username(self, username:str):
        user = User.objects.get(username=username)
        return user

    def set_user_password(self, username:str, password:str):
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        return user
