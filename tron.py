import pygame
from player import Player, Bike
from component import Button, VerticalMenu, HorizontalMenu

pygame.init()

# Display Dimensions
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

# Constant Colors
colors = {
    "background": (20, 20, 20),
    "white": (240, 245, 240),
    "black": (0, 0 , 0),
    "red": (185, 45, 45),
    "green": (45, 180, 45),
    "blue": (125, 253, 254),
    "orange": (255, 89, 0)
}

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("TRON")

clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load("./images/background.png"), (DISPLAY_WIDTH, DISPLAY_HEIGHT))
backgroundRect = background.get_rect()
backgroundRect.center = ((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2))

bikeSize = 35
trailSize = 11
maxTrailLength = 50

fontRegular = "./fonts/ScienceGothic-Regular.ttf"
fontThin = "./fonts/ScienceGothic_Condensed-Light.ttf"

objects = []

def drawText(surface, text, fontName, fontSize, color, x, y, centered=True):
    font = pygame.font.Font(fontName, fontSize)

    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    
    if centered:
        textRect.center = ((x, y))
    else:
        textRect.x = x
        textRect.y = y

    surface.blit(textSurface, textRect)

def quitGame():
    pygame.quit()
    quit()

def gameOver():
    gameOverMenu = VerticalMenu(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.55, DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.4)
    gameOverMenu.addButton(colors["white"], colors["green"], colors["black"], "Continue", loop)
    gameOverMenu.addButton(colors["white"], colors["orange"], colors["black"], "Select Mode", screen)
    gameOverMenu.addButton(colors["white"], colors["red"], colors["black"], "Quit", quitGame)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        
        drawText(gameDisplay, "Game Over", None, 180, colors["white"], DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.3)
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
        player.move(newDir)
        player.addBlock(gameDisplay)
        
        # Opponent Movement
        opp.move(oppNewDir)
        opp.addBlock(gameDisplay)

        # Rendering
        gameDisplay.blit(background, backgroundRect)
        player.render()
        opp.render()
        drawText(gameDisplay, str(int(elapsedTime)), None, 30, colors["white"], DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.02)

        # Check Player Collisions
        if player.checkCollisions(opp.blocks, (DISPLAY_WIDTH, DISPLAY_HEIGHT)) or opp.checkCollisions(player.blocks, (DISPLAY_WIDTH, DISPLAY_HEIGHT)):
            gameOver()
        
        pygame.display.update()
        clock.tick(60)

