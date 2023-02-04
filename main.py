# user class
class User:
    def __init__(self, username, password, highscore_1, highscore_2):
        self.username = username 
        self.password = password 
        self.highscore_1 = highscore_1 
        self.highscore_2 = highscore_2
    

class UserManagement:
    def __init__(self):
        self.users = []
        self.load_users()

    def load_users(self):
        with open('app/scores.csv', 'r') as f:
            for line in f:
                username, password, highscore_1, highscore_2 = line.strip().split(',')
                self.users.append(User(username, password, highscore_1, highscore_2))

    def save_users(self):
        with open('app/scores.csv', 'w') as f:
            for user in self.users:
                f.write(f'{user.username},{user.password},{user.highscore_1},{user.highscore_2}

        