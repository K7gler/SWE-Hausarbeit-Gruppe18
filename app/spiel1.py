import pygame
import random

# Initializing game window1
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
    def __init__(self, snake, food, clock, score):
        self.snake = snake
        self.food = food
        self.clock = clock
        self.score = score

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
            
    def update_score(self, screen, color):
        text = Font.get_font().render("Score: " + str(self.score), True, color)
        screen.blit(text, [0,0])
        
    def update_snake_length(self):
        if not self.check_collision():
            self.snake.snake_list.pop(0)
    
    def return_score():
        return game.score


def game_loop(screen, clock):
    # Initialize snake and food
    snake = Snake(250, 250, 10, 10)
    food = Food(round(random.randrange(0, window_size[0] - 10) / 10.0) * 10.0, 
                round(random.randrange(0, window_size[1] - 10) / 10.0) * 10.0, 
                10, 10)
    game = Game(snake, food, clock, 0)
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        screen.fill(Colors.white)
        game.update_snake_position()
        if snake.check_collision_with_borders(window_size[0], window_size[1]):
            run = False
        game.update_food_position()        
        game.update_score(screen, Colors.black)
        snake.draw(screen, Colors.black)
        food.draw(screen, Colors.red)
        pygame.display.update()
        clock.tick(30)        
        game.update_snake_length()
       
    
    pygame.quit()
    Game.score_value = game.score
    
    
game_loop(screen, pygame.time.Clock())
