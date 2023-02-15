import pygame
import random

# Initializing game windo
pygame.init()

# Setting window size
window_size = (500, 500)
screen = pygame.display.set_mode(window_size)

# Setting window title
pygame.display.set_caption("Pygame Snake Game")

# Define colors as class variables
class Colors:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

# Setting font for text as static class variable
class Font:
    font = pygame.font.Font(None, 25)
    @staticmethod
    def get_font():
        return Font.font

# Snake class
class Snake(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.snake_list = [(x, y)]
        self.direction = "right"
        
    def draw(self, screen, color):
        for pos in self.snake_list:
            pygame.draw.rect(screen, color, (pos[0], pos[1], self.width, self.height))

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.direction = "right"
        if keys[pygame.K_UP]:
            self.direction = "up"
        if keys[pygame.K_DOWN]:
            self.direction = "down"
         
        if self.direction == "left":
            self.x -= self.vel
        if self.direction == "right":
            self.x += self.vel
        if self.direction == "up":
            self.y -= self.vel
        if self.direction == "down":
            self.y += self.vel
    
    def check_collision_with_borders(self, window_width, window_height):
        if self.x >= window_width or self.x < 0 or self.y >= window_height or self.y < 0:
            return True
        return False

# Food class
class Food(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

# Game class
class Game:
    score_value = 0
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.snake = Snake(250, 250, 10, 10)
        self.food = Food(round(random.randrange(0, window_size[0] - 10) / 10.0) * 10.0, 
                         round(random.randrange(0, window_size[1] - 10) / 10.0) * 10.0, 
                         10, 10)
        self.score = 0

    @classmethod
    def transfer_score(cls):
        return cls.score_value

    def check_collision(self):
        snake_rect = pygame.Rect(self.snake.x, self.snake.y, self.snake.width, self.snake.height)
        food_rect = pygame.Rect(self.food.x, self.food.y, self.food.width, self.food.height)
        return snake_rect.colliderect(food_rect)

    def update_snake_position(self):
        self.snake.move(pygame.key.get_pressed())
        self.snake.snake_list.append((self.snake.x, self.snake.y))

    def update_food_position(self):
        if self.check_collision():
            self.food.x = round(random.randrange(0, window_size[0] - self.food.width) / 10.0) * 10.0
            self.food.y = round(random.randrange(0, window_size[1] - self.food.height) / 10.0) * 10.0
            self.score += 10
            self.snake.vel += 2

    def update_score(self, color):
        text = Font.get_font().render("Score: " + str(self.score), True, color)
        self.screen.blit(text, [0, 0])

    def update_snake_length(self):
        if not self.check_collision():
            self.snake.snake_list.pop(0)

    def game_loop(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.screen.fill(Colors.white)
            self.update_snake_position()
            if self.snake.check_collision_with_borders(window_size[0], window_size[1]):
                run = False
            self.update_food_position()
            self.update_score(Colors.black)
            self.snake.draw(self.screen, Colors.black)
            self.food.draw(self.screen, Colors.red)
            pygame.display.update()
            self.clock.tick(30)
            self.update_snake_length()

        # Prepare score for transfer
        Game.score_value = self.score

        # Display score
        self.screen.fill(Colors.white)
        text = Font.get_font().render("Your score: " + str(self.score), True, Colors.black)
        self.screen.blit(text, [window_size[0]/2 - 50, window_size[1]/2])
        pygame.display.update()
        pygame.time.wait(3000)
        pygame.quit()

# Create an instance of the Game class and call game_loop() method
game = Game(screen, pygame.time.Clock())
game.game_loop()
