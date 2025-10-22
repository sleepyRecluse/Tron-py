import pygame

pygame.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("TRON")

clock = pygame.time.Clock()
blueBikeImg = pygame.image.load("./images/blueBike.png")

def blueBike(x, y):
    gameDisplay.blit(blueBikeImg, (x, y))
BIKE_WIDTH = 64
BIKE_HEIGHT = 64

def loop():
    x = DISPLAY_WIDTH * 0.45
    y = DISPLAY_HEIGHT * 0.8
    x_change = 0
    y_change = 0

    # Player death
    derezzed = False

    while not derezzed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                derezzed = True

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

        gameDisplay.fill((255, 255, 255))
        blueBike(x, y)

        # Player dies if they touch the end 
        if x > DISPLAY_WIDTH - BIKE_WIDTH or x < 0 or y > DISPLAY_HEIGHT - BIKE_HEIGHT or y < 0:
            derezzed = True

        pygame.display.update()
        clock.tick(60)

loop()
pygame.quit()
quit()