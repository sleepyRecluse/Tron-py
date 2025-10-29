import pygame

pygame.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

BACKGROUND = (20, 20 ,20)
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Bike / Trail Colors
bikeColors = {"red": (221, 34, 0), "orange": (244, 175, 45), "blue": (125, 253, 254) }

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("TRON")

clock = pygame.time.Clock()

bikeSize = (40, 40)
trailWidth = 10
trailLength = 10
maxTrailSize = 50

objects = []

buttonFont = pygame.font.SysFont(None, 40)

class Button():
    def __init__(self, x, y, width, height, color, activeColor, text="Button", onClick=None):
        # Attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.activeColor = activeColor
        self.text = text
        self.onClick = onClick
        self.clicked = False

        # Define button and text surfaces
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.textSurface = buttonFont.render(self.text, True, BLACK)

        # Appends self to object array for rendering
        objects.append(self)
        
    def render(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.color)
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.activeColor)
            if pygame.mouse.get_pressed()[0] and self.onClick != None:
                self.onClick()

        # Prepares text to be rendered in the center of the button surface
        self.buttonSurface.blit(self.textSurface, [
            self.buttonRect.width / 2 - self.textSurface.get_rect().width / 2,
            self.buttonRect.height / 2 - self.textSurface.get_rect().height / 2
        ])

        gameDisplay.blit(self.buttonSurface, self.buttonRect)

class Bike():
    def __init__(self, x, y, width, height, color, currDir="UP"):
        # Attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.currDir = currDir

        # Bike Images
        self.upImg = pygame.transform.scale(pygame.image.load(f"./images/{self.color}Bike.png"), bikeSize)
        self.downImg = pygame.transform.flip(self.upImg, False, True)

        self.rightImg = pygame.transform.scale(pygame.image.load(f"./images/{self.color}BikeHor.png"), bikeSize)
        self.leftImg = pygame.transform.flip(self.rightImg, True, False)

        self.image = self.upImg

        # Trail array for storing tuples of attributes
        self.trailAttr = []
    
    def render(self):
        for attr in self.trailAttr:
            rect = pygame.Rect(attr[0], attr[1], attr[2], attr[3])
            for key in bikeColors.keys():
                if key == self.color:
                    pygame.draw.rect(gameDisplay, bikeColors[key], rect)
        gameDisplay.blit(self.image, (self.x, self.y))

    def createTrail(self):
        if len(self.trailAttr) != maxTrailSize:
            self.trailAttr.append((self.x + self.width / 3, self.y + self.height / 3, trailWidth, trailLength))
        else:
            self.trailAttr.pop(0)
        

def drawText(surface, text, fontName, fontSize, color, x, y):
    font = pygame.font.SysFont(fontName, fontSize)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.center = ((x, y))
    surface.blit(textSurface, textRect)

def quitGame():
    pygame.quit()
    quit()

def startScreen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

        gameDisplay.fill(BACKGROUND)
        Button(DISPLAY_WIDTH / 9, DISPLAY_HEIGHT - DISPLAY_HEIGHT / 3, 200, 100, WHITE, GREEN, "Play", loop)
        Button(DISPLAY_WIDTH - DISPLAY_WIDTH / 3, DISPLAY_HEIGHT - DISPLAY_HEIGHT / 3, 200, 100, WHITE, RED, "Quit", quitGame)
        for obj in objects:
            obj.render()
        drawText(gameDisplay, "TRON", None, 160, WHITE, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)

        pygame.display.update()
        clock.tick(15)

