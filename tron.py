import pygame

pygame.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

BACKGROUND = (20, 20 ,20)
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("TRON")

clock = pygame.time.Clock()
blueBikeImg = pygame.image.load("./images/blueBike.png")

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

def blueBike(x, y):
    gameDisplay.blit(blueBikeImg, (x, y))
BIKE_WIDTH = 64
BIKE_HEIGHT = 64

def drawText(surface, text, fontName, fontSize, color, x, y):
    font = pygame.font.SysFont(fontName, fontSize)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.center = ((x, y))
    surface.blit(textSurface, textRect)
    pygame.display.update()

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
    x = DISPLAY_WIDTH * 0.45
    y = DISPLAY_HEIGHT * 0.8
    x_change = 0
    y_change = 0
    objects.clear()

    # Player death
    derezzed = False

    while not derezzed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:     # move left
                    x_change = -5
                elif event.key == pygame.K_d:   # move right
                    x_change = 5
                elif event.key == pygame.K_w:   # move up
                    y_change = -5
                elif event.key == pygame.K_s:   # move down
                    y_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x_change = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    y_change = 0

        x += x_change
        y += y_change

        gameDisplay.fill(BACKGROUND)
        blueBike(x, y)

        # Player dies if they touch the end 
        if x > DISPLAY_WIDTH - BIKE_WIDTH or x < 0 or y > DISPLAY_HEIGHT - BIKE_HEIGHT or y < 0:
            gameOver()

        pygame.display.update()
        clock.tick(60)

startScreen()
loop()
quitGame()