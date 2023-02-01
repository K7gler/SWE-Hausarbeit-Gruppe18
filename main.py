import hashlib
import csv

class User:
    # Constructor to initialize a User object
    def __init__(self, username, password):
        # Store the given username as an instance variable
        self.username = username
        # Hash the given password and store the hashed password
        self.password = self.hash_password(password)
        # Initialize the scores list with two zeros
        self.scores = [0, 0]

    # Method to hash a password using the SHA-256 algorithm
    @staticmethod
    def hash_password(password):
        # Encode the password as a byte string and hash it using the SHA-256 algorithm
        # Return the hexadecimal representation of the hash
        return hashlib.sha256(password.encode()).hexdigest()

    # Method to check if a given password matches the stored password
    def check_password(self, password):
        # Return True if the hash of the given password matches the stored hashed password, False otherwise
        return self.hash_password(password) == self.password

class UserDatabase:
    def __init__(self, path):
        # initialize the UserDatabase object with the file path
        self.path = path
        self.users = {}
        # load the user data from the file
        self.load_users()

    def load_users(self):
        # open the file for reading
        with open(self.path, "r") as file:
            reader = csv.reader(file)
            # skip the header line of the file
            next(reader)  
            for line in reader:
                # unpack the line into username, password, score1, score2
                username, password, score1, score2 = line
                # create a new User object with the given username and password
                user = User(username, password)
                # update the scores of the user object
                user.scores = [int(score1), int(score2)]
                # store the user object in the dictionary self.users, with username as the key
                self.users[username] = user

    def save_users(self):
        # open the file for writing
        with open(self.path, "w") as file:
            writer = csv.writer(file)
            # write the header line to the file
            writer.writerow(["Username", "Password", "Punkte1", "Punkte2"])
            for user in self.users.values():
                # write the username, password, and scores of each user to the file
                writer.writerow([user.username, user.password, *user.scores])

    def get_user(self, username):
        # return the user object for the given username, or None if the username does not exist
        return self.users.get(username)

    def create_user(self, username, password):
        # check if the given username already exists in self.users
        if username in self.users:
            # if the username already exists, return False
            return False
        # create a new User object with the given username and password
        user = User(username, password)
        # store the user object in the dictionary self.users, with username as the key
        self.users[username] = user
        # save the updated user data to the file
        self.save_users()
        # return True if the user was created successfully
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