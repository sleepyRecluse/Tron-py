import pygame

class Bike():
    def __init__(self, x, y, size, color, currDir="UP"):
        # Attributes
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.currDir = currDir

        # Bike Images
        self.upImg = pygame.transform.scale(pygame.image.load(f"./images/{self.color}Bike.png"), (size, size))
        self.downImg = pygame.transform.flip(self.upImg, False, True)

        self.rightImg = pygame.transform.scale(pygame.image.load(f"./images/{self.color}BikeHor.png"), (size, size))
        self.leftImg = pygame.transform.flip(self.rightImg, True, False)

        self.image = self.upImg
        self.bikeRect = self.image.get_rect()

class Block():
    def __init__(self, screen, x, y, color, size=10, image=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.image = image

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.bikeColors = {"red": (221, 34, 0), "orange": (244, 175, 45), "blue": (125, 253, 254)}
    
    def render(self):
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.rect.center = ((self.x, self.y))
        if self.image == None:
            for key in self.bikeColors.keys():
                if key == self.color:
                    pygame.draw.rect(self.screen, self.bikeColors[key], self.rect)
        else:
            self.screen.blit(self.image, self.rect)     

class Player():
    def __init__(self, bike, x, y, color, trailSize, maxBlocks=50):
        self.bike = bike
        self.x = x
        self.y = y
        self.color = color
        self.trailSize = trailSize
        self.maxBlocks = maxBlocks
        
        self.blocks = []

    def addBlock(self, screen):
        if len(self.blocks) != self.maxBlocks:
            self.blocks.append(Block(screen, self.x, self.y, self.color, self.bike.size, self.bike.image))
        else:
            self.blocks.pop(0)
    
    def render(self):
        for block in self.blocks[:-1]:
            block.size = self.trailSize
            block.image = None
            block.render()
        self.blocks[-1].render()

    def checkCollisions(self, oppBlocks, screenSize):
        halfWidth = self.bike.size / 2
        halfHeight = self.bike.size / 2
        if self.x > screenSize[0] - halfWidth or self.x - halfWidth < 0 or self.y > screenSize[1] - halfHeight or self.y - halfHeight < 0:
            return True
        if self.blocks[-1].rect.collidelist(oppBlocks) != -1:
            return True
        return False
    
    def move(self, newDir):
        if newDir == 'UP' and self.bike.currDir != 'DOWN':
            self.bike.currDir = 'UP'
        elif newDir == 'DOWN' and self.bike.currDir != 'UP':
            self.bike.currDir = 'DOWN'
        elif newDir == 'LEFT' and self.bike.currDir != 'RIGHT':
            self.bike.currDir = 'LEFT'
        elif newDir == 'RIGHT' and self.bike.currDir != 'LEFT':
            self.bike.currDir = 'RIGHT'

        if self.bike.currDir == 'UP':
            self.y -= 5
        elif self.bike.currDir == 'DOWN':
            self.y += 5
        elif self.bike.currDir == 'LEFT':
            self.x -= 5
        elif self.bike.currDir == 'RIGHT':
            self.x += 5