import pygame
import math
from random import choice
import collections

##################### elements #####################

# initialise pygame
pygame.init()

# screen setting
width = 560
height = 620
rows = 30
columns = 28
cell_width = width//columns
cell_height = height//rows
screen = pygame.display.set_mode((width, height))

# variables
running = True
FPS = 60 # frame per second
clock = pygame.time.Clock()
walls = [[5,4,556,15], [4,16,17,614], [15,184,115,394], [16,484,56,515], [543,16,556,615], [445,183,543,396],[504,483,543,516],
        [262,15,295,95], [44,44,115,95], [144,44,235,95], [325,45,415,95], [444,44,515,94], [44,125,116,156], [143,125,175,276],
        [175,184,235,214], [205,124,355,155], [264,156,295,215], [385,125,415,277], [324,184,384,215], [444,124,515,155],
        [144,303,175,395], [383,304,415,395], [205,364,355,395], [263,396,295,456], [145,425,235,455], [324,425,415,455],
        [445,425,515,456], [445,456,476,515], [45,424,115,455], [84,455,115,514], [205,484,355,515], [264,515,295,574],
        [384,485,415,544], [325,544,515,574], [145,484,176,544], [44,544,235,574], [15,604,555,614], [205,244,354,332]]
# pacman initial position info
pacmanXpos = 40
pacmanYpos = 20
pacmanXcha = 0
pacmanYcha = 0
deg = 0
# enimies initial position info
enemyNum = 4
enemyXpos = [400, 120, 300, 180]
enemyYpos = [20, 40, 400, 220]
enemyXcha = [0, 0, 0, 0]
enemyYcha = [0, 0, 0, 0]
WALLS = set()
# initial state
state = "ready"
# initial level
level = 1
# highest score
score = 1000

# fonts
fluoGumsFont = pygame.font.Font("fonts/Fluo Gums.ttf", 32)
bublingFont = pygame.font.Font("fonts/Little Comet Bubling Demo Version.otf", 32)
spiderFont = pygame.font.Font("fonts/The Amazing Spider-Man.ttf", 64)
texatFont = pygame.font.Font("fonts/TEXAT BOLD.otf", 64)

# colors
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

# images 
iconPic = pygame.image.load("images/icon.png")
backgroundPic = pygame.image.load("images/maze2.png")
backgroundPic = pygame.transform.scale(backgroundPic, (width, height))
playerPic = pygame.image.load("images/2020pacman.png")
enemy1Pic = pygame.image.load("images/redenemy2020.png")
enemy2Pic = pygame.image.load("images/yellowenemy2020.png")
enemy3Pic = pygame.image.load("images/redenemy2020.png")
enemy4Pic = pygame.image.load("images/yellowenemy2020.png")
enemies = [enemy1Pic, enemy2Pic, enemy3Pic, enemy4Pic] 

# music
pygame.mixer.music.load("music/pacman_beginning.wav")
walkMus = pygame.mixer.Sound("music/pacman_chomp.wav")
deathMus = pygame.mixer.Sound("music/pacman_death.wav")
nextLvlMus = pygame.mixer.Sound("music/pacman_win.wav")

# set title and icon, play the intro music
pygame.display.set_caption("PAC-MAN")
pygame.display.set_icon(iconPic) 
pygame.mixer.music.play()


