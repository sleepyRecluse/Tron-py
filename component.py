import pygame 

class Button():
    def __init__(self, x, y, width, height, color, activeColor, textColor, fontSize, text="Button", onClick=None, centered=True):
        # Attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.activeColor = activeColor
        self.textColor = textColor
        self.text = text
        self.fontSize = fontSize
        self.onClick = onClick
        self.clicked = False

        self.buttonFont = pygame.font.SysFont(None, self.fontSize)

        # Define button and text surfaces
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        if centered:
            self.buttonRect.center = ((self.x, self.y))
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

class Menu():
    def __init__(self, x, y, width, height, color = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.buttons = []
        self.surface = pygame.Surface((self.width, self.height))
        if self.color != None:
            self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.rect.center = ((self.x, self.y))

    def addButton(self, color, activeColor, textColor, text, onClick=None):
        if len(self.buttons) == 0:
            btn = Button(self.x, self.y, self.width * 0.8, self.height * 0.8, color, activeColor, textColor, int(self.height / 4), text, onClick)
            self.buttons.append(btn)
        else: 
            top = self.y - self.height / 2
            res = (len(self.buttons) + 2)

            width = self.width * 0.8
            height = (self.height / res) * 0.8
            avalSpace = self.height - height * (res - 1)
            padding = avalSpace / res
            startY = top + padding + height / 2
            
            fontSize = height / 4

            i = 0
            tmp = self.buttons.copy()
            self.buttons.clear()
            for btn in tmp:
                if (i == 0): btn.y = startY 
                else: btn.y = startY + (padding + height) * i
                updBtn = Button(btn.x, btn.y, width, height, btn.color, btn.activeColor, btn.textColor, int(fontSize), btn.text, btn.onClick)
                self.buttons.append(updBtn)
                i += 1
            y = startY + (padding + height) * i 

            btn = Button(self.x, y, width, height, color, activeColor, textColor, int(fontSize), text, onClick)
            self.buttons.append(btn)

    def render(self, screen):
        if self.color != None:
            screen.blit(self.surface, self.rect)

        for btn in self.buttons:
            btn.render(screen)