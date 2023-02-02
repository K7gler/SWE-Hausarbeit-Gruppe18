import hashlib
import csv

class UserDB:
    def __init__(self, username, password, score1, score2):
        self.username = username
        self.password = self.hash_password(password)
        self.score1 = score1
        self.score2 = score2

    @staticmethod
    def hash_password(password):
        return hashlib.sha256