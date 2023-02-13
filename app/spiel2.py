import pygame
import random
# Farbe  und Form der Tetris Blöcken definieren
colors = [
    (3, 3, 3),   # Schwarz
    (0, 128, 0),   # Green
    (255, 0, 0),   # Rot
    (160, 82, 45),   # Braun
    (255, 153, 18),  # Gelb
    (139, 10, 80),   # Rosa
    (71, 60, 139),   # Lila
]

# Form der Tetris : S, Z, I, T, O, J, L

# Matrix :     0   1   2   3
#              4   5   6   7
#              8   9   10  11
#              12  13  14  15
class Figure:
    x = 0
    y = 0
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # I
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # L
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # J
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T
        [[1, 2, 5, 6]],  # o
        [[4, 5, 9, 10], [2, 6, 5, 9]],  # Z
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # S

    ]
# Rotation, Farbe und type initialisieren
    type = 3
    color = 1
    rotation = 0
# Typ und Farbe auswählen
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures)-1)
        self.color = random.randint(1, len(colors)-1)

#  Drehen und aktuelle Drehung der Figur erhalten
    def image(self):
        return self.figures[self.type][self.rotation]
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

# Spiel mit einige Variable initialisieren
class Tetris:
    level = 1
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 200
    y = 100
    zoom = 20
    figure = None

    def __init__(self, height, width):
#    Konstructeur:
#      height: Höhe des Tetris-Spielfenster
#      Width :  Breit des Tertris-Spielfenster

        self.height = height
        self.width = width
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def transfer_score(self):
        return game.score
# neu Form der Tetris Blöck erstellen
    def new_figure(self):
        self.figure = Figure(3, 0) # an Koordinaten(3,0) positionnieren


    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                                            j + self.figure.x > self.width - 1 or \
                                            j + self.figure.x < 0 or \
                                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

# prüft, ob eine Zeile gebildet wird und diese Zeile zerstört
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1-1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()
# Block nach unten verschieben
    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()
            
#  Diese Funktion wird ausgeführt, sobald der Block den unteren Rand erreicht.
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            game.state = "game_over"

# Block nach rechts oder links verschieben
    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x
# Block drehen
    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


# Spiel initialisieren
pygame.init()

# Einige Farbe definieren
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# size
screen = pygame.display.set_mode((620, 600))

pygame.display.set_caption("Tetris by Josue and Ida")


done = False
clock = pygame.time.Clock()
x = 1
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False


while not done:
    if game.figure is None:
         game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

# Überprufen welche Taste gedrückt wird und die entsprechende Funktion ausführt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False



#     Hintergrund farbe
    screen.fill("Gray")

#
    for i in range(game.height):
        for j in range(game.width):
           pygame.draw.rect(screen, "White", [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 2)

           if game.field[i][j] > 0:
               for z in range(0, game.zoom, 3):
                   pygame.draw.rect(screen, colors[game.field[i][j]],
                                    [game.x + game.zoom * j, game.y + game.zoom * i, z, z], 2)

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    for z in range(0, game.zoom, 3):
                        pygame.draw.rect(screen, colors[game.figure.color],
                                         [game.x + game.zoom * (j + game.figure.x),
                                          game.y + game.zoom * (i + game.figure.y),
                                          z, z], 2)


    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True,   "Black")
    text_game_over = font1.render(("game_over"),True, (255, 125, 0))


    screen.blit(text, [300,0])
    if game.state == "game_over":
        screen.blit(text_game_over, [150, 250])


    pygame.display.flip()

    clock.tick(fps)

pygame.init()