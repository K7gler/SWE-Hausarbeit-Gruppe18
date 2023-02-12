import hashlib
import csv
 
class User:
    def __init__(self, username, password_hash, highscore_1, highscore_2):
        """
        Initialize a User instance with the given username, password hash, and high scores.
        """
        self.username = username
        self.password_hash = password_hash
        self.highscore_1 = highscore_1
        self.highscore_2 = highscore_2

    @staticmethod
    def get_hash(password):
        """
        Hash the given password using SHA-256.
        """
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash

    @staticmethod
    def create_account(username, password):
        """
        Create a new user account if the username is not already taken.
        """
        if User.is_username_taken(username):
            return "Username is already in use."

        password_hash = User.get_hash(password)
        # Write the username, password hash, and initial highscores to the CSV file
        with open("app/scores.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([username, password_hash, 0, 0])
            return "Account created successfully."

    @staticmethod
    def is_username_taken(username):
        """
        Check if the given username is already taken.
        """
        with open("app/scores.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == username:
                    return True
        return False

    @staticmethod
    def login(username, password):
        """
        Log in with the given username and password and return the corresponding User instance.
        """
        password_hash = User.get_hash(password)
        with open("app/scores.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == username and row[1] == password_hash:
                    # Return the User instance if the username and password hash match
                    return User(username, password_hash, int(row[2]), int(row[3]))
        # User was not found
        return None

    def update_highscore(self, game_score_1, game_score_2):
        # update highscore_1 
        if game_score_1 > self.highscore_1:
            self.highscore_1 = game_score_1
        # update highscore_2 
        if game_score_2 > self.highscore_2:
            self.highscore_2 = game_score_2

        # update the csv file with the new highscores
        with open("app/scores.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
        
        for i, row in enumerate(rows):
            if row[0] == self.username:        
                rows[i][2] = self.highscore_1
                rows[i][3] = self.highscore_2
        
        with open("app/scores.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)




# mainfunction 
def main():
    print("Welcome to your game center!")
    # Loop until the user quits 
    while True:
        print("1. Login")
        print("2. Create an account")
        print("3. Quit")
        # Get the user's choice
        choice = int(input("Enter your choice: "))
        if choice == 1:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            # Try to login the user
            user = User.login(username, password)    
            if user:
                # If the login was successful, print the highscores and ask the user which game they want to play
                print(f"Welcome back, {username}! Your highscores are {user.highscore_1} and {user.highscore_2}.")
                print(f"1. Game1 - Highscore: {user.highscore_1}")
                print(f"2. Game2 - Highscore: {user.highscore_2}")
                choose_game = int(input("Choose: which game you want to play?"))
                if choose_game == 1:
                    # Import game1 and run it
                    import app.spiel1                    
                    game_score_1 = app.spiel1.Game.get_score()
                    print(game_score_1)
                    user.update_highscore(game_score_1, 0)

                elif choose_game == 2:
                    # Import game2 and run it
                    import app.spiel2
                    game_score_2 = app.spiel2.game_loop()
                    user.update_highscore(0, game_score_2)               
            else:
                print("Login failed. Invalid username or password.")
        # Create a new account
        elif choice == 2:
            username = input("Enter a username: ")
            if User.is_username_taken(username):
                print("Username is already taken. Please choose a different one.")
                continue
            password = input("Enter a password: ")
            result = User.create_account(username, password)
            print(result)
        else:
            break

if __name__ == '__main__':
    main()