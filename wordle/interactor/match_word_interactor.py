from collections import defaultdict
from typing import Dict

from wordle.interactor.storage_interface.storage_interface import StorageInterface


class MatchWordInteractor:
    def __init__(self, storage:StorageInterface):
        self.storage = storage


    def check_is_word_matched(self, username:str,guessed_word:str)-> Dict[int,str]:
        self.storage.store_guessed_word(username=username, guessed_word=guessed_word)
        correct_word = self.storage.get_latest_word()
        verifying_word = list(correct_word)
        color_cells = {}
        for i in range(5):
            if verifying_word[i] == guessed_word[i]:
                color_cells[i] = "correctPosition"
                verifying_word[i] = None
            elif verifying_word[i] in correct_word:
                color_cells[i] = "present"
            else:
                color_cells[i] = "notPresent"

        return color_cells

