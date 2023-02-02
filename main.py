import hashlib
import csv

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)
        self.scores = [0, 0]

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        return self.hash_password(password) == self.password

class UserDatabase:
    def __init__(self, path):
        self.path = path
        self.users = {}
        self.load_users()

    def load_users(self):
        with open(self.path, "r") as file:
            reader = csv.reader(file)
            next(reader)  
            for line in reader:
                username, password, score1, score2 = line
                user = User(username, password)
                user.scores = [int(score1), int(score2)]
                self.users[username] = user

    def save_users(self):
        with open(self.path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Password", "Punkte1", "Punkte2"])
            for user in self.users.values():
                writer.writerow([user.username, user.password, *user.scores])

    def get_user(self, username):
        return self.users.get(username)

    def create_user(self, username, password):
        if username in self.users:
            return False
        user = User(username, password)
        self.users[username] = user
        self.save_users()
        return True


class LoginScreen:
    def __init__(self, database):
        self.database = database

    def run(self):
        username = input("Username: ")
        user = self.database.get_user(username)
        if user is None:
            create = input(f"No user '{username}' found. Create a new user? (y/n) ")
            if create.lower() == "y":
                password = input("Password: ")
                password2 = input("Confirm password: ")
                if password != password2:
                    print("Passwords do not match.")
                elif self.database.create_user(username, password):
                    print("User created.")
                    user = self.database.get_user(username)
                else:
                    print("User creation failed.")
            else:
                print("Goodbye.")
                return
        else:
            password = input("Password: ")
            if not user.check_password(password):
                print("Incorrect password.")
            else:
                print("Login successful.")

if __name__ == "__main__":
    database = UserDatabase("app/scores.csv")
    login_screen = LoginScreen(database)
    login_screen.run()
    