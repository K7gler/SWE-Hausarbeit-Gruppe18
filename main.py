# login class
class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login = False

    def login(self):
        if self.username == "admin" and self.password == "admin":
            self.login = True
        else:
            self.login = False

    def get_login(self):
        return self.login