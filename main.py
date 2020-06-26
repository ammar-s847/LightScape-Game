import pygame
import time

pygame.mixer.pre_init(44100, 16, 2, 2048)
pygame.init()

WinX, WinY = 360, 380
window = pygame.display.set_mode((WinX, WinY))
pygame.display.set_caption("LightScape")
run = True
clock = pygame.time.Clock()

# Colours
YELLOW = (255, 255, 1)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# GAME CLASS
class Game(object):
    def __init__(self, file):
        self.file = file
        self._board = [[None for x in range(18)] for y in
                       range(18)]  # board to handle data, will be filled with black hole objects/photon object
        x = 0
        with open(self.file) as file:  # initialize board from txt file ignoring new lines and spaces.
            for row in self._board:
                self._board[x] = file.readline().rstrip().split(' ')
                x += 1
            # timeLeft Variable
            readLine = file.readline().rstrip()
            if 'time:' in readLine:
                self.timeLeft = int(readLine[5:])

    def display(self):
        global blackHoleList, light, goal, timeLeft
        timeLeft = self.timeLeft
        for row in range(0, 18):
            for col in range(0, 18):
                if self._board[row][col] == '0':
                    blackHoleList.append(blackHole(col * 20, row * 20))
                if self._board[row][col] == '2':
                    light = photon(10 + (col * 20), 10 + (row * 20))
                if self._board[row][col] == '3':
                    goal = finishLine(col * 20, row * 20)
                if self._board[row][col] == '4':
                    wormHoleList.append(wormHole(col * 20, row * 20, 0, 0))
                if self._board[row][col] == '5':
                    wormHoleList.append(wormHole(col * 20, row * 20, 1, 0))
                if self._board[row][col] == '6':
                    wormHoleList.append(wormHole(col * 20, row * 20, 0, 1))
                if self._board[row][col] == '7':
                    wormHoleList.append(wormHole(col * 20, row * 20, 1, 1))

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

    def draw(self, window):
        window.blit(pygame.image.load('images/Blackhole.png'), (self.x, self.y))


class wormHole(object):
    def __init__(self, x, y, direction,
                 pair):  # direction (0=can enter, 1=can exit), pair (to match up sets of enter/exit worm holes)
        self.x = x
        self.y = y
        self.direction = direction
        self.pair = pair
        self.hitbox = (self.x, self.y, 20, 20)

    def draw(self, window):
        window.blit(pygame.image.load('images/Wormhole.png'), (self.x, self.y))


