import pygame 

class Button():
    def __init__(self, x, y, width, height, color, activeColor, textColor, text="Button", onClick=None):
        # Attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.activeColor = activeColor
        self.textColor = textColor
        self.text = text
        self.onClick = onClick
        self.clicked = False

        self.buttonFont = pygame.font.SysFont(None, 40)

        # Define button and text surfaces
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.textSurface = self.buttonFont.render(self.text, True, self.textColor)
        
    def render(self, screen):
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

        screen.blit(self.buttonSurface, self.buttonRect)