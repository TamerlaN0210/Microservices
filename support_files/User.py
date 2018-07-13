import hashlib
from initialize.config import *


class User:
    def __init__(self, dict_: dict):
        self.username = dict_.get("username")
        self.__password = dict_.get("password")
        self.created_at = dict_.get("created_at")

    def get_hashed_password(self):
        return hashlib.md5((self.__password + SALT).encode('utf-8')).digest()

    def is_valid_for_registry(self):
        if self.username is not None and type(self.username) is str and \
                self.__password is not None and type(self.__password) is str and \
                self.created_at is not None and type(self.created_at) is int:
            return True
        else:
            return False

    def is_valid_for_auth(self):
        if self.username is not None and type(self.username) is str and \
                self.__password is not None and type(self.__password) is str:
            return True
        else:
            return False
