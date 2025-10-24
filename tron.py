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

class Bike():
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
    
    def render(self):
        gameDisplay.blit(self.image, (self.x, self.y))

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
    player = Bike(DISPLAY_WIDTH * 0.45, DISPLAY_HEIGHT * 0.8, 60, 60, blueBikeImg)
    x_change = 0
    y_change = 0

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

        player.x += x_change
        player.y += y_change

        gameDisplay.fill(BACKGROUND)
        player.render()

        # Player dies if they touch the end 
        if player.x > DISPLAY_WIDTH - player.width or player.x < 0 or player.y > DISPLAY_HEIGHT - player.height or player.y < 0:
            gameOver()

        pygame.display.update()
        clock.tick(60)

startScreen()
loop()
quitGame()