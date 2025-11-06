import pygame
from player import Player, Bike
from component import Button, Menu

pygame.init()

# Display Dimensions
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

# Constamt Colors
BACKGROUND = (20, 20, 20)
WHITE = (240, 245, 240)
BLACK = (0, 0 , 0)
RED = (185, 45, 45)
GREEN = (45, 180, 45)
BLUE = (125, 253, 254)

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("TRON")

clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load("./images/background.png"), (DISPLAY_WIDTH, DISPLAY_HEIGHT))
backgroundRect = background.get_rect()
backgroundRect.center = ((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2))

bikeSize = 41
trailSize = 11
maxTrailLength = 50

objects = []

# testMenu = Menu(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, 500, 500, RED)

def drawText(surface, text, fontName, fontSize, color, x, y):
    font = pygame.font.SysFont(fontName, fontSize)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.center = ((x, y))
    surface.blit(textSurface, textRect)

def quitGame():
    pygame.quit()
    quit()

# def modeSelect():
#     titleFontSize = 180
#     btnWidth = 300
#     btnHeight = 100
#     btnFontSize = 30

#     objects.clear()

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 quitGame()

#         gameDisplay.fill(BACKGROUND)
#         drawText(gameDisplay, "TRON", None, titleFontSize, WHITE, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 8)
#         btnRect = pygame.Rect(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.55)
#         btnRect.center = ((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2))
#         pygame.draw.rect(gameDisplay, (55, 55, 55), btnRect)
#         pvpBtn = Button(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 3, btnWidth, btnHeight, WHITE, BLUE, BLACK, btnFontSize, "PVP")
#         vsCpuBtn = Button(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, btnWidth, btnHeight, WHITE, GREEN, BLACK, btnFontSize, "VS CPU")
#         backBtn = Button(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT - DISPLAY_HEIGHT / 3, btnWidth, btnHeight, WHITE, RED, BLACK, btnFontSize, "Back", startScreen)

#         objects.append(pvpBtn)
#         objects.append(vsCpuBtn)
#         objects.append(backBtn)

#         for obj in objects:
#             obj.render(gameDisplay)

#         pygame.display.update()
#         clock.tick(15)

def startScreen():
    titleFontSize = 180
    btnWidth = 300
    btnHeight = 100
    btnFontSize = 30

    objects.clear()
    # testMenu.addButton(WHITE, GREEN, BLACK, "1")
    # testMenu.addButton(BLUE, (255, 0, 255), BLACK, "2")
    # testMenu.addButton((150, 150, 150), RED, BLACK, "3")


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

        gameDisplay.fill(BACKGROUND)
        drawText(gameDisplay, "TRON", None, titleFontSize, WHITE, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 8)
        btnRect = pygame.Rect(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.55)
        btnRect.center = ((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2))
        pygame.draw.rect(gameDisplay, (55, 55, 55), btnRect)
        selectModeBtn = Button(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 3, btnWidth, btnHeight, WHITE, BLUE, BLACK, btnFontSize, "Game Modes", loop)
        settingsBtn = Button(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, btnWidth, btnHeight, WHITE, GREEN, BLACK, btnFontSize, "Settings")
        quitBtn = Button(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT - DISPLAY_HEIGHT / 3, btnWidth, btnHeight, WHITE, RED, BLACK, btnFontSize, "Quit Game", quitGame)


        objects.append(selectModeBtn)
        objects.append(settingsBtn)
        objects.append(quitBtn)

        for obj in objects:
            obj.render(gameDisplay)

        pygame.display.update()
        clock.tick(15)

