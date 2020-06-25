import pygame
import time
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
class Game(object):
    def __init__(self, file):
        self.file = file
        self._board = [[None for x in range(18)] for y in range(18)]  # board to handle data, will be filled with black hole objects/photon object
        x = 0
        with open(self.file) as file: # initialize board from txt file ignoring new lines and spaces.
            for row in self._board:
                self._board[x] = file.readline().rstrip().split(' ')
                x += 1
        for row in range (0, 18):
            for col in range (0, 18):
                if self._board[row][col] == 0: # blackHole, NOT ALLOWED
                    self._board[row][col] = blackHole(row*20, col*20)
                if self._board[row][col] == 1: # EMPTY, SET AS None
                    self._board[row][col] = None
                if self._board[row][col] == 2:  # Photon
                    self._board[row][col] = photon(row*20, col*20)
                #if(self._board[row][col] == 4):
                    #WARP HOLE 1 OBJECT
               # if(self._board[row][col] == 5):
                    #WARP HOLE 2 OBJECT

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
        window.blit(pygame.image.load('images/Blackhole.png'), (self.x, self.y))

class wormHole(object):
    def __init__(self, x, y, direction, pair): #direction (0=can enter, 1=can exit), pair (to match up sets of enter/exit worm holes)
        self.x = x
        self.y = y
        self.direction = direction
        self.pair = pair
        self.hitbox = (self.x, self.y, 20, 20)

    def draw(self,window):
        window.blit(pygame.image.load('images/Wormhole.png'), (self.x, self.y))


def renderScreen():
    window.fill(BLACK)
    for i in range(0, len(blackHoleList)):
        blackHoleList[i].draw(window)
        # wormHoleList[i].draw(window)
    light.draw(window)  # render light after rendering wormholes
    timerText = font1.render('Time Left: ' + str(round(timeLeft)), 1, (255, 0, 0))
    window.blit(timerText, (200, 340))
    pygame.display.update()

# light = photon(10, 10)
blackHoleList = []
wormHoleList = []
game = Game('levels/level1.txt')
for i in game._board:
    print(str(i) + "\n")

for row in range (0, 18):
    for col in range (0, 18):
        if game._board[row][col] == '0':
            blackHoleList.append(blackHole(col * 20, row * 20))
        if game._board[row][col] == '2':
            light = photon(10 + (col * 20), 10 + (row * 20))
        #if(self._board[row][col] == 4):
            #WARP HOLE 1 OBJECT
        # if(self._board[row][col] == 5):
            #WARP HOLE 2 OBJECT
        #if col == '0': # blackHole, NOT ALLOWED
            #blackHoleList.append(blackHole((i.index(n)) * 20, game._board.index(i) * 20))
            #print("spawned BlackHole at " + str(i.index(n) * 20))
        #if n == 2:  # Photon
            #light = photon(n*20, n*20)
        #if(self._board[row][col] == 4):
            #WARP HOLE 1 OBJECT
        # if(self._board[row][col] == 5):
            #WARP HOLE 2 OBJECT

'''
for i in range(0,2): # remove later - just for now to load in blackholes and worm holes
    blackHoleList.append(blackHole((i+1)*40, (i+1)*40))
    wormHoleList.append(wormHole((i+1)*60, (i+1)*80, i, 0)) '''

timeLeft = 20
lastTime = pygame.time.get_ticks()/1000
font1 = pygame.font.SysFont('Comic Sans', 20)

keyReleased = True
lastdirection = None #0 is left, 1 is right, 2 is down 3 is up
count = 0
while run:
    clock.tick(60)
    for event in pygame.event.get(): #ENDS RUN LOOP & CLOSES WINDOW WHEN RED X IS PRESSED
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False

    currentTime = pygame.time.get_ticks()/1000
    timeLeft -= (currentTime-lastTime)
    lastTime = currentTime

    # teleports photon from one wormhole to another
    for i in range(0, len(wormHoleList)):
        if wormHoleList[i].direction == 0:
            if light.x > wormHoleList[i].x and light.x < wormHoleList[i].x + 20:
                if light.y > wormHoleList[i].y and light.y < wormHoleList[i].y + 20:
                    print("teleport!")
                    light.x = 10 + wormHoleList[i + 1].x  # currently the wormhole pair must have adjacent indexcies - maybe we can make it such that it checks the index of the wormhole with the same wormhole.pair number & uses that wormhole's location
                    light.y = 10 + wormHoleList[i + 1].y  # teleports photon to other wormhole

    keys = pygame.key.get_pressed()  # this is a list
    if True:
        if keys[pygame.K_SPACE] == 1:
            lastdirection = None # "brake"/stop moving by clicking space
        if keys[pygame.K_LEFT] == 1 or lastdirection == 0:
            if light.x >= light.radius * 2:
                leftBarrier = False
                for i in range(0, len(blackHoleList)):
                    if light.y > (blackHoleList[i].y) and light.y < (blackHoleList[i].y + 20):
                        if light.x - light.radius > blackHoleList[i].x and light.x - light.radius < blackHoleList[
                            i].x + 40:
                            leftBarrier = True
                            lastdirection = None
                if not leftBarrier:
                    light.x -= light.vel
                    lastdirection = 0
                    time.sleep(0.17)
                leftBarrier = False
            else:
                pass
            keyReleased = False
        elif keys[pygame.K_RIGHT] == 1 or lastdirection == 1:
            if light.x <= WinX - 20:
                rightBarrier = False
                for i in range(0, len(blackHoleList)):
                    if light.y > (blackHoleList[i].y) and light.y < (blackHoleList[i].y + 20):
                        if light.x + light.radius > blackHoleList[i].x - 20 and light.x + light.radius < blackHoleList[i].x + 20:
                            rightBarrier = True
                            lastdirection = None
                if not rightBarrier:
                    light.x += light.vel
                    lastdirection = 1
                    time.sleep(0.17)
                rightBarrier = False
            else:
                pass
            keyReleased = False
        elif keys[pygame.K_UP] == 1 or lastdirection == 2:
            if light.y >= light.radius * 2:
                bottomBarrier = False
                for i in range(0, len(blackHoleList)):
                    if light.y-light.radius > (blackHoleList[i].y - 20) and light.y-light.radius < (
                        blackHoleList[i].y + 40):
                        print("y")
                        if light.x > blackHoleList[i].x and light.x < blackHoleList[i].x + 20:
                            print("x")
                            bottomBarrier = True
                            lastdirection = None
                if not bottomBarrier:
                    light.y -= light.vel
                    lastdirection = 2
                    time.sleep(0.17)
                bottomBarrier = False
            else:
                pass
            keyReleased = False
        elif keys[pygame.K_DOWN] == 1 or lastdirection == 3:
            if light.y <= WinY - 20:
                topBarrier = False
                for i in range(0, len(blackHoleList)):
                    if light.y + light.radius > (blackHoleList[i].y - 20) and light.y + light.radius < (
                            blackHoleList[i].y + 20):
                        print("y")
                        if light.x > blackHoleList[i].x and light.x < blackHoleList[i].x + 20:
                            print("x")
                            topBarrier = True
                            lastdirection = None
                if not topBarrier:
                    light.y += light.vel
                    lastdirection = 3
                    time.sleep(0.17)
                topBarrier = False
            else:
                pass
            keyReleased = False
    elif keys[pygame.K_LEFT] == 0 and keys[pygame.K_RIGHT] == 0 and keys[pygame.K_UP] == 0 and keys[pygame.K_DOWN] == 0:
        keyReleased= True;
    count+=1
    renderScreen()