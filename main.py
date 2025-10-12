import pygames
pygame.init()
screen =pygame.display.set_mode((958,554))
pygame.display.set_caption("SwordDeul")
pygame.display.set_icon(pygame.image.load("knight.png"))
background = pygame.image.load("Inmost - metroidvania exploring game in development - Alexey Testov.gif")

#this the main window of the game
while True:
    #background image
    screen.blit(background,(0,0))
    #basic input to close the window by the player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    pygame.display.update()
