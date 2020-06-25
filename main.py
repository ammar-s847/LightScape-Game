import pygame
pygame.init()

WinX, WinY = 360, 380
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
        
    def display(self):
        global blackHoleList, light
        for row in range (0, 18):
            for col in range (0, 18):
                if self._board[row][col] == '0':
                    blackHoleList.append(blackHole(col * 20, row * 20))
                if self._board[row][col] == '2':
                    light = photon(10 + (col * 20), 10 + (row * 20))

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

class finishLine(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def draw(self,window):
        window.blit(pygame.image.load('images/Finish.png'),(self.x,self.y))

def renderScreen():
    global window, goal, light
    window.fill(BLACK)
    goal.draw(window)
    for i in range(0, len(blackHoleList)):
        blackHoleList[i].draw(window)
        # wormHoleList[i].draw(window)
    light.draw(window)  # render light after rendering wormholes

    pygame.draw.rect(window, (211, 211, 211), (0, 360, 360, 20))
    timerText = font1.render('Time Left: ' + str(round(timeLeft)), 1, (255, 0, 0))
    window.blit(timerText, (265, 365))

    levelText = font1.render('Level: ' + str(level), 1, (255, 0, 0))
    window.blit(levelText, (5, 365))

    pygame.display.update()

light = None
blackHoleList = []
wormHoleList = []
game = Game('levels/level1.txt')
for i in game._board:
    print(str(i) + "\n")

game.display()
# wormHoleList.append(wormHole((i+1)*60, (i+1)*80, i, 0))

goal = finishLine(300,100)

timeLeft = 20
lastTime = pygame.time.get_ticks()/1000
font1 = pygame.font.SysFont('Comic Sans', 20)
level = 1

keyReleased = True
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
                    light.x = 10 + wormHoleList[i + 1].x  # currently the wormhole pair must have adjacent indexcies - maybe we can make it such that it checks the index of the wormhole with the same wormhole.pair number & uses that wormhole's location
                    light.y = 10 + wormHoleList[i + 1].y  # teleports photon to other wormhole

    #when goal is reached
    if light.x > goal.x and light.x < goal.x + 20:
        if light.y > goal.y and light.y < goal.y + 20:
            print("goal reached - congrats!")

    keys = pygame.key.get_pressed()  # this is a list
    if keyReleased:
        if keys[pygame.K_LEFT] == 1:
            if light.x >= light.radius * 2:
                leftBarrier = False
                for i in range(0, len(blackHoleList)):
                    if light.y > (blackHoleList[i].y) and light.y < (blackHoleList[i].y + 20):
                        if light.x - light.radius > blackHoleList[i].x and light.x - light.radius < blackHoleList[
                            i].x + 40:
                            leftBarrier = True
                if not leftBarrier:
                    light.x -= light.vel
                leftBarrier = False
            else:
                pass
            keyReleased = False
        elif keys[pygame.K_RIGHT] == 1:
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
                        if light.x > blackHoleList[i].x and light.x < blackHoleList[i].x + 20:
                            bottomBarrier = True
                if not bottomBarrier:
                    light.y -= light.vel
                bottomBarrier = False
            else:
                pass
            keyReleased = False
        elif keys[pygame.K_DOWN] == 1:
            if light.y <= (WinY-20) - 20:
                topBarrier = False
                for i in range(0, len(blackHoleList)):
                    if light.y + light.radius > (blackHoleList[i].y - 20) and light.y + light.radius < (
                            blackHoleList[i].y + 20):
                        if light.x > blackHoleList[i].x and light.x < blackHoleList[i].x + 20:
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