def settings():
    # Control Settings
    wasdBtn = Button(DISPLAY_WIDTH * 0.335, DISPLAY_HEIGHT * 0.175, 220, 50, colors["white"], colors["blue"], colors["black"], 26, "WASD", None, False)
    arrowBtn = Button(DISPLAY_WIDTH * 0.66, DISPLAY_HEIGHT * 0.175, 220, 50, colors["white"], colors["blue"], colors["black"], 26, "Arrow Keys", None, False)

    # Player Speed Settings
    plySpeedMenu = HorizontalMenu(DISPLAY_WIDTH * 0.635, DISPLAY_HEIGHT * 0.3, DISPLAY_WIDTH * 0.7, DISPLAY_HEIGHT * 0.075)
    plySpeedMenu.addButton(colors["white"], colors["blue"], colors["black"], "Slow")
    plySpeedMenu.addButton(colors["white"], colors["blue"], colors["black"], "Normal")
    plySpeedMenu.addButton(colors["white"], colors["blue"], colors["black"], "Fast")

    # Opponent Speed Settings
    oppSpeedMenu = HorizontalMenu(DISPLAY_WIDTH * 0.635, DISPLAY_HEIGHT * 0.4, DISPLAY_WIDTH * 0.7, DISPLAY_HEIGHT * 0.075)
    oppSpeedMenu.addButton(colors["white"], colors["blue"], colors["black"], "Slow")
    oppSpeedMenu.addButton(colors["white"], colors["blue"], colors["black"], "Normal")
    oppSpeedMenu.addButton(colors["white"], colors["blue"], colors["black"], "Fast")

    # Player Color Settings
    plyColorMenu = HorizontalMenu(DISPLAY_WIDTH * 0.635, DISPLAY_HEIGHT * 0.5, DISPLAY_WIDTH * 0.7, DISPLAY_HEIGHT * 0.075)
    plyColorMenu.addButton(colors["white"], colors["blue"], colors["black"], "Blue")
    plyColorMenu.addButton(colors["white"], colors["orange"], colors["black"], "Orange")
    plyColorMenu.addButton(colors["white"], colors["red"], colors["black"], "Red")

    # Opponent Color Settings
    oppColorMenu = HorizontalMenu(DISPLAY_WIDTH * 0.635, DISPLAY_HEIGHT * 0.6, DISPLAY_WIDTH * 0.7, DISPLAY_HEIGHT * 0.075)
    oppColorMenu.addButton(colors["white"], colors["blue"], colors["black"], "Blue")
    oppColorMenu.addButton(colors["white"], colors["orange"], colors["black"], "Orange")
    oppColorMenu.addButton(colors["white"], colors["red"], colors["black"], "Red")

    # Time Settings
    timeMenu = HorizontalMenu(DISPLAY_WIDTH * 0.635, DISPLAY_HEIGHT * 0.7, DISPLAY_WIDTH * 0.7, DISPLAY_HEIGHT * 0.075)
    timeMenu.addButton(colors["white"], colors["blue"], colors["black"], "30 Secs")
    timeMenu.addButton(colors["white"], colors["blue"], colors["black"], "60 Secs")
    timeMenu.addButton(colors["white"], colors["blue"], colors["black"], "No Limit")

    btns = [wasdBtn, arrowBtn]
    menus = [plySpeedMenu, oppSpeedMenu, plyColorMenu, oppColorMenu, timeMenu]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    screen()
        
        gameDisplay.fill(colors["background"])
        drawText(gameDisplay, "Settings", fontRegular, 90, colors["white"], DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.08)
        drawText(gameDisplay, "Player Controls", fontThin, 28, colors["white"], DISPLAY_WIDTH * 0.065, DISPLAY_HEIGHT * 0.178, False)
        drawText(gameDisplay, "Player Speed", fontThin, 28, colors["white"], DISPLAY_WIDTH * 0.065, DISPLAY_HEIGHT * 0.278, False)
        drawText(gameDisplay, "Opponent Speed", fontThin, 28, colors["white"], DISPLAY_WIDTH * 0.065, DISPLAY_HEIGHT * 0.378, False)
        drawText(gameDisplay, "Player Color", fontThin, 28, colors["white"], DISPLAY_WIDTH * 0.065, DISPLAY_HEIGHT * 0.478, False)
        drawText(gameDisplay, "Opponent Color", fontThin, 28, colors["white"], DISPLAY_WIDTH * 0.065, DISPLAY_HEIGHT * 0.578, False)
        drawText(gameDisplay, "Time Limit", fontThin, 28, colors["white"], DISPLAY_WIDTH * 0.065, DISPLAY_HEIGHT * 0.678, False)
        
        for btn in btns:
            btn.render(gameDisplay)

        for m in menus:
            m.render(gameDisplay)

        drawText(gameDisplay, "< Click left arrow to return to start menu >", fontThin, 20, colors["white"], DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.9)
        
        pygame.display.update()
        clock.tick(15)
        

# Menu
menu = VerticalMenu(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.55, DISPLAY_WIDTH * 0.4, DISPLAY_HEIGHT * 0.6, (35, 35, 35))

def toStartMenu():
    menu.buttons.clear()
    menu.addButton(colors["white"], colors["blue"], colors["black"], "Select Mode", toSelectMode)
    menu.addButton(colors["white"], colors["green"], colors["black"], "Settings", settings)
    menu.addButton(colors["white"], colors["red"], colors["black"], "Quit", quitGame)

def toSelectMode():
    menu.buttons.clear()
    menu.addButton(colors["white"], colors["blue"], colors["black"], "PvP", loop)
    menu.addButton(colors["white"], colors["green"], colors["black"], "VS Cpu")
    menu.addButton(colors["white"], (175, 125, 0), colors["black"], "Skill Test")

menu.addButton(colors["white"], colors["blue"], colors["black"], "Select Mode", toSelectMode)
menu.addButton(colors["white"], colors["green"], colors["black"], "Settings", settings)
menu.addButton(colors["white"], colors["red"], colors["black"], "Quit", quitGame)

def screen():
    titleFontSize = 140

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and menu.buttons[0].text == "PvP":
                    toStartMenu()

        gameDisplay.fill(colors["background"])
        drawText(gameDisplay, "TRON", fontRegular, titleFontSize, colors["white"], DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.125)
        menu.render(gameDisplay)

        if menu.buttons[0].text == "PvP":
            drawText(gameDisplay, "< Click left arrow to return to start menu >", fontThin, 20, colors["white"], DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.9)

        pygame.display.update()
        clock.tick(15)

screen()
quitGame()