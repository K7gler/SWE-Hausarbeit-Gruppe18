import hashlib
import csv
 
class User:
    def __init__(self, username, password_hash, highscore_1, highscore_2):
        self.username = username
        self.password_hash = password_hash
        self.highscore_1 = highscore_1
        self.highscore_2 = highscore_2

    def get_hash(password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash

    def create_account(username, password):
        if User.is_username_taken(username):
            return "Username is already in use."

        password_hash = User.get_hash(password)
        # Write the username, password hash, and initial highscores to the CSV file
        with open("app/scores.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([username, password_hash, 0, 0])
            return "Account created successfully."

    def login(username, password):
        password_hash = User.get_hash(password)
        with open("app/scores.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == username and row[1] == password_hash:
                    # Return the highscores if the username and password hash match
                    return User(username, password_hash, int(row[2]), int(row[3]))
        # User was not found
        return None

    def is_username_taken(username):
        with open("app/scores.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == username:
                    return True
        return False

    def update_highscore(self, game_score_1, game_score_2):
        # update highscore_1 with game_score_1 if game_score_1 is greater than highscore_1
        if game_score_1 > self.highscore_1:
            self.highscore_1 = game_score_1
        # update highscore_2 with game_score_2 if game_score_2 is greater than highscore_2
        if game_score_2 > self.highscore_2:
            self.highscore_2 = game_score_2

        with open("app/scores.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
        
        for i, row in enumerate(rows):
            if row[0] == self.username:
                # update the highscores for the user in the csv file
                rows[i][2] = self.highscore_1
                rows[i][3] = self.highscore_2
        
        with open("app/scores.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

def main():
    print("Welcome to the score tracking app.")
    while True:
        print("1. Login")
        print("2. Create an account")
        print("3. Quit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user = User.login(username, password)    
            if user:
                print(f"Welcome back, {username}! Your highscores are {user.highscore_1} and {user.highscore_2}.")
                print(f"1. Game1 - Highscore: {user.highscore_1}")
                print(f"2. Game2 - Highscore: {user.highscore_2}")
                choose_game = int(input("Choose: which game you want to play?"))
                if choose_game == 1:
                    import app.spiel1
                    game_score_1 = app.spiel1.game_loop()
                    user.update_highscore(game_score_1, 0)

                elif choose_game == 2:
                    import app.spiel2
                    game_score_2 = app.spiel2.game_loop()
                    user.update_highscore(0, game_score_2)
               
            else:
                print("Login failed. Invalid username or password.")
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