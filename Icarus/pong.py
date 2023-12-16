import pygame
import math
import random
def runner():
    pygame.init()
    font20 = pygame.font.Font('freesansbold.ttf', 20)
    ballspeed=12
    playerspeed=10
    load=3
    health=3
    DARKRED=(102,0,35)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    GLOW=(39,79,35)
    WIDTH, HEIGHT = 900, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Final Battle")
    clock = pygame.time.Clock()
    FPS = 60
    dragon_closed_image=pygame.image.load("assets/dragonclosed.png")
    dragonclosed=pygame.transform.scale(dragon_closed_image,(60,60))
    dragonclosed=pygame.transform.rotate(dragonclosed,90)
    dragon_open_image=pygame.image.load("assets/dragonopen.png")
    dragonopen=pygame.transform.scale(dragon_open_image,(60,60))
    dragonopen=pygame.transform.rotate(dragonopen,90)
    warrior_image=pygame.image.load("assets/icarus_sword.png")
    warrior=pygame.transform.scale(warrior_image,(100,100))
    fire = pygame.image.load('./images/fire1.png')
    fire = pygame.transform.scale(fire,(26,26))
    win_image=pygame.image.load("assets/win2.png")
    winimage=pygame.transform.scale(win_image,(450,300))
    lose_image=pygame.image.load("assets/lost2.png")
    loseimage=pygame.transform.scale(lose_image,(450,300))
    background=pygame.image.load("assets/battle.png")
    background=pygame.transform.scale(background,(WIDTH,HEIGHT))
    class Player:
        def __init__(self, posx, posy, width, height, speed, color):
            self.posx = posx
            self.posy = posy
            self.width = width
            self.height = height
            self.speed = speed
            self.color = color
            self.geekRect = pygame.Rect(posx, posy, width, height)
            screen.blit(warrior,(self.posx,self.posy))
        def display(self):
            screen.blit(warrior,(self.posx,self.posy))
        def update(self, yFac):
            self.posy = self.posy + self.speed*yFac
            if self.posy <= 0:
                self.posy = 0
            elif self.posy + self.height >= HEIGHT:
                self.posy = HEIGHT-self.height
            self.geekRect = (self.posx, self.posy, self.width, self.height)

        def displayScore(self, text, score, x, y, color):
            text = font20.render(text+str(score), True, color)
            textRect = text.get_rect()
            textRect.center = (x, y)
            screen.blit(text, textRect)
        def getRect(self):
            return self.geekRect
    class Dragon:
        listOfDragons=[]
        fireballLoadlist=[]
        def __init__(self, posx, posy, width, height,health,color,image):
            self.posx = posx
            self.posy = posy
            self.width = width
            self.height = height
            self.color = color
            self.health=health
            self.image=image
            self.geekRect = pygame.Rect(posx, posy, width, height)
            screen.blit(self.image,(self.posx,self.posy))
        def display(self):
            if self in Dragon.listOfDragons:
                screen.blit(self.image,(self.posx,self.posy))

        def displayHealth(self, score,color):
            text = font20.render(str(score), True, color)
            textRect = text.get_rect()
            textRect.center = (self.posx + 30, self.posy-10)

            screen.blit(text, textRect)

        def getRect(self):
            return self.geekRect
    class Ball:
        def __init__(self, posx, posy, radius, speed, color):
            self.posx = posx
            self.posy = posy
            self.radius = radius
            self.speed = speed
            self.color = color
            self.xFac = 1
            self.yFac = -1
            self.ball = pygame.draw.circle(
                screen, self.color, (self.posx, self.posy), self.radius)
            screen.blit(fire,(self.posx,self.posy))
            self.firstTime = 1
        def display(self):
            self.ball = pygame.draw.circle(
                screen, self.color, (self.posx+self.radius, self.posy+self.radius), self.radius)
            screen.blit(fire,(self.posx,self.posy))
        def update(self):
            self.posx += self.speed*self.xFac
            self.posy += round(math.sqrt(ballspeed**2-self.speed**2))*self.yFac
            if self.posy <= 0 or self.posy+26 >= HEIGHT:
                self.yFac *= -1

            if self.posx <= 0 and self.firstTime:
                self.firstTime = 0
                return -1
            elif self.posx >= WIDTH and self.firstTime:
                self.firstTime = 0
                return 1
        def reset(self):
            dra=0
            if load+1:
                dra=random.randint(0,load)
            self.posx = 100
            for dragon in Dragon.listOfDragons:
                if dra==Dragon.listOfDragons.index(dragon):
                    dragon.image=dragonopen
                else:
                    dragon.image=dragonclosed
            self.posy = Dragon.fireballLoadlist[dra]
            self.xFac = 1
            self.firstTime = 1
            self.speed=random.randint(int(ballspeed/1.5),ballspeed)
            return dra
        def hit(self):
            self.xFac *= -1
        def revenge(self):
            dra=0
            if load+1:
                dra=random.randint(0,load)
            self.posx = 100
            for dragon in Dragon.listOfDragons:
                if dra==Dragon.listOfDragons.index(dragon):
                    dragon.image=dragonopen
                else:
                    dragon.image=dragonclosed
            self.posy = Dragon.fireballLoadlist[dra]
            self.firstTime = 1
            self.xFac *= -1
            self.speed=random.randint(int(ballspeed/1.5),ballspeed)
        def getRect(self):
            return self.ball
    cover=True
    replay=True
    while replay:
        Dragon.fireballLoadlist=[]
        Dragon.listOfDragons=[]
        load=3
        running = True
        win=False
        lose=False
        dragon1 = Dragon(20, 40, 50, 50, health, GREEN,dragonclosed)
        dragon2 = Dragon(20, 190, 50, 50,health, GREEN,dragonclosed)
        dragon3 = Dragon(20, 340, 50, 50,health, GREEN,dragonclosed)
        dragon4 = Dragon(20, 490, 50, 50,health, GREEN,dragonclosed)
        icarus = Player(WIDTH-120, 0, 10, 100, playerspeed, GREEN)
        Dragon.fireballLoadlist.extend([65,65+150,65+300,65+450])
        ball = Ball(WIDTH//2-200, Dragon.fireballLoadlist[random.randint(0,load)], 13, random.randint(int(ballspeed/1.5),ballspeed), WHITE)
        Dragon.listOfDragons.extend([ dragon1,dragon2,dragon3,dragon4])
        icarusScore = 5
        icarusYFac = 0
        title_image=pygame.image.load("images/battle.png")
        while cover:
            screen.blit(title_image,(0,0))
            events =pygame.event.get()
            for even in events:
                if even.type == pygame.QUIT:
                        cover=False
                        replay=False
                        running=False
                        win=False
                        run=False
                if even.type == pygame.KEYDOWN:
                    if even.key == pygame.K_RETURN:
                        cover=False   
            pygame.display.flip()
        while running:
            screen.blit(background,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    replay=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        icarusYFac = -1
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        icarusYFac = 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        icarusYFac = 0
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        icarusYFac = 0
            hit=0
            for dragon in Dragon.listOfDragons:
                if pygame.Rect.colliderect(ball.getRect(), dragon.getRect()):
                    hit=Dragon.listOfDragons.index(dragon)+1
            if pygame.Rect.colliderect(ball.getRect(), icarus.getRect()):
                    ball.hit()
            if hit:
                Dragon.listOfDragons[hit-1].health-=1
            for dragon in Dragon.listOfDragons:
                if dragon.health==0:
                    for i in Dragon.fireballLoadlist:
                        if i==(dragon.posy+25):
                            Dragon.fireballLoadlist.remove(i)
                    Dragon.listOfDragons.remove(dragon)
                    load-=1
            if not Dragon.listOfDragons:
                running=False
                win=True
                victory=True
            icarus.update(icarusYFac)
            point = ball.update()       
            if point == 1:
                icarusScore -= 1
            if icarusScore == 0:
                running=False
                lose=True
                loss=True
            if hit and load+1:
                ball.revenge()
            if point:
                ball.reset()
            dragon1.display()
            dragon2.display()
            dragon3.display()
            dragon4.display()
            icarus.display()
            ball.display()
            icarus.displayScore("Health : ",
                            icarusScore, WIDTH-100, 20, GLOW)
            if Dragon.listOfDragons:
                for dragon in Dragon.listOfDragons:
                    dragon.displayHealth(dragon.health, DARKRED)

            pygame.display.update()
            clock.tick(FPS)
        while win:
            for even in pygame.event.get():
                if even.type == pygame.QUIT:
                    win=False 
                    replay=False
                if even.type == pygame.KEYDOWN:
                    if even.key == pygame.K_RETURN:
                        win=False
            screen.blit(winimage,(225,150))    
            pygame.display.flip()
        while lose:
            for even in pygame.event.get():
                if even.type == pygame.QUIT:
                    lose=False
                    replay=False 
                if even.type == pygame.KEYDOWN:
                    if even.key == pygame.K_RETURN:
                        lose=False
            screen.blit(loseimage,(225,150))    
            pygame.display.flip()
#runner()