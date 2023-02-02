import pygame
import random

pygame.init()

width, height = 500, 500
cell_size = 20
cols, rows = width//cell_size, height//cell_size

black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Snake Game')

class Snake:
    def __init__(self):
        self.x = cols//2
        self.y = rows//2
        self.body = [(self.x, self.y)]
        self.dir_x = 0
        self.dir_y = -1

    def update(self):
        self.x += self.dir_x
        self.y += self.dir_y
        self.body.insert(0, (self.x, self.y))
        self.body.pop()

    def change_direction(self, dir_x, dir_y):
        self.dir_x = dir_x
        self.dir_y = dir_y

    def grow(self):
        self.body.insert(0, (self.x, self.y))

    def draw(self, screen, cell_size):
        for x, y in self.body:
            pygame.draw.rect(screen, white, (x*cell_size, y*cell_size, cell_size, cell_size))

class Food:
    def __init__(self):
        self.x = random.randint(0, cols-1)
        self.y = random.randint(0, rows-1)

    def draw(self, screen, cell_size):
        pygame.draw.rect(screen, white, (self.x*cell_size, self.y*cell_size, cell_size, cell_size))

snake = Snake()
food = Food()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(0, -1)
            if event.key == pygame.K_DOWN:
                snake.change_direction(0, 1)
            if event.key == pygame.K_LEFT:
                snake.change_direction(-1, 0)
            if event.key == pygame.K_RIGHT:
                snake.change_direction(1, 0)
        if snake.x == food.x and snake.y == food.y:
            snake.grow()
            food = Food()
        if snake.x < 0 or snake.x > cols-1 or snake.y < 0 or snake.y > rows-1:
            running = False
        
        for i in range(1, len(snake.body)):
            if snake.x == snake.body[i][0] and snake.y == snake.body[i][1]:
                running = False

        snake.update()
        screen.fill(black)

        snake.draw(screen, cell_size)
        food.draw(screen, cell_size)

        pygame.display.update()

pygame.quit()
