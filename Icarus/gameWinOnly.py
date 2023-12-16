from pygame import display,image,transform,Rect,mixer,QUIT,KEYDOWN,time,event,K_a,K_RIGHT,K_LEFT,K_d,K_RETURN,key
from pygame import quit as q
import random
def runner(x):
    global replay#flag to check if player wants to keep playing
    difficulty=x  #difficulty is inversely proportional to this value
    mixer.init()
    replay=True
    cover=True
    sW=500
    sH=900
    screen=display.set_mode((sW,sH))
    title="Icarus and the Sword"
    win_image=image.load("assets/win.png")
    winimage=transform.scale(win_image,(450,300))
    lose_image=image.load("assets/lost.png")
    loseimage=transform.scale(lose_image,(450,300))
    dragon1=Rect(12,25,100,100)
    dragon2=Rect(125+12,25,100,100)
    dragon3=Rect(250+12,25,100,100)
    dragon4=Rect(375+12,25,100,100)
    dragon_closed_image=image.load("assets/dragonclosed.png")
    dragonclosed=transform.scale(dragon_closed_image,(99,99))
    dragon_open_image=image.load("assets/dragonopen.png")
    dragonopen=transform.scale(dragon_open_image,(99,99))
    dragonlist={0:[dragon1,dragonclosed],1:[dragon2,dragonclosed],2:[dragon3,dragonclosed],3:[dragon4,dragonclosed]}
    sword=Rect(0,250,500,10)
    sword_image=image.load("assets/sword.png")
    swordimage=transform.scale(sword_image,(500,10))
    ball_image=image.load("assets/fire1.png")
    ball_image1=image.load("assets/fire2.png")
    ball_image2=image.load("assets/fire3.png")
    ball_image3=image.load("assets/fire4.png")
    ballgroup=[ball_image,ball_image1,ball_image2,ball_image3]
    ball1=transform.scale(ball_image1,(89,89))
    ball2=transform.scale(ball_image2,(89,89))
    fireball_sound=mixer.Sound("assets/fireball.mp3")
    mixer.Sound.set_volume(fireball_sound,0.05)  
    death_sound=mixer.Sound("assets/explode.mp3")
    mixer.Sound.set_volume(death_sound,0.15) 
    wind=mixer.Sound("assets/wind.mp3")
    mixer.Sound.set_volume(wind,0.1)
    swordsound=mixer.Sound("assets/sword.mp3")
    mixer.Sound.set_volume(swordsound,0.1)
    warrior_image=image.load("assets/icarus.png")
    warrior=transform.scale(warrior_image,(80,80))
    warrior2_image=image.load("assets/icarus2.png")
    warrior2=transform.scale(warrior2_image,(80,80))
    title_image=image.load("images/flight.png")
    display.set_caption(title)
    startx=225
    starty=800
    background_Image=image.load("assets/clouds.png")
    backgroundImage=transform.scale(background_Image,(500,600))
    fps=60#framerate
    frequency=time.Clock()
    vict=False
    while replay:
        fireballs=[]
        loadball=0
        def fireball(x):
            global r
            if(ballcount%20==0):
                r=random.randint(0,3)
            for i in fireballs:
                screen.blit(x[r],(i.x,i.y))
        ballcount=0
        play=True 
        warriorRect=Rect(startx,starty,80,40)
        clouds=0
        count=0
        play=True
        lose=False
        win=False
        while cover:
            screen.blit(title_image,(0,0))
            events =event.get()
            for even in events:
                if even.type == QUIT:
                        cover=False
                        win=False
                        lose=False
                        play=False
                        replay=False
                if even.type == KEYDOWN:
                    if even.key == K_RETURN:
                        cover=False   
            display.flip()
        while play:
            frequency.tick(fps)
            for even in event.get():
                if even.type == QUIT:
                    play=False 
                    replay=False
            if count%5==0 and warriorRect.y>50:
                warriorRect.y-=1
            if count%3540==0:
                wind.play()
            if count%3535==0 and count!=0:
                wind.stop()
            count+=1
            if loadball%difficulty==0:
                fireball_sound.play()
                i,j=random.sample(range(0,4),2)
                for k in range(4):
                    dragonlist[k][1]=dragonclosed
                dragonlist[i][1]=dragonopen
                dragonlist[j][1]=dragonopen
                ball1=Rect(dragonlist[i][0].x+8,dragonlist[i][0].y+55,83,80)
                ball2=Rect(dragonlist[j][0].x+8,dragonlist[i][0].y+55,83,80)
                fireballs.append(ball1)
                fireballs.append(ball2)
            loadball+=1
            for i in fireballs:
                i.y+=3
            pressedKeys=key.get_pressed()
            if (pressedKeys[K_a] or pressedKeys[K_LEFT]) and (warriorRect.x)>3:
                warriorRect.x-=9
            if (pressedKeys[K_d] or pressedKeys[K_RIGHT]) and (warriorRect.x)<414:
                warriorRect.x+=9
            for i in range(0,3):
                screen.blit(backgroundImage,(0,clouds-i*600+300))
            clouds+=10
            if clouds>600:
                clouds=0
            screen.blit(swordimage,(sword.x,sword.y))
            fireball(ballgroup)
            ballcount+=1
            for i in range(4):
                screen.blit(dragonlist[i][1],(dragonlist[i][0].x,dragonlist[i][0].y))
            if(warriorRect.y<325):
                screen.blit(warrior2,(warriorRect.x+3,warriorRect.y))
            else:
                screen.blit(warrior,(warriorRect.x+3,warriorRect.y))
            if warriorRect.colliderect(sword):
                swordsound.play()
                vict=True
                win=True
                play=False
            for i in fireballs:
                if warriorRect.colliderect(i):
                    death_sound.play()
                    play=False
                    lose=True
            display.flip()
        wind.stop()
        while win:
            replay=False
            for even in event.get():
                if even.type == QUIT:
                    win=False 
                    replay=False
                if even.type == KEYDOWN:
                    if even.key == K_RETURN:
                        win=False
            screen.blit(winimage,(25,300))    
            display.flip()
        while lose:
            for even in event.get():
                if even.type == QUIT:
                    lose=False
                    replay=False 
                if even.type == KEYDOWN:
                    if even.key == K_RETURN:
                        lose=False
            screen.blit(loseimage,(25,300))    
            display.flip()
    return vict