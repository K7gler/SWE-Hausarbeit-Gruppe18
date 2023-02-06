import pygame
import random

# Initializing game window1
pygame.init()

# Setting window size
window_size = (500, 500)
screen = pygame.display.set_mode(window_size)

# Setting window title
pygame.display.set_caption("Pygame Snake Game")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Setting font for text
font = pygame.font.Font(None, 25)

# Snake class
class Snake(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.snake_list = [(x, y)]
        self.direction = "right"
        
    def draw(self, screen, color):
        for pos in self.snake_list:
            pygame.draw.rect(screen, color, (pos[0], pos[1], self.width, self.height))

        
# Food class
class Food(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

# Main game loop
def game_loop():
    # Initializing snake and food objects
    snake = Snake(250, 250, 10, 10)
    food = Food(random.randint(0, window_size[0]-10), random.randint(0, window_size[1]-10), 10, 10)
    
    # Initializing clock and score
    clock = pygame.time.Clock()
    score = 0
    
    # Running game until user quits
    run = True
    while run:
        # Setting clock speed
        clock.tick(10)
        
        # Checking for user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        # Clearing screen before redrawing
        screen.fill(black)
        
        # Moving snake and redrawing
        keys = pygame.key.get_pressed()        
        if keys[pygame.K_LEFT]:
            snake.direction = "left"
        if keys[pygame.K_RIGHT]:
            snake.direction = "right"
        if keys[pygame.K_UP]:
            snake.direction = "up"
        if keys[pygame.K_DOWN]:
            snake.direction = "down"
            
        if snake.direction == "left":
            snake.x -= snake.vel
        if snake.direction == "right":
            snake.x += snake.vel
        if snake.direction == "up":
            snake.y -= snake.vel
        if snake.direction == "down":
            snake.y += snake.vel
        
        # Checking for collision with window borders
        if snake.x < 0 or snake.x > window_size[0] or snake.y < 0 or snake.y > window_size[1]:
            run = False
            break
         
        # Checking for collision with snake body 
        snake.snake_list.pop(0)
        snake.snake_list.append((snake.x, snake.y))
        if (snake.x, snake.y) in snake.snake_list[:-1]:
            run = False
            break
        snake.draw(screen, green)
        
        
        # Redrawing food and checking for collision with snake
        food.draw(screen, red)
        food.draw(screen, red)
        snake_rect = pygame.Rect(snake.x, snake.y, snake.width, snake.height)
        food_rect = pygame.Rect(food.x, food.y, food.width, food.height)
        if snake_rect.colliderect(food_rect):
            # Increasing score and creating new food object
            score += 1
            snake.snake_list.append((snake.x, snake.y))
            food = Food(random.randint(0, window_size[0]-10), random.randint(0, window_size[1]-10), 10, 10)
        # Displaying score on screen
        score_text = font.render("Score: " + str(score), True, white)
        screen.blit(score_text, [0, 0])
        
        # Updating screen
        pygame.display.update()
    # Return Score 
    return score    
    # Quitting game
    pygame.quit()

# Running game loop
game_loop()
