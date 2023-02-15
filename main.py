import hashlib
import csv
import pygame

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

class GameCenter:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((400, 300))
		self.font = pygame.font.Font(None, 30)

	def run(self):
		self.show_welcome_screen()
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_1:
						# Login
						username = self.get_input("Enter your username:")
						password = self.get_input("Enter your password:")
						user = User.login(username, password)
						if user:
							self.show_game_select(user)
							break
						else:
							self.show_error("Login failed. Invalid username or password.")
					elif event.key == pygame.K_2:
						# Create an account
						username = self.get_input("Enter a username:")
						if User.is_username_taken(username):
							self.show_error("Username is already taken. Please choose a different one.")
							continue
						password = self.get_input("Enter a password:")
						result = User.create_account(username, password)
						self.show_message(result)
						break
					elif event.key == pygame.K_3:
						pygame.quit()
						return True

		

	def get_input(self, prompt):
		self.show_message(prompt)
		input_text = ""
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						return input_text
					elif event.key == pygame.K_BACKSPACE:
						input_text = input_text[:-1]
					else:
						input_text += event.unicode
			self.show_message(prompt + input_text)


	def show_welcome_screen(self):
		text = self.font.render("Welcome to your game center!", True, (255, 255, 255))
		self.screen.fill((0, 0, 0))
		self.screen.blit(text, (50, 100))
		text = self.font.render("1. Login", True, (255, 255, 255))
		self.screen.blit(text, (50, 150))
		text = self.font.render("2. Create an account", True, (255, 255, 255))
		self.screen.blit(text, (50, 200))
		text = self.font.render("3. Quit", True, (255, 255, 255))
		self.screen.blit(text, (50, 250))
		pygame.display.update()

	def show_highscores(self, user):
		self.screen.fill((0, 0, 0))
		text = self.font.render(f"Welcome back, {user.username}!", True, (255, 255, 255))
		self.screen.blit(text, (50, 100))
		text = self.font.render(f"Your highscores are {user.highscore_1} and {user.highscore_2}.", True, (255, 255, 255))
		self.screen.blit(text, (50, 150))
		pygame.display.update()
	
	def show_game_select(self, user):
		self.screen.fill((0, 0, 0))
		text = self.font.render(f"1. Game1 - Highscore: {user.highscore_1}", True, (255, 255, 255))
		self.screen.blit(text, (50, 100))
		text = self.font.render(f"2. Game2 - Highscore: {user.highscore_2}", True, (255, 255, 255))
		self.screen.blit(text, (50, 150))
		pygame.display.update()
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_1:
						import app.spiel1
						game_score_1 = app.spiel1.Game.transfer_score() # get score	
						user.update_highscore(game_score_1, 0)
						break
					elif event.key == pygame.K_2:
						import app.spiel2
						game_score_2 = app.spiel2.game.transfer_score() # get score
						user.update_highscore(0, game_score_2)
						break
					elif event.key == pygame.K_3:
						pygame.quit()
						done = True
						return
			


	def show_message(self, message):
		self.screen.fill((0, 0, 0))
		text = self.font.render(message, True, (255, 255, 255))
		self.screen.blit(text, (50, 150))
		pygame.display.update()

	def show_error(self, message):
		self.screen.fill((255, 0, 0))
		text = self.font.render(message, True, (255, 255, 255))
		self.screen.blit(text, (50, 150))
		pygame.display.update()

if __name__ == '__main__':
	done = False
	while not done:
		game_center = GameCenter()
		game_center.run()
