import pygame
pygame.init()
sW=500
sH=1000
screen=pygame.display.set_mode((sW,sH))
dragon1=pygame.Rect(12,100,100,100)
pygame.display.set_caption("Get The Sword")
play=True
while play:
    dragon_image=pygame.image.load("temp.png")
    dragon=pygame.transform.scale(dragon_image,(99,99))
    screen.blit(dragon,(dragon1.x,dragon1.y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play=False 
    pygame.display.update()
    screen.fill((0,0,0))
pygame.quit()