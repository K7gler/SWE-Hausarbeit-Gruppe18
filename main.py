import hashlib
import csv
 
class User:
    # Konstruktorfunktion für die Klasse "User". Initialisiert eine Benutzerinstanz mit Benutzername, Passworthash und Highscores.
    def __init__(self, username, password_hash, highscore_1, highscore_2):
        self.username = username
        self.password_hash = password_hash
        self.highscore_1 = highscore_1
        self.highscore_2 = highscore_2

    # Statische Methode, die das gegebene Passwort mit SHA-256 hasht.
    @staticmethod
    def get_hash(password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash

    # Statische Methode, die ein neues Benutzerkonto mit dem gegebenen Benutzernamen und Passwort erstellt, wenn der Benutzername noch nicht vergeben ist.
    @staticmethod
    def create_account(username, password):
        if User.is_username_taken(username):
            return "Username is already in use."

        password_hash = User.get_hash(password)
        # Füge die neuen Daten in die CSV-Datei ein
        with open("app/scores.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([username, password_hash, 0, 0])
            return "Account created successfully."

    # Statische Methode, die überprüft, ob der gegebene Benutzername bereits vergeben ist.
    @staticmethod
    def is_username_taken(username):
        with open("app/scores.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == username:
                    return True
        return False

    # Statische Methode, die den Benutzer mit dem gegebenen Benutzernamen und Passwort einloggt und die entsprechende Benutzerinstanz zurückgibt.
    @staticmethod
    def login(username, password):
        password_hash = User.get_hash(password)
        with open("app/scores.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == username and row[1] == password_hash:
                    return User(username, password_hash, int(row[2]), int(row[3]))
        return None

    # Methode, die die Highscores aktualisiert, wenn ein neuer Highscore erreicht wurde.
    def update_highscore(self, game_score_1, game_score_2):
        # update highscore_1 
        if game_score_1 > self.highscore_1:
            self.highscore_1 = game_score_1
        # update highscore_2 
        if game_score_2 > self.highscore_2:
            self.highscore_2 = game_score_2 
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





def main():
    print("Welcome to your game center!")
    #  
    while True:
        print("1. Login")
        print("2. Create an account")
        print("3. Quit")
        # Nimmt die Benutzereingabe entgegen und konvertiert sie in eine ganze Zahl.
        choice = int(input("Enter your choice: "))
        # Wenn der Benutzer sich anmelden möchte.
        if choice == 1:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            # Versuche den Benutzer mit den gegebenen Daten anzumelden.
            user = User.login(username, password)    
            if user:
                # Wenn die Anmeldung erfolgreich war, wird der Benutzer begrüßt und die Highscores werden angezeigt.
                print(f"Welcome back, {username}! Your highscores are {user.highscore_1} and {user.highscore_2}.")
                print(f"1. Game1 - Highscore: {user.highscore_1}")
                print(f"2. Game2 - Highscore: {user.highscore_2}")
                # Der Benutzer wählt ein Spiel aus.
                choose_game = int(input("Choose a game: "))
                if choose_game == 1:
                    import app.spiel1
                    game_score_1 = app.spiel1.Game.score_value
                    user.update_highscore(game_score_1, 0)

                elif choose_game == 2:
                    import app.spiel2
                    game_score_2 = app.spiel2.score_value
                    user.update_highscore(0, game_score_2)               
            else:
                print("Login failed. Invalid username or password.")
        # Wenn der Benutzer ein neues Konto erstellen möchte.
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
