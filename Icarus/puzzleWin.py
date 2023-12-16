import pygame
from sys import exit
from time import time
from random import randint

def runner():
    def GeneratePrompt():
        with open("chest_assets/prompts.txt", 'r') as file:
            prompts=file.readlines()
            for i in prompts:
                if len(i)>=10 and len(i)<25:
                    try:
                        index = randint(0,(len(prompts))+1)
                        finalprompt=prompts[index]
                    except IndexError or UnboundLocalError:
                        GeneratePrompt()
        return finalprompt



    def timeElapsed(stime, etime):
        tim = stime-etime

        return tim   

    def Processing(user_text):
        stime=time()
        global tim
        iprompt = user_text
        tim = round(timeElapsed(stime, etime), 2)
        speed = typingSpeed(iprompt, stime, etime)
        errors = typingErrors(displayprompt)
        accuracy = ((len(iwords)-errors)/len(iwords))*100
        wpm = round(speed,2)*60   
        if wpm>=35 and accuracy == 100:
            return True
        else:
            return False

    def typingSpeed(iprompt, stime, etime):
        global iwords

        iwords = iprompt.split()
        twords = len(iwords)
        speed = twords / tim

        return speed


    def typingErrors(prompt):
        global iwords

        words = prompt.split()
        errors = 0

        for i in range(len(iwords)):
            if i in (0, len(iwords)-1):
                if iwords[i] == words[i]:
                    continue
                else:
                    errors +=1
            else:
                if iwords[i] == words[i]:
                    if (iwords[i+1] == words[i+1]) & (iwords[i-1] == words[i-1]):
                        continue
                    else:
                        errors += 1
                else:
                    errors += 1
        return errors
    


    pygame.init()
    Win = pygame.display.set_mode((1000,900))
    clock = pygame.time.Clock()
    chest_left_tilt = pygame.image.load("chest_assets/chest_left_tilt.png")
    chest_right_tilt = pygame.image.load("chest_assets/right tilt.png")
    chest_no_tilt = pygame.image.load("chest_assets/no_tilt.png")
    display_textbox = pygame.image.load("chest_assets/final textbox.png")
    winimage=pygame.image.load("chest_assets/chest_open.png")
    loseimage=pygame.image.load("chest_assets/no_tilt.png")
    title_image=pygame.image.load("images/scripture.png")
    display_textbox.set_alpha(100)
    txtf = pygame.font.Font("chest_assets/game font.ttf",40)
    replay=True
    cover=True
    vict=False
    while replay:
        win=False
        lose=False
        typing=False
        snip = txtf.render('',True,(0,0,0))
        EnterPrompt = txtf.render("Enter this code to open the chest: ",True,(0,0,0))
        EnterPrompt.set_alpha(200)
        EnterLine = "Press Enter to start"
        counter = 0
        speed = 3
        TextRendered = False
        imgtick = 1
        displayprompt = GeneratePrompt()
        text = txtf.render(displayprompt,True,(0,0,0))
        user_text = ''  
        GameStatus = True
        DisplayCondition = False
        while cover:
            Win.blit(title_image,(0,0))
            events =pygame.event.get()
            for even in events:
                if even.type == pygame.QUIT:
                        cover=False
                        win=False
                        GameStatus=False
                        replay=False
                if even.type == pygame.KEYDOWN:
                    if even.key == pygame.K_RETURN:
                        cover=False   
            pygame.display.flip()
        while GameStatus == True:           
            if imgtick%100 == 0:
                Win.blit(chest_left_tilt,(0,0))
                imgtick+=1
            elif imgtick%100 != 0:
                Win.blit(chest_right_tilt,(0,0))
                imgtick+=1
                
            Win.blit(display_textbox,(100,50))    
            Win.blit(EnterPrompt,(150,100))
            
            if counter < speed * len(displayprompt):
                counter+=1
            elif counter >= speed * len(displayprompt):
                done = True
            snip = txtf.render(displayprompt[0:counter//speed],True,(0,0,0))
            EnterLineRender = txtf.render(EnterLine[0:counter//speed],True,(0,0,0))
            EnterLineRender.set_alpha(200)
            Win.blit(snip,(150,150))
            Win.blit(EnterLineRender,(150,200))
                            
            user_text_surface = txtf.render(user_text,True,(0,0,0))        
            Win.blit(user_text_surface, (150,250)) 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE and typing:
                        user_text = user_text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    elif event.key == pygame.K_RETURN and (not typing):
                        etime = time()
                        typing=True
                    elif typing:
                        user_text += event.unicode 
                    else:
                        pass
            if len(user_text.strip()) == len(displayprompt.strip()):
                DisplayCondition =Processing(user_text)
                result_1 = "You have unlocked the chest ! "
                result_win = txtf.render(result_1, True, (0, 0, 0))

                result_2 = "You have failed to unlock the chest ! "
                result_lose = txtf.render(result_2, True, (0, 0, 0))
                GameStatus=False
                
                '''if DisplayCondition == True:
                        Win.blit(result_win, (150,350))
                else:
                        Win.blit(result_lose, (150,350))'''
                if DisplayCondition == True:
                        win=True
                else:
                        lose=True                               
            pygame.display.update()
            clock.tick(60)
        while win:
            replay=False
            vict=True
            for even in pygame.event.get():
                if even.type == pygame.QUIT:
                    win=False 
                    replay=False
                if even.type == pygame.KEYDOWN:
                    if even.key == pygame.K_RETURN:
                        win=False
            Win.blit(winimage,(0,0))    
            pygame.display.flip()
        while lose:
            for even in pygame.event.get():
                if even.type == pygame.QUIT:
                    lose=False
                    replay=False 
                if even.type == pygame.KEYDOWN:
                    if even.key == pygame.K_RETURN:
                        lose=False
            Win.blit(loseimage,(0,0))    
            pygame.display.flip()
    return vict
#runner()           