class finishLine(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        window.blit(pygame.image.load('images/Finish.png'), (self.x, self.y))

def renderScreen():
    global window, goal, light
    window.fill(BLACK)
    goal.draw(window)
    for i in range(0, len(blackHoleList)):
        blackHoleList[i].draw(window)
    for i in range(0,len(wormHoleList)):
        wormHoleList[i].draw(window)
    light.draw(window)  # render light after rendering wormholes

    pygame.draw.rect(window, (211, 211, 211), (0, 360, 360, 20))
    timerText = font1.render('Time Left: ' + str(round(timeLeft)), 1, (255, 0, 0))
    window.blit(timerText, (265, 365))

    levelText = font1.render('Level: ' + str(level), 1, (255, 0, 0))
    window.blit(levelText, (5, 365))

    livetxt = font1.render('Energy: ' + str(lives), 1, (255,0,0))
    window.blit(livetxt, (100, 365))
    pygame.display.update()

    pygame.display.update()

# Music
try:
    music = pygame.mixer.music.load("sounds/8bit_music.mp3")
    pygame.mixer.music.play(-1)
except:
    music = None

# Game Variables
lives = 20
light = None
goal = None
blackHoleList = []
wormHoleList = []
game = Game('levels/level1.txt')
for i in game._board:
    print(str(i) + "\n")

game.display()

timeLeft = game.timeLeft
lastTime = pygame.time.get_ticks() / 1000
font1 = pygame.font.SysFont('Comic Sans', 20)
level = 1
winningLevel = 8 # One above final level number

keyReleased = True
lastdirection = None
while run:
    if (lives == 0) or (timeLeft <= 0):
        window.fill(WHITE)
        font2 = pygame.font.SysFont('Comic Sans', 60)
        winText = font2.render('YOU LOST :(', 1, BLACK)
        window.blit(winText, (60, 100))
        pygame.display.update()
        print("You Lost!")
        if music: pygame.mixer.music.stop()
        time.sleep(5)
        break
    
    clock.tick(60)
    
    for event in pygame.event.get():  # Ends Game loop and quits program
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False

    currentTime = pygame.time.get_ticks() / 1000
    timeLeft -= (currentTime - lastTime)
    lastTime = currentTime

    # teleports photon from one wormhole to another
    for i in range(0, len(wormHoleList)):
        if wormHoleList[i].direction == 0:
            if light.x > wormHoleList[i].x and light.x < wormHoleList[i].x + 20:
                if light.y > wormHoleList[i].y and light.y < wormHoleList[i].y + 20:
                    for j in range(0,len(wormHoleList)):
                        if wormHoleList[j].pair == wormHoleList[i].pair and wormHoleList[j].direction == 1:
                            light.x = 10 + wormHoleList[j].x
                            light.y = 10 + wormHoleList[j].y  # teleports photon to other wormhole

    # when goal is reached
    if light.x > goal.x and light.x < goal.x + 20:
        if light.y > goal.y and light.y < goal.y + 20:
            print(f"Level {level} Complete - congrats!")
            level += 1
            lives += 10 # regain 10 lives after each level
            if level == winningLevel: # <- one level above the final level number.
                window.fill(WHITE)
                font2 = pygame.font.SysFont('Comic Sans', 60)
                winText = font2.render('YOU WIN!!!', 1, BLACK)
                window.blit(winText, (60, 100))
                pygame.display.update()
                if music: pygame.mixer.music.stop()
                time.sleep(5)
                break
                run = False
            game = Game('levels/level' + str(level) + '.txt')
            timeLeft = None
            blackHoleList.clear()
            wormHoleList.clear()
            game.display()

    keys = pygame.key.get_pressed()  # this is a list
    if True:
        if keys[pygame.K_SPACE] == 1:
            lastdirection = None  # "brake"/stop moving by clicking space
        if keys[pygame.K_LEFT] == 1 or lastdirection == 0:
            if light.x >= light.radius * 2:
                leftBarrier = False
                for i in range(0, len(blackHoleList)):
                    if light.y > (blackHoleList[i].y) and light.y < (blackHoleList[i].y + 20):
                        if light.x - light.radius > blackHoleList[i].x and light.x - light.radius < blackHoleList[i].x + 40:
                            leftBarrier = True
                            lastdirection = None
                            lives -= 1 
                if not leftBarrier:
                    light.x -= light.vel
                    lastdirection = 0
                    time.sleep(0.07)
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
                            lives -= 1
                if not rightBarrier:
                    light.x += light.vel
                    lastdirection = 1
                    time.sleep(0.07)
                rightBarrier = False
            else:
                pass
            keyReleased = False
        elif keys[pygame.K_UP] == 1 or lastdirection == 2:
            if light.y >= light.radius * 2:
                bottomBarrier = False
                for i in range(0, len(blackHoleList)):
                    if light.y - light.radius > (blackHoleList[i].y - 20) and light.y - light.radius < (blackHoleList[i].y + 40):
                        # print("y")
                        if light.x > blackHoleList[i].x and light.x < blackHoleList[i].x + 20:
                            # print("x")
                            bottomBarrier = True
                            lastdirection = None
                            lives -= 1
                if not bottomBarrier:
                    light.y -= light.vel
                    lastdirection = 2
                    time.sleep(0.07)
                bottomBarrier = False
            else:
                pass
            keyReleased = False
        elif keys[pygame.K_DOWN] == 1 or lastdirection == 3:
            if light.y <= WinY - 40:
                topBarrier = False
                for i in range(0, len(blackHoleList)):
                    if light.y + light.radius > (blackHoleList[i].y - 20) and light.y + light.radius < (
                            blackHoleList[i].y + 20):
                        # print("y")
                        if light.x > blackHoleList[i].x and light.x < blackHoleList[i].x + 20:
                            # print("x")
                            topBarrier = True
                            lastdirection = None
                            lives -= 1
                if not topBarrier:
                    light.y += light.vel
                    lastdirection = 3
                    time.sleep(0.07)
                topBarrier = False
            else:
                pass
            keyReleased = False
    elif keys[pygame.K_LEFT] == 0 and keys[pygame.K_RIGHT] == 0 and keys[pygame.K_UP] == 0 and keys[pygame.K_DOWN] == 0:
        keyReleased = True;
    renderScreen()