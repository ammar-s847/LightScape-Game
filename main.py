import pygame
pygame.init()

WinX, WinY = 360, 360
window = pygame.display.set_mode((WinX, WinY)) # Creates Window
pygame.display.set_caption("LightGame")
run = True
clock = pygame.time.Clock()

# Colours
YELLOW = (255, 255, 1)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# PHOTON OBJECT
class photon(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = YELLOW
        self.vel = 20

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius, 0)

def renderScreen():
    window.fill(BLACK)
    light.draw(window)
    pygame.display.update()


light = photon(10, 10)
keyReleased = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run= False

    keys = pygame.key.get_pressed() # <- This is a List
    if keyReleased:
        if keys[pygame.K_LEFT] == 1:
            if light.x >= light.radius * 2:
                light.x -= light.vel
            else:
                pass
            keyReleased = False
        elif keys[pygame.K_RIGHT] == 1:
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