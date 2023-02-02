import pygame
import time
import random

pygame.init()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Screen dimensions
dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.update()

clock = pygame.time.Clock()

# Font for displaying score
font_style = pygame.font.SysFont(None, 30)

def our_snake(block_size, snake_list):
    for x,y in snake_list:
        pygame.draw.rect(dis, yellow, [x, y, block_size, block_size])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width/6, dis_height/3])

def gameLoop():
    game_over = False
    game_close = False

    # Initial position of the snake
    x1 = dis_width / 2
    y1 = dis_height / 2

    # Initial velocity
    x1_change = 0
    y1_change = 0

    # Snake block size
    block_size = 10

    # List to keep track of all the blocks in the snake
    snake_List = []
    Length_of_snake = 1

    # Food position
    foodx = round(random.randrange(0, dis_width - block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - block_size) / 10.0) * 10.0

    # Main game loop
    while not game_over:

        while game_close == True:
            dis.fill(black)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_close = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0

        # Moving the snake by updating the x and y coordinates
        x1 += x1_change
        y1 += y1_change

        # Adding a black background to the display window
        dis.fill(white)

        # Displaying the food
        pygame.draw.rect(dis, green, [foodx, foody, block_size, block_size])

        # Adding the snake to the display
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x,y in snake_List[:-1]:
            if x == snake_Head[0] and y == snake_Head[1]:
                game_close = True

        # Drawing the snake and updating the display
        our_snake(block_size, snake_List)
        pygame.display.update()

        # Checking if the snake hits the boundry
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        # Checking if the snake eats the food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - block_size) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - block_size) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(10)

    # Deactivating pygame library
    pygame.quit()

# Starting the game
gameLoop()