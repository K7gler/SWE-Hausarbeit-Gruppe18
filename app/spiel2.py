import pygame

class Tetris:
    height = 0
    width = 0
    field = []
    score = 0
    state = "start"

    def __int__(self, _height, _width):
        self.height = _height
        self.width = _width
        self.field = []
        self.score = 0 
        self.state = "start"
        for i in range(_height):
            new_line = []
            for j in range(_width):
                new_line.append(0)
            self.field.append(new_line)


pygame.init()
screen = pygame.display.set_mode((380,620))
pygame.display.set_caption("Tetris")

done = False
fps = 25
clock = pygame.time.Clock()
counter = 0
zoom = 30
game = Tetris()

pressing_down = False
pressing_left = False
pressing_right = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                pressing_left = True
            if event.key == pygame.K_RIGHT:
                pressing_right = True

            if pressing_down:
                game.down()
            if pressing_left:
                game.left()
            if pressing_right:
                game.right()

        if event.type == pygame.K_UP:
             if event.key == pygame.K_DOWN:
                pressing_down = False
             if event.key == pygame.K_LEFT:
                pressing_left = False
             if event.key == pygame.K_RIGHT:
                pressing_right = False


screen.fill(color=WHITE)
for i in range(game.height):
    for j in range(game.width):
        pygame.draw.rect(screen, GRAY, [30+j*zoom, 30+i*zoom, zoom, zoom], 1)


pygame.display.flip()
clock.tick(fps)







pygame.quit()
