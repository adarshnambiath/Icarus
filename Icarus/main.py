import pygame
from pygame.locals import *
from pygame import sprite
from pygame import quit as q
from pygame.sprite import Group
def runner():
    global win 
    win=False
    tile_size = 50

    game_over = 0

    #to start py gmae 
    pygame.init()

    clock = pygame.time.Clock()
    fps = 60 

    #size of game window 

    screen_width = 1000
    screen_height = 900

    #display screen
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("Level 3")



    #loading images
    bg_img = pygame.image.load('images/bg.png')
    # sun_img = pygame.image.load('./images/sun.png')
    # bg_img = pygame.image.load('./images/sky.png')
    
    
    restart_button1 = pygame.image.load('./images/restart_btn.png')
    restart_button = pygame.transform.scale(restart_button1,(225,150))


    #grid for the screen 
    #def draw_grid():
        #for line in range(0, 20):
            #pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
            #pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


    #button for resetting 
    class Button():
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.clicked = False
        
        def draw(self):
            action = False

            #get mouse position
            pos = pygame.mouse.get_pos()

            #check mouseover and clicked conditions
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    action = True
                    self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False


            #draw button
            screen.blit(self.image, self.rect)

            return action
            
                                    
                
                
            


            
            screen.blit(self.image,self.rect)



    #loading the character image and displaying and movement
    class Player():
        def __init__(self,x,y) :#(constructer loads only once when called  )
            self.reset(x,y)


        
        def update(self,game_over):#runs througout the game loop 
            global win
            global run
            #coordinate of the player initially
            dx = 0
            dy = 0  

            #to slow down the speed of animation
            walk_cooldown = 5

            if game_over == 0:

                #to recieve key presses for the movement of the player
                key = pygame.key.get_pressed()

                #jump y corrdinate is increasing from top to bottom so -ve
                if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                    self.vel_y=-15
                    self.jumped = True
                if key[pygame.K_SPACE] == False:
                    self.jumped = False
                


 
                #left movement 
                if key[pygame.K_LEFT]:
                    dx -=5
                    #to change animation when the key is presssed
                    self.counter+=1
                    self.direction= -1
                if key[pygame.K_RIGHT]:
                    dx +=5
                    self.counter+=1
                    self.direction = 1
                #to load the noraml animation when no key is pressed 
                if key[pygame.K_LEFT]==False and key[pygame.K_RIGHT]== False:
                    self.counter = 0
                    self.index = 0 
                    if self.direction == 1:
                        self.image = self.image_right[self.index]
                    if self.direction == -1:
                        self.image = self.image_left[self.index]


                



                #handle animation
                
                if self.counter > walk_cooldown:
                    self.counter=0
                    self.index+=1
                    #not to allow to exceed the list of images 
                    if self.index >= len(self.image_right):
                        self.index = 0
                    #to get the direction the char is facing 
                    if self.direction == 1:
                        self.image = self.image_right[self.index]

                    if self.direction == -1:
                        self.image = self.image_left[self.index]



                #to add gravity 
                self.vel_y+=1
                if self.vel_y>10:#threshold for gravity 
                    self.vel_y = 10
                dy+=self.vel_y


                #check for collision
                #to check if he is on top a block 
                self.in_air = False#inital asumption then the next code block runs to prove he is not in air 
                for tile in world.tile_list:
                    #check for collision in x direction
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    #check for collision in y direction
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        #check if below the ground i.e. jumping
                        if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                            self.vel_y = 0
                        #check if above the ground i.e. falling
                        elif self.vel_y >= 0:
                            dy = tile[1].top - self.rect.bottom
                            self.vel_y = 0
                            self.in_air = False
                

                #check for collision wtih enemies
                if pygame.sprite.spritecollide(self, fire_group, False):
                    game_over = -1

                if pygame.sprite.spritecollide(self, Lava_group, False):
                    game_over = -1

                if pygame.sprite.spritecollide(self,exit_group,False):
                    game_over=2
                    
                    
                #update player cords 
                
                self.rect.x +=dx
                self.rect.y +=dy
                
                #to avoid the player from falling from the bottom of the screen 
                if self.rect.bottom>screen_height:
                    self.rect.bottom = screen_height
                    dy=0

            
            elif game_over== -1:
                self.image = self.dead_image
                if self.rect.y>200:

                    self.rect.y -= 5
            elif game_over== 2:
                if self.rect.y>200:

                    self.rect.y -= 5
                

            # to draw player on the screen 
            screen.blit(self.image,self.rect)
            #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

            return game_over
        def reset(self,x,y):#when rest button is pressed the player should come to initial position 
            #this acts as dual fucntion  first time and when reset is cicked 
            # to add walking animations
            #facing right 
            self.image_right = []#has all the images animated

            #facing  left
            self.image_left = []

            self.index = 0
            #speed of animation 
            self.counter = 0


            #loop to load the animation images
            for num in range(1,5): 
                img_right= pygame.image.load(f'./images/icarus{num}.png')
                #images scales to (width,height)
                img_right = pygame.transform.scale(img_right,(40,80))
                img_left = pygame.transform.flip(img_right , True , False)
                self.image_right.append(img_right)
                self.image_left.append(img_left)

            tempimg=pygame.image.load("./images/ghost.png")
            self.dead_image = pygame.transform.scale(tempimg,(50,100))

            self.image = self.image_right[self.index]
            #creates rectangle of the character
            self.rect = self.image.get_rect()
            #x and y coordinates of the char
            self.rect.x = x
            self.rect.y = y
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            #jump show reduce with gravity so thsi variable for tht velocity 
            self.vel_y = 0
            #TO JUMP ONCE IF SPACE BAR IS PRESSED ONCE 
            self.jumped = False
            #to control the direction the character is facing 
            self.direction = 0
            #to avoid spam of space bar we need to check if the player is on a block
            self.in_air=True

        

    #define the world 
    class World():
        def __init__(self, data):
            self.tile_list = []

            #load images
            brick_img = pygame.image.load('./images/brick.png')
            floor_img = pygame.image.load('./images/floor.png')
            chest_img= pygame.image.load('./images/chest.png')

            row_count = 0
            for row in data:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        img = pygame.transform.scale(brick_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 2:
                        img = pygame.transform.scale(floor_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        #positon of the grass block
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 3:
                        fire=Enemy(col_count * tile_size,row_count*tile_size+15)
                        fire_group.add(fire)
                    #lava
                    if tile == 6:
                        lava = Lava(col_count * tile_size,row_count*tile_size + int((tile_size // 2)))
                        Lava_group.add(lava)
                    if tile == 9:
                        chest = Exit(col_count * tile_size,row_count*tile_size )
                        exit_group.add(chest)
                        

                    col_count += 1
                row_count += 1

        def draw(self):
            for tile in self.tile_list:
                screen.blit(tile[0], tile[1])


    #enemy creation 
    class Enemy(pygame.sprite.Sprite):
        
        def __init__(self, x, y) :
            pygame.sprite.Sprite.__init__(self)
            #load images
            self.image1 = pygame.image.load('./images/fire1.png')
            self.image = pygame.transform.scale(self.image1,(45,36))

            self.rect =self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.move_direction = 1
            self.move_counter = 0

        

        def update(self):
                self.rect.x += self.move_direction
                self.move_counter += 1
                if abs(self.move_counter) > 50:
                    self.move_direction *= -1
                    self.move_counter *= -1
            
    #lava    
    class Lava(pygame.sprite.Sprite):
        def __init__(self, x, y) :
            pygame.sprite.Sprite.__init__(self)
            #load images
            img= pygame.image.load('./images/lava.png')
            self.image = pygame.transform.scale(img,(tile_size,tile_size // 2))
            
            self.rect =self.image.get_rect() 
            self.rect.x = x
            self.rect.y = y
            
    class Exit(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            img=pygame.image.load('./images/chest.png')
            self.image = pygame.transform.scale(img,(tile_size,tile_size))
            
            self.rect =self.image.get_rect() 
            self.rect.x = x
            self.rect.y = y
            
            
        
        


        
        

    world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1], 
    [1, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 7, 1, 5, 0, 0, 0, 1], 
    [1, 2, 2, 0, 0, 0, 0, 1, 6, 6, 6, 6, 6, 1, 0, 0, 0, 0, 0, 1], 
    [1, 7, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1], 
    [1, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
    [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 0, 0, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
    [1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]


    #to call the player and y coordinate is screen height - (tile size+height of char)
    player =  Player(100,screen_height - 130 )

    fire_group = pygame.sprite.Group()

    Lava_group = pygame.sprite.Group()
    
    exit_group = pygame.sprite.Group()


    world = World(world_data)

    #create buttons 

    restart_button = Button(screen_width // 2 -100 ,screen_height // 2 -50 , restart_button)

    #to run the game continiously

    run=True
    cover=True
    title_image=pygame.image.load("images/labyrinth_.png")
    while cover:
        screen.blit(title_image,(0,0))
        events =pygame.event.get()
        for even in events:
            if even.type == QUIT:
                    cover=False
                    win=False
                    run=False
            if even.type == KEYDOWN:
                if even.key == K_RETURN:
                    cover=False   
        pygame.display.flip()
    while run:

        clock.tick(fps)
        
        #to display the loaded images on the screen(order matters)

        screen.blit(bg_img, (0, 0))
        # screen.blit(sun_img, (100, 100))

        world.draw()
        if game_over == 15:
            run=False
        if game_over == 0:

            fire_group.update()
        fire_group.draw(screen)

        Lava_group.draw(screen)

        exit_group.draw(screen)
        

        #draw_grid()

        game_over = player.update(game_over)
        
        #if player has died the button has to be displayed 
        if game_over == -1:
            if restart_button.draw():
            
                player =  Player(100,screen_height - 130)
                game_over=0
        if game_over == 2:
            if restart_button.draw():
            
                player =  Player(100,screen_height - 130)
                game_over=0
        #way to close the game (event handler)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

        # world.draw()

        #update the screen 
        pygame.display.update()
#runner()
