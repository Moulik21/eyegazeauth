import pygame
import sys

pygame.init()

window = pygame.display.set_mode((500, 500))
window.fill((255, 255, 255))

class button():
    def __init__(self, color=(0, 0, 255), x=150, y=200, width=200, height=100, text='Authenticate'):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        
        if self.text != '':
            font = pygame.font.SysFont('arial', 20)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

button = button()

def redraw():
    window.fill((255, 255, 255))
    button.draw(window)
    
run = True
while run:
    redraw()
    pygame.display.update()
    
    for event in pygame.event.get():
        mouse = pygame.mouse.get_pos()
        
        if event.type == pygame.QUIT:
            run = False
            quit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.isOver(mouse):
                button.x = button.x + 5
                button.y = button.y + 5
                button.width = button.width - 10
                button.height = button.height - 10
                
        if event.type == pygame.MOUSEBUTTONUP:
            if button.isOver(mouse):
                button.x = button.x - 5
                button.y = button.y - 5
                button.width = button.width + 10
                button.height = button.height + 10
                run = False
                pygame.quit()
                sys.exit(0)
    
