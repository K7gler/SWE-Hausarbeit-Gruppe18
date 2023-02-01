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
    # Initialize class with a database parameter
    def __init__(self, database):
        # Assign the database parameter to self.database
        self.database = database

    # Define the run method for the LoginScreen class
    def run(self):
        # Input prompt for the username
        username = input("Username: ")
        # Get the user from the database using the entered username
        user = self.database.get_user(username)
        # If the user is not found in the database
        if user is None:
            # Prompt the user to create a new account or exit
            create = input(f"No user '{username}' found. Create a new user? (y/n) ")
            # If the user chooses to create a new account
            if create.lower() == "y":
                # Input prompts for password and confirmation
                password = input("Password: ")
                password2 = input("Confirm password: ")
                # If the passwords don't match, print an error message
                if password != password2:
                    print("Passwords do not match.")
                # If the create_user method returns True
                elif self.database.create_user(username, password):
                    # Print a success message and get the user from the database again
                    print("User created.")
                    user = self.database.get_user(username)
                # If the create_user method returns False
                else:
                    # Print an error message
                    print("User creation failed.")
            # If the user chooses not to create a new account
            else:
                # Print a goodbye message and return
                print("Goodbye.")
                return
        # If the user is found in the database
        else:
            # Input prompt for the password
            password = input("Password: ")
            # Check if the entered password matches the user's password
            if not user.check_password(password):
                # Print an error message if the password is incorrect
                print("Incorrect password.")
            # If the password is correct
            else:
                # Print a success message
                print("Login successful.")

# If the script is being run as the main program
if __name__ == "__main__":
    # Initialize the database with a file path
    database = UserDatabase("app/scores.csv")
    # Initialize the LoginScreen class with the database
    login_screen = LoginScreen(database)
    # Run the login screen
    login_screen.run()
