import pygame
import random

# Initializing game window
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
        self.body = [(x, y)]
        
    def draw(self, screen, color):
        for x, y in self.body:
            pygame.draw.rect(screen, color, (x, y, self.width, self.height))        
        
# Food class
class Food(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

# Main Game loop
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
            snake.x -= snake.vel
        if keys[pygame.K_RIGHT]:
            snake.x += snake.vel
        if keys[pygame.K_UP]:
            snake.y -= snake.vel
        if keys[pygame.K_DOWN]:
            snake.y += snake.vel
        snake.body = [(snake.x, snake.y)] + snake.body[:-1]
        snake.draw(screen, green)

        # Redrawing food and checking for collision with snake
        food.draw(screen, red)

        for x, y in snake.body:
            if x == food.x and y == food.y:
                # Increasing score and creating new food object
                score += 1
                snake.body.append(snake.body[-1])
                food = Food(random.randint(0, window_size[0]-10), random.randint(0, window_size[1]-10), 10, 10)
                break
            
        # Displaying score on screen
        score_text = font.render("Score: " + str(score), True, white)
        screen.blit(score_text, [0, 0])
        
        # Updating screen
        pygame.display.update()
        
    # Quitting game
    pygame.quit()

# Running game loop
game_loop()
