import pygame
pygame.init()

WinX, WinY = 360, 360
window = pygame.display.set_mode((WinX, WinY)) #create 600x600 pxl window
pygame.display.set_caption("LightScape")
run = True
clock = pygame.time.Clock()

# Colours
YELLOW = (255, 255, 1)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#GAME CLASS
class Game():
    def __init__(self):
        self._board = [[0 for x in range(18)] for y in range(18)]  #board to handle data, will be filled with black hole objects/photon object

    def update_photon(self, screen_x, screen_y):
        ''' @:param screen_x : screen x coordinate to be converted to the coordinates on the 18 by 18 array
            @:param screen_y : screen y coordinate to be converted to the coordinates on the 18 by 18 array
            :returns void, updates the photon's location on the board matrix directly
            '''
    # def check_for_game_win(self): work in progress

# PHOTON OBJECT
class photon(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = YELLOW
        self.vel = 20

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius,
                           0)  # I believe 0 means the circle will be completely filled

class blackHole(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, 20, 20)

    def draw(self,window):
        window.blit(pygame.image.load('Blackhole.png'), (self.x, self.y))

def renderScreen():
    window.fill(BLACK)
    light.draw(window)
    for i in range(0, len(blackHoleList)):
        blackHoleList[i].draw(window)
    pygame.display.update()


light = photon(10,10)
blackHoleList = []
for i in range(0,2):
    blackHoleList.append(blackHole(i*40, i*40))

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
                leftBarrier= False
                for i in range(0, len(blackHoleList)): #Collision detection for left collision with blackhole
                    if light.y > (blackHoleList[i].y) and light.y < (blackHoleList[i].y + 20):
                        if light.x - light.radius > blackHoleList[i].x and light.x - light.radius < blackHoleList[
                            i].x + 40:
                            leftBarrier= True
                if not leftBarrier:
                    light.x -= light.vel
                leftBarrier= False
            else:
                pass
            keyReleased = False
        elif keys[pygame.K_RIGHT] == 1:  # x<screenWidth-width(of character)
            if light.x <= WinX - 20:
                rightBarrier = False
                for i in range(0, len(blackHoleList)):
                    if light.y > (blackHoleList[i].y) and light.y < (blackHoleList[i].y + 20):
                        if light.x + light.radius > blackHoleList[i].x - 20 and light.x + light.radius < blackHoleList[
                            i].x + 20:
                            rightBarrier = True
                if not rightBarrier:
                    light.x += light.vel
                rightBarrier = False
            else:
                pass
            keyReleased = False
        elif keys[pygame.K_UP] == 1:
            if light.y >= light.radius * 2:
                bottomBarrier = False
                for i in range(0, len(blackHoleList)):
                    if light.y-light.radius > (blackHoleList[i].y - 20) and light.y-light.radius < (
                        blackHoleList[i].y + 40):
                        print("y")
                        if light.x > blackHoleList[i].x and light.x < blackHoleList[i].x + 20:
                            print("x")
                            bottomBarrier = True
                if not bottomBarrier:
                    light.y -= light.vel
                bottomBarrier = False
            else:
                pass
            keyReleased = False
        elif keys[pygame.K_DOWN] == 1:
            if light.y <= WinY - 20:
                topBarrier = False
                for i in range(0, len(blackHoleList)):
                    if light.y + light.radius > (blackHoleList[i].y - 20) and light.y + light.radius < (
                            blackHoleList[i].y + 20):
                        print("y")
                        if light.x > blackHoleList[i].x and light.x < blackHoleList[i].x + 20:
                            print("x")
                            topBarrier = True
                if not topBarrier:
                    light.y += light.vel
                topBarrier = False
            else:
                pass
            keyReleased = False
    elif keys[pygame.K_LEFT] == 0 and keys[pygame.K_RIGHT] == 0 and keys[pygame.K_UP] == 0 and keys[pygame.K_DOWN] == 0:
        keyReleased= True;

    renderScreen()