from turtle import update
import pygame

color = pygame.Color

#set the colors
BLUE = color("blue")
RED = color("red")
GREEN = color("green")
WHITE = color("white")
BLACK = color("black")
# set the speed of the frames
FPS = 60

class TextBox(pygame.Rect):
    
    #initialize the attributes of the text box
    def __init__(self,*args) -> None:
        super().__init__(*args)
        self.text = ""  
        self.textBox = Font.render(self.text,True,WHITE)
        self.active = False
        self.hover = False
        self.activeColor,self.hoverColor,self.normalColor = GREEN,RED,BLUE
    #set the colors
    def setColors(self,active,hover,normal):
        self.activeColor = active
        self.hoverColor = hover
        self.normalColor = normal
    #set the title
    def setTitle(self,title):
        self.title = title
        self.titleBox = titleFont.render(self.title,True,WHITE)
    #get the colors based on activities
    def get_color(self):
        return self.activeColor if self.active else self.normalColor if not self.hover else self.hoverColor

    def on_click(self,otherBox):
        if not self.collidepoint(mouse.get_pos()):
            self.active = False
            return
        if otherBox.active:
            otherBox.active = False
        self.active = True
    
    def on_hover(self):
        if not self.collidepoint(mouse.get_pos()):
            self.hover = False
            return
        self.hover = True
    #update the text
    def update_text(self,event):
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.textBox = Font.render(self.text,True,WHITE)

                return
            if self.w > self.textBox.get_width() + 10:
                self.text += event.unicode
        self.textBox = Font.render(self.text,True,WHITE)
    #renders text and rects on screen
    def render(self):
        pygame.draw.rect(window,self.get_color(),self,2)
        window.blit(self.textBox,(self.x+5,self.y+10))
        window.blit(self.titleBox,(self.x,self.y-40))



class PassBox(TextBox):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.starText = ""
    
    def update_text(self,event):
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.starText = "*" * len(self.text)
                self.textBox = Font.render(self.starText,True,WHITE)
                return
            if self.w > self.textBox.get_width() + 10:
                self.text += event.unicode
            
        self.starText = "*" * len(self.text)
        self.textBox = Font.render(self.starText,True,WHITE)


pygame.init()

Font = pygame.font.Font(None,28)
titleFont = pygame.font.Font(None,32)

SPECIAL_KEYS = (pygame.K_ESCAPE,pygame.K_RETURN,pygame.K_DELETE,pygame.K_TAB,pygame.K_CAPSLOCK,
                pygame.K_LSHIFT,pygame.K_RSHIFT,pygame.K_LCTRL,pygame.K_RCTRL)

display = pygame.display

WIDTH,HEIGHT = 600,600

window = display.set_mode((WIDTH,HEIGHT))
display.set_caption("Login")

mouse = pygame.mouse

pygame.key.set_repeat(320)


def main():
    open = True

    user_box = TextBox(200,200,200,40)
    user_box.setTitle("Benutzername")

    pass_box = PassBox(200,300,200,40)
    pass_box.setTitle("Passwort")

    clock = pygame.time.Clock()

    while open:
        clock.tick(FPS)
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    open = False
                    pygame.quit()
                    return
                case pygame.MOUSEBUTTONUP:
                    user_box.on_click(pass_box)
                    pass_box.on_click(user_box)          

                case pygame.MOUSEMOTION:
                    user_box.on_hover()
                    pass_box.on_hover()  
                
                case pygame.KEYUP:
                    pass
                    if event.key == pygame.K_ESCAPE:
                        user_box.active = False
                        pass_box.active = False
                
                case pygame.KEYDOWN:
                    if event.key in SPECIAL_KEYS:
                        continue
                    
                    user_box.update_text(event)
                    pass_box.update_text(event)

        window.fill(BLACK)
        user_box.render()
        pass_box.render()
        display.update()

                    


if __name__ == "__main__":
    main()
else:
    raise Exception("This file doesnt support imports. Please run the file itself with 'python main.py'")
