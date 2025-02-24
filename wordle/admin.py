from django.contrib import admin

from wordle.models import Word, GuessedWord, CorrectWord


class WordAdmin(admin.ModelAdmin):
    list_display = ["id", "content"]

class GuessedWordAdmin(admin.ModelAdmin):
    list_display = ["id", "content", "user"]





# Register your models here.
admin.site.register(Word, WordAdmin)
admin.site.register(GuessedWord, GuessedWordAdmin)
admin.site.register(CorrectWord)

