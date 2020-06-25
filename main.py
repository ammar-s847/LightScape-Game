import pygame
pygame.init()

WinX, WinY = 500, 400
window = pygame.display.set_mode((WinX, WinY)) #create 600x600 pxl window
pygame.display.set_caption("LightGame")
run = True
clock = pygame.time.Clock()

# PHOTON OBJECT
class photon(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = (255, 255, 1)  # yellow
        self.vel = 20

    def draw(self,window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius,
                           0)  # I believe 0 means the circle will be completely filled

def renderScreen():
    window.fill((0,0,0))
    light.draw(window)
    pygame.display.update()


light = photon(10,10)
keyReleased = True
while run:
    clock.tick(60)
    for event in pygame.event.get(): #ENDS RUN LOOP & CLOSES WINDOW WHEN RED X IS PRESSED
        if event.type == pygame.QUIT:
            pygame.quit()
            run= False

    keys = pygame.key.get_pressed()  # this is a list
    if keyReleased:
        if keys[pygame.K_LEFT] == 1:  # if left key is pressed - and is to prevent square moving off screen
            if light.x >= light.radius * 2:
                light.x -= light.vel
            else:
                pass
            keyReleased = False
        elif keys[pygame.K_RIGHT] == 1:  # x<screenWidth-width(of character)
            if light.x <= WinX - 20:
                light.x += light.vel
            else:
                pass
            keyReleased = False
        elif keys[pygame.K_UP] == 1:
            if light.y >= light.radius * 2:
                light.y -= light.vel
            else: 
                pass
            keyReleased = False
        elif keys[pygame.K_DOWN] == 1:
            if light.y <= WinY - 20:
                light.y += light.vel
            else:
                pass
            keyReleased = False
    elif keys[pygame.K_LEFT] == 0 and keys[pygame.K_RIGHT] == 0 and keys[pygame.K_UP] == 0 and keys[pygame.K_DOWN] == 0:
        keyReleased = True;

    renderScreen()