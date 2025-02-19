import abc

class StorageInterface(abc.ABC):

    @abc.abstractmethod
    def get_all_words(self):
        pass

    @abc.abstractmethod
    def get_latest_word(self):
        pass

    @abc.abstractmethod
    def store_correct_word(self, content:str):
        pass

    @abc.abstractmethod
    def get_user_by_username(self, username:str):
        pass

    @abc.abstractmethod
    def store_guessed_word(self,username:str, guessed_word:str):
        pass