def gameOver():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        objects.clear()
        
        continueButton = Button(DISPLAY_WIDTH * 0.25, DISPLAY_HEIGHT - DISPLAY_HEIGHT / 3, 200, 100, WHITE, GREEN, BLACK, 35, "Continue", loop)
        objects.append(continueButton)

        quitButton = Button(DISPLAY_WIDTH * 0.75, DISPLAY_HEIGHT - DISPLAY_HEIGHT / 3, 200, 100, WHITE, RED, BLACK, 35, "Quit", quitGame)
        objects.append(quitButton)

        for obj in objects:
            obj.render(gameDisplay)

        drawText(gameDisplay, "Game Over", None, 160, WHITE, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
        pygame.display.update()
        clock.tick(15)

def loop():
    objects.clear()
    playerBike = Bike(DISPLAY_WIDTH * 0.45, DISPLAY_HEIGHT * 0.8, bikeSize, "blue")
    oppBike = Bike(DISPLAY_WIDTH * 0.45, DISPLAY_HEIGHT * 0.2, bikeSize, "red")
    player = Player(playerBike, DISPLAY_WIDTH * 0.45, DISPLAY_HEIGHT * 0.8 , "blue", trailSize, maxTrailLength)
    opp = Player(oppBike, DISPLAY_WIDTH * 0.45, DISPLAY_HEIGHT * 0.2, "red", trailSize, maxTrailLength)

    # Player death
    derezzed = False
    newDir = playerBike.currDir 
    oppBike.currDir = "DOWN"
    oppNewDir = oppBike.currDir

    startTime = pygame.time.get_ticks()

    while not derezzed:
        currentTime = pygame.time.get_ticks()
        elapsedTime = (currentTime - startTime) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:                 # move player left
                    newDir = "LEFT"
                    playerBike.image = playerBike.leftImg
                elif event.key == pygame.K_d:               # move player right
                    newDir = "RIGHT"
                    playerBike.image = playerBike.rightImg
                elif event.key == pygame.K_w:               # move player up
                    newDir = "UP"
                    playerBike.image = playerBike.upImg
                elif event.key == pygame.K_s:               # move player down
                    newDir = "DOWN"
                    playerBike.image = playerBike.downImg
                elif event.key == pygame.K_LEFT:            # move opponent left
                    oppNewDir = "LEFT"
                    oppBike.image = oppBike.leftImg
                elif event.key == pygame.K_RIGHT:           # move opponent right
                    oppNewDir = "RIGHT"
                    oppBike.image = oppBike.rightImg
                elif event.key == pygame.K_UP:              # move opponent up
                    oppNewDir = "UP"
                    oppBike.image = oppBike.upImg
                elif event.key == pygame.K_DOWN:            # move opponent down
                    oppNewDir = "DOWN"
                    oppBike.image = oppBike.downImg
                elif event.key == pygame.K_ESCAPE:
                    gameOver()
                
        # Player Movement
        if newDir == 'UP' and playerBike.currDir != 'DOWN':
            playerBike.currDir = 'UP'
        elif newDir == 'DOWN' and playerBike.currDir != 'UP':
            playerBike.currDir = 'DOWN'
        elif newDir == 'LEFT' and playerBike.currDir != 'RIGHT':
            playerBike.currDir = 'LEFT'
        elif newDir == 'RIGHT' and playerBike.currDir != 'LEFT':
            playerBike.currDir = 'RIGHT'

        if playerBike.currDir == 'UP':
            player.y -= 5
        elif playerBike.currDir == 'DOWN':
            player.y += 5
        elif playerBike.currDir == 'LEFT':
            player.x -= 5
        elif playerBike.currDir == 'RIGHT':
            player.x += 5
        
        player.addBlock(gameDisplay)
        
        # Opponent Movement
        if oppNewDir == 'UP' and oppBike.currDir != 'DOWN':
            oppBike.currDir = 'UP'
        elif oppNewDir == 'DOWN' and oppBike.currDir != 'UP':
            oppBike.currDir = 'DOWN'
        elif oppNewDir == 'LEFT' and oppBike.currDir != 'RIGHT':
            oppBike.currDir = 'LEFT'
        elif oppNewDir == 'RIGHT' and oppBike.currDir != 'LEFT':
            oppBike.currDir = 'RIGHT'

        if oppBike.currDir == 'UP':
            opp.y -= 5
        elif oppBike.currDir == 'DOWN':
            opp.y += 5
        elif oppBike.currDir == 'LEFT':
            opp.x -= 5
        elif oppBike.currDir == 'RIGHT':
            opp.x += 5
        
        opp.addBlock(gameDisplay)

        # Rendering
        gameDisplay.blit(background, backgroundRect)
        player.render()
        opp.render()
        drawText(gameDisplay, str(int(elapsedTime)), None, 30, WHITE, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.02)

        # Check Player Collisions
        if player.checkCollisions(opp.blocks, (DISPLAY_WIDTH, DISPLAY_HEIGHT)) or opp.checkCollisions(player.blocks, (DISPLAY_WIDTH, DISPLAY_HEIGHT)):
            gameOver()
        
        pygame.display.update()
        clock.tick(60)

startScreen()
loop()
quitGame()