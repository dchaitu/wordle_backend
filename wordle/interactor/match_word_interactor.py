from collections import defaultdict

from wordle.interactor.storage_interface.storage_interface import StorageInterface


class MatchWordInteractor:
    def __init__(self, storage:StorageInterface):
        self.storage = storage


    def check_is_word_matched(self, guessed_word:str):

        correct_word = self.storage.get_latest_word()
        color_cells = {}
        for i in range(5):
            if correct_word[i] == guessed_word[i]:
                color_cells[i] = "correctPosition"
            elif guessed_word[i] in correct_word and guessed_word[i]:
                color_cells[i] = "present"

            else:
                color_cells[i] = "notPresent"

        return color_cells

