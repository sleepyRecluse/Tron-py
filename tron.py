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

def drawText(surface, text, fontName, fontSize, color, x, y):
    font = pygame.font.SysFont(fontName, fontSize)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.center = ((x, y))
    surface.blit(textSurface, textRect)

def quitGame():
    pygame.quit()
    quit()

def gameOver():
    gameOverMenu = Menu(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.55, DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.4)
    gameOverMenu.addButton(WHITE, GREEN, BLACK, "Continue", loop)
    gameOverMenu.addButton(WHITE, RED, BLACK, "Quit", quitGame)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        
        drawText(gameDisplay, "Game Over", None, 180, WHITE, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.3)
        gameOverMenu.render(gameDisplay)

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

# Menu
menu = Menu(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, DISPLAY_WIDTH * 0.4, DISPLAY_HEIGHT * 0.6, (35, 35, 35))

def toStartMenu():
    menu.buttons.clear()
    menu.addButton(WHITE, BLUE, BLACK, "Select Mode", toSelectMode)
    menu.addButton(WHITE, GREEN, BLACK, "Settings")
    menu.addButton(WHITE, RED, BLACK, "Quit", quitGame)

def toSelectMode():
    menu.buttons.clear()
    menu.addButton(WHITE, BLUE, BLACK, "PvP", loop)
    menu.addButton(WHITE, GREEN, BLACK, "VS Cpu")
    menu.addButton(WHITE, (220, 220, 220), BLACK, "Skill Test")
    
menu.addButton(WHITE, BLUE, BLACK, "Select Mode", toSelectMode)
menu.addButton(WHITE, GREEN, BLACK, "Settings")
menu.addButton(WHITE, RED, BLACK, "Quit", quitGame)

def screen():
    titleFontSize = 180

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and menu.buttons[0].text == "PvP":
                    toStartMenu()

        gameDisplay.fill(BACKGROUND)
        drawText(gameDisplay, "TRON", None, titleFontSize, WHITE, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 8)
        menu.render(gameDisplay)

        if menu.buttons[0].text == "PvP":
            drawText(gameDisplay, "< Click left arrow to return to start menu > ", None, 22, WHITE, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.9)

        pygame.display.update()
        clock.tick(15)

screen()
quitGame()