def gameOver():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

        objects.clear()
        
        Button(DISPLAY_WIDTH / 9, DISPLAY_HEIGHT - DISPLAY_HEIGHT / 3, 200, 100, WHITE, GREEN, "Continue", loop)
        Button(DISPLAY_WIDTH - DISPLAY_WIDTH / 3, DISPLAY_HEIGHT - DISPLAY_HEIGHT / 3, 200, 100, WHITE, RED, "Quit", quitGame)
        for obj in objects:
            obj.render()
        drawText(gameDisplay, "Game Over", None, 160, WHITE, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
        pygame.display.update()
        clock.tick(15)

def loop():
    objects.clear()
    player = Bike(DISPLAY_WIDTH * 0.45, DISPLAY_HEIGHT * 0.8, bikeSize[0], bikeSize[1], "blue")
    opp = Bike(DISPLAY_WIDTH * 0.45, DISPLAY_HEIGHT * 0.2, bikeSize[0], bikeSize[1], "red")

    # Player death
    derezzed = False
    newDir = player.currDir 
    opp.currDir = "DOWN"
    oppNewDir = opp.currDir

    while not derezzed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:             # move player left
                    newDir = "LEFT"
                    player.image = player.leftImg
                elif event.key == pygame.K_d:           # move player right
                    newDir = "RIGHT"
                    player.image = player.rightImg
                elif event.key == pygame.K_w:           # move player up
                    newDir = "UP"
                    player.image = player.upImg
                elif event.key == pygame.K_s:           # move player down
                    newDir = "DOWN"
                    player.image = player.downImg
                elif event.key == pygame.K_LEFT:           # move opponent left
                    oppNewDir = "LEFT"
                    opp.image = opp.leftImg
                elif event.key == pygame.K_RIGHT:           # move opponent right
                    oppNewDir = "RIGHT"
                    opp.image = opp.rightImg
                elif event.key == pygame.K_UP:           # move opponent up
                    oppNewDir = "UP"
                    opp.image = opp.upImg
                elif event.key == pygame.K_DOWN:           # move opponent down
                    oppNewDir = "DOWN"
                    opp.image = opp.downImg
                
        # Player Movement
        if newDir == 'UP' and player.currDir != 'DOWN':
            player.currDir = 'UP'
        elif newDir == 'DOWN' and player.currDir != 'UP':
            player.currDir = 'DOWN'
        elif newDir == 'LEFT' and player.currDir != 'RIGHT':
            player.currDir = 'LEFT'
        elif newDir == 'RIGHT' and player.currDir != 'LEFT':
            player.currDir = 'RIGHT'

        if player.currDir == 'UP':
            player.y -= 5
            player.createTrail()
        elif player.currDir == 'DOWN':
            player.y += 5
            player.createTrail()
        elif player.currDir == 'LEFT':
            player.x -= 5
            player.createTrail()
        elif player.currDir == 'RIGHT':
            player.x += 5
            player.createTrail()
        
        # Opponent Movement
        if oppNewDir == 'UP' and opp.currDir != 'DOWN':
            opp.currDir = 'UP'
        elif oppNewDir == 'DOWN' and opp.currDir != 'UP':
            opp.currDir = 'DOWN'
        elif oppNewDir == 'LEFT' and opp.currDir != 'RIGHT':
            opp.currDir = 'LEFT'
        elif oppNewDir == 'RIGHT' and opp.currDir != 'LEFT':
            opp.currDir = 'RIGHT'

        if opp.currDir == 'UP':
            opp.y -= 5
            opp.createTrail()
        elif opp.currDir == 'DOWN':
            opp.y += 5
            opp.createTrail()
        elif opp.currDir == 'LEFT':
            opp.x -= 5
            opp.createTrail()
        elif opp.currDir == 'RIGHT':
            opp.x += 5
            opp.createTrail()

        gameDisplay.fill(BACKGROUND)  
        player.render()
        opp.render()

        # Player dies if they touch the end 
        if player.x > DISPLAY_WIDTH - player.width or player.x < 0 or player.y > DISPLAY_HEIGHT - player.height or player.y < 0:
            gameOver()
        elif opp.x > DISPLAY_WIDTH - opp.width or opp.x < 0 or opp.y > DISPLAY_HEIGHT - opp.height or opp.y < 0:
            gameOver()

        pygame.display.update()
        clock.tick(60)

startScreen()
loop()
quitGame()