##################### functions #####################
def init():
    for p in walls:
        for x in range((p[0]//20) * 20, (p[2]//20)*20 + 1, 20):
            for y in range ((p[1]//20 ) * 20, (p[3]//20)*20 + 1, 20):
                WALLS.add((x,y))
init()

# player movement
def pMove(xPos, yPos, deg):
    ## change pacman position according to the pressed key
    if deg == 180:
        screen.blit(pygame.transform.flip(playerPic, True, False), (xPos, yPos))
    else:
        screen.blit(pygame.transform.rotate(playerPic, deg), (xPos, yPos))   

# enemy movement
# first level (Random movement)
def eMoveLevel1(xPos, yPos,xDir,yDir,i,targetx,targety):
    tmpxDir=0
    tmpyDir=0    
    if xPos%20>0 or yPos%20>0:
        xPos+=xDir
        yPos+=yDir
        screen.blit(enemies[i],(xPos,yPos))
        return xPos,yPos,xDir,yDir
    else:
        xDir=0
        yDir=0
        while True:
            tmpxDir = choice([-20,0,20])
            tmpyDir = choice([-20,0,20])            
            if (tmpxDir!=0 and tmpyDir!=0) or (tmpxDir==0 and tmpyDir==0):continue
            if (xPos+tmpxDir,yPos+tmpyDir) not in WALLS:
                break
        
    if tmpxDir==20:
        xDir=1
    elif tmpxDir==-20:
        xDir=-1
    elif tmpyDir==20:
        yDir=1
    elif tmpyDir==-20:
        yDir=-1
    xPos+=xDir
    yPos+=yDir
    screen.blit(enemies[i],(xPos,yPos))
    return xPos,yPos,xDir,yDir

def eMoveLevel2(xPos, yPos, xDir,yDir,i, targetx, targety):
    tmpxDir=0
    tmpyDir=0    
    if xPos%20>0 or yPos%20>0:
        xPos+=xDir
        yPos+=yDir
        screen.blit(enemies[i],(xPos,yPos))
        return xPos,yPos,xDir,yDir    
    start=(xPos,yPos)
    end = (targetx,targety)
    queue = collections.deque([[start]])
    seen = set([start])    
    while queue:
            path = queue.popleft()
            x, y = path[-1]
            if x==targetx and y==targety:
                if path[1%len(path)][0] > xPos: 
                    tmpxDir=1
                if path[1%len(path)][0] < xPos:
                    tmpxDir=-1
                if path[1%len(path)][1] > yPos: 
                    tmpyDir=1
                if path[1%len(path)][1] < yPos: 
                    tmpyDir=-1
                xPos+=tmpxDir
                yPos+=tmpyDir
                screen.blit(enemies[i], (xPos, yPos))
                return xPos, yPos,tmpxDir,tmpyDir               
            for x2, y2 in ((x+20,y), (x-20,y), (x,y+20), (x,y-20)):
                if (x2,y2) not in WALLS:
                    if (x2,y2) not in seen:
                        seen.add((x2,y2))
                        queue.append(path + [(x2, y2)])
    screen.blit(enemies[i], (xPos,yPos))    
    return xPos, yPos, xDir, yDir 

def eMoveLevel3(xPos, yPos, xDir,yDir,i, targetx, targety):
    tmpxDir=0
    tmpyDir=0    
    if xPos%20>0 or yPos%20>0:
        xPos+=xDir
        yPos+=yDir
        screen.blit(enemies[i],(xPos,yPos))
        return xPos,yPos,xDir,yDir    
    start=(xPos,yPos)
    end = (targetx,targety)
    queue = collections.deque([[start]])
    seen = set([start])    
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if x==targetx and y==targety:
            if path[1%len(path)][0] > xPos: 
                tmpxDir=2
            if path[1%len(path)][0] < xPos:
                tmpxDir=-2
            if path[1%len(path)][1] > yPos: 
                tmpyDir=2
            if path[1%len(path)][1] < yPos: 
                tmpyDir=-2
            xPos+=tmpxDir
            yPos+=tmpyDir
            screen.blit(enemies[i], (xPos, yPos))
            return xPos, yPos,tmpxDir,tmpyDir               
        for x2, y2 in ((x+20,y), (x-20,y), (x,y+20), (x,y-20)):
            if (x2,y2) not in WALLS:
                if (x2,y2) not in seen:
                    seen.add((x2,y2))
                    queue.append(path + [(x2, y2)])
    screen.blit(enemies[i], (xPos,yPos))    
    return xPos, yPos, xDir, yDir 



# enemy kill pacman
def isCollision(pXpos, pYpos, eXpos, eYpos):
    # distance between pacman and the enemy
    distance = math.sqrt(math.pow(pXpos-eXpos, 2)+math.pow(pYpos-eYpos, 2))
    if distance < 20: 
        return True
    return False

# pacman win when enter the red door
def isWin(pXpos, pYpos):
    if 480 <= pXpos+24 <= 505 and 488 <= pYpos+12 <= 506:
        return True
    return False

# show exit door
def exitDoor():
    pygame.draw.rect(screen, red, pygame.Rect(504, 484, 15, 32))

# maze background
def showBackground():
    screen.blit(backgroundPic, (0, 0))
    #for x in range(width//cell_width):
        #pygame.draw.line(backgroundPic, white, (x*cell_width, 0),
                             #(x*cell_width, height))
    #for x in range(height//cell_height):
        #pygame.draw.line(backgroundPic, white, (0, x*cell_height),
                             #(width, x*cell_height))    

# intro backgrund
def readyBackground():
    screen.fill(black)
    t1 = bublingFont.render("Welcome To", True, white)
    t2 = fluoGumsFont.render("PAC-MAN", True, white)
    t3 = fluoGumsFont.render("GAME", True, white)
    t4 = bublingFont.render("Ready? Press space", True, white)
    screen.blit(t1, (204, 140))
    screen.blit(t2, (146, 201))
    screen.blit(t3, (201, 284))
    screen.blit(t4, (162, 384))

# next level background
def nextLevelBackground():
    screen.fill(black)
    t1 = texatFont.render("YOU WON!", True, white)
    t2 = bublingFont.render("Next Level? Press space", True, white)
    screen.blit(t1, (103, 208))
    screen.blit(t2, (146, 325))

# lose background
def loseBackground():
    screen.fill(black)
    t1 = spiderFont.render("YOU LOST", True, white)
    t2 = bublingFont.render("Play again? Press space", True, white)
    screen.blit(t1, (164, 213))
    screen.blit(t2, (146, 325))

def scoreLevelTxt(score, lvl):
    sString = str(score)
    lString = str(lvl)
    t1 = bublingFont.render("Score", True, white)
    t2 = bublingFont.render(sString, True, white)
    t3 = bublingFont.render("Level", True, white)
    t4 = bublingFont.render(lString, True, white)
    screen.blit(t1, (26, 245))
    screen.blit(t2, (27, 302))
    screen.blit(t3, (481, 250))
    screen.blit(t4, (507, 305))

# draw walls
def dWalls():
    for p in walls:
        pygame.draw.rect(screen, red, pygame.Rect(p[0], p[1], p[2]-p[0], p[3]-p[1]))
        
##################### running the game #####################

done = [0,0,0,0]
while running:

    if state == "ready":
        # show intro background
        readyBackground()
        
        # loop on each event (any pressed key)
        for event in pygame.event.get():
            # close the game
            if event.type == pygame.QUIT:
                running = False
            # press space to start the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop() # stop the intro music to start the game
                    state = "start" # change the state to start

    elif state == "start":

        # show background
        showBackground()

        # show exit door
        exitDoor()
        
        # show score and level
        if score > 0:
            score -= 1
        scoreLevelTxt(score, level)

        # loop on each event (any pressed key)
        for event in pygame.event.get():
            # close the game
            if event.type == pygame.QUIT:
                running = False
            # pacman direction  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and (pacmanXpos-20,pacmanYpos) not in WALLS:
                    deg = 180
                    pacmanXpos-=20
                if event.key == pygame.K_RIGHT and (pacmanXpos+20,pacmanYpos) not in WALLS:
                    deg = 0
                    pacmanXpos+=20                    
                if event.key == pygame.K_UP and (pacmanXpos,pacmanYpos-20) not in WALLS:
                    deg = 90
                    pacmanYpos-=20
                if event.key == pygame.K_DOWN and (pacmanXpos,pacmanYpos+20) not in WALLS:
                    deg = 270
                    pacmanYpos+=20

        # pacman movement
        pMove(pacmanXpos, pacmanYpos, deg)

        # enemey movement
        for i in range (enemyNum):
            if level == 1:
                enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i] = eMoveLevel1(
                    enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i], i,pacmanXpos,pacmanYpos)
            elif level == 2:
                enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i] = eMoveLevel2(
                    enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i], i,pacmanXpos,pacmanYpos)
            elif level == 3:
                enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i] = eMoveLevel3(
                    enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i], i,pacmanXpos,pacmanYpos)
            elif level==4:
                if i==2:
                    if enemyXpos[i]==24*20 and enemyYpos[i]==24*20:done[i]=1
                    if done[i]:
                        enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i] = eMoveLevel2(
                        enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i], i,pacmanXpos,pacmanYpos)                                            
                    else:
                        enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i] = eMoveLevel2(
                        enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i], i,24*20,24*20)                    
                elif i==3:
                    if enemyXpos[i]==24*20 and enemyYpos[i]==24*20:done[i]=1
                    if done[i]:
                        enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i] = eMoveLevel2(
                        enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i], i,pacmanXpos,pacmanYpos)                                            
                    else:
                        enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i] = eMoveLevel2(
                        enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i], i,24*20,24*20)                  
                else:
                    enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i] = eMoveLevel3(
                    enemyXpos[i], enemyYpos[i],enemyXcha[i],enemyYcha[i], i,pacmanXpos,pacmanYpos)                    
                        
            ## detect collision
            if (isCollision(pacmanXpos, pacmanYpos, enemyXpos[i], enemyYpos[i])):
                # play the music of loss
                deathMus.play()
                # change the state of the game to lost
                level = 1
                score = 1000
                state = "lost"

        # pacman win
        if (isWin(pacmanXpos, pacmanYpos)):
            nextLvlMus.play()
            deg = 0
            pacmanXpos = 40
            pacmanYpos = 20
            pacmanXcha = 0
            pacmanYcha = 0
            deg = 0
            # enimies initial position info
            enemyNum = 4
            enemyXpos = [400, 120, 300, 180]
            enemyYpos = [20, 40, 400, 220]
            enemyXcha = [0, 0, 0, 0]
            enemyYcha = [0, 0, 0, 0]
            if level < 4:
                score = 1000
                level += 1
            else:
                score = 1000
                level = 1
            state = "next level"

    elif state == "next level":
        
        # show next level background
        nextLevelBackground()

        # loop on each event (any pressed key)
        for event in pygame.event.get():
            # close the game
            if event.type == pygame.QUIT:
                running = False
            # press space to start the game
            if event.type == pygame.KEYDOWN:
                # ---------------------------------
                if event.key == pygame.K_SPACE:
                    state = "start"

    elif state == "lost":

        # show lose background
        loseBackground()

        # loop on each event (any pressed key)
        for event in pygame.event.get():
            # close the game
            if event.type == pygame.QUIT:
                running = False
            # press space to start the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # pacman initial position info
                    pacmanXpos = 40
                    pacmanYpos = 20
                    pacmanXcha = 0
                    pacmanYcha = 0
                    deg = 0
                    # enimies initial position info
                    enemyNum = 4
                    enemyXpos = [400, 120, 300, 180]
                    enemyYpos = [20, 40, 400, 220]
                    enemyXcha = [0, 0, 0, 0]
                    enemyYcha = [0, 0, 0, 0]
                    state = "start"

    # frame rate
    clock.tick(FPS)

    # update the screen every loop
    pygame.display.update()