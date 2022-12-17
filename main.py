import pygame
import random
import os 
from pygame import mixer
import sys 

pygame.display.init()
pygame.font.init()

HIGHESTSCORE = 0

#window dimensions
WIDTH, HEIGHT = 1100, 800
WHITE = (255,255,255)
FPS = 60

#Duck dimensions
DUCK_WIDTH, DUCK_HEIGHT = 100, 170  
DUCK_RECT_WIDTH, DUCK_RECT_HEIGHT = 45, 60   #size of duck beak //collision zone 
STARTING_Y_HEIGHT = HEIGHT - DUCK_HEIGHT - 40
DUCK_X_VELOCITY = 10

GRAPE_LIST = []
LEMONADE_LIST = []
FRUIT_VELOCITY = 1 
SPAWN_TIME_DECREASE_INTERVAL = 10000 #decreases the max spawn time every 10 seconds


GRAPE_RANDOM_SPAWN_TIME_HIGH = 500   #spawns grape/lemonade times range #see line 67 and 87
GRAPE_RANDOM_SPAWN_TIME_LOW = 400   


SCORE = 0   #For some reason it counts by 2
REAL_SCORE = 0 #so this halves the score
#HIGH_SCORE = 0 
my_font = pygame.font.SysFont('Comic Sans MS', 30)


#import assets
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "background.png")),(WIDTH,HEIGHT))  
DUCK = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "duck.png")), (DUCK_WIDTH,DUCK_HEIGHT))


#create display and name
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("The Duck Song Game")
duck = pygame.Rect(WIDTH/2, STARTING_Y_HEIGHT, DUCK_RECT_WIDTH, DUCK_RECT_HEIGHT)  #draw duck mouth
pygame.mixer.init()
mixer.music.load(os.path.join("Assets", "backgroundmusic.wav"))
mixer.music.play(-1)
grapepopSound = pygame.mixer.Sound(os.path.join("Assets", "pop.wav"))
lemonadeloseSound = pygame.mixer.Sound(os.path.join("Assets", "lemonade.wav"))
def main():  #main loop to keep window open until exit is pressed
    
    global HIGHESTSCORE

    try:
        HIGHESTSCORE = int(gethighscore())
    except:
        HIGHESTSCORE = 0
            
    startscreen()    
def game():    

    
    global GRAPE_RANDOM_SPAWN_TIME_HIGH, GRAPE_RANDOM_SPAWN_TIME_LOW, FRUIT_VELOCITY

    clock = pygame.time.Clock()

    def draw_window(duck):                      
        WIN.blit(BACKGROUND, (0,0)) #draw background
        WIN.blit(DUCK, (duck.x-30, duck.y)) #draw duck using "duck rectangle" position
        drawing_items()
        draw_score()
        pygame.display.update()

    run = True
    pygame.time.set_timer(pygame.USEREVENT+1, random.randint(GRAPE_RANDOM_SPAWN_TIME_LOW,GRAPE_RANDOM_SPAWN_TIME_HIGH))   #every so and so seconds randomly generate grape
    #pygame.time.set_timer(pygame.USEREVENT+2, SPAWN_TIME_DECREASE_INTERVAL)      #see line 87   #spawn time interval. every SPAWNTIMEDECREASEINTERVAL seconds call userevent 2, which decreases rand values          
    pygame.time.set_timer(pygame.USEREVENT+3, SPAWN_TIME_DECREASE_INTERVAL) #increase drop speed
    while run:
        clock.tick(FPS)   #run loop FPS (60) times per second 

        for current_grape in GRAPE_LIST:            #speed of grape downwards
            current_grape.y += FRUIT_VELOCITY  
        for current_lemonade in LEMONADE_LIST:
            current_lemonade.y += FRUIT_VELOCITY
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                run = False   
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT+1:
                grape_or_lemon = random.randint(1,5) #grape or lemonade
                if grape_or_lemon == 5:  #    1/5 create grape
                    x_coordinate_of_grape_or_lemon = random.randint(60, WIDTH - 60)            #create random x variable for grape or lemonade
                    GRAPE_LIST.append(grape(x_coordinate_of_grape_or_lemon,-100))                 #spawn grape by adding to grape_list to draw
                if grape_or_lemon < 5:  #     4/5 create lemonade
                    x_coordinate_of_grape_or_lemon = random.randint(100,WIDTH - 100)
                    LEMONADE_LIST.append(lemonade(x_coordinate_of_grape_or_lemon, -100))
    #        if event.type == pygame.USEREVENT + 2:                  #decreases max spawn time of grape/lemonade
   #             if GRAPE_RANDOM_SPAWN_TIME_LOW > 250:
    #                GRAPE_RANDOM_SPAWN_TIME_LOW -= 50
   #                 print('1')
   #             if GRAPE_RANDOM_SPAWN_TIME_HIGH > 500:
   #                 GRAPE_RANDOM_SPAWN_TIME_HIGH -= 100
   #                 print("12")
            if event.type == pygame.USEREVENT + 3:
                if FRUIT_VELOCITY < 4:
                    FRUIT_VELOCITY += 0.1
                    
        keys_pressed = pygame.key.get_pressed()            #finds what keys are being pressed
        duck_move(keys_pressed, duck)                      #moves duck left and right
        loop_boundary(duck)                                #loops duck around if edge is touched
        draw_window(duck)             #line 45.  #call function draw window and update display to show window
    
    pygame.quit()




def duck_move(keys_pressed, duck):

    if keys_pressed[pygame.K_RIGHT]:   #move right
        duck.x += DUCK_X_VELOCITY      
    if keys_pressed[pygame.K_LEFT]:   #move left
        duck.x -= DUCK_X_VELOCITY    

def loop_boundary(duck):                 
    if duck.x + 15> WIDTH:     #if duck moves past screen on the right
        duck.x = 15    
    if duck.x < 0:     #if duck moves past screen on the left
        duck.x = WIDTH - 35

class grape (object):           #grape object
    img = pygame.image.load(os.path.join("Assets", "Grape.png"))
    def __init__(self, x, y):
        self.x = x
        self.y = y
        GRAPE_LIST.append(self)
    def draw(self, WIN):            #draw grape to screen
        WIN.blit(self.img, (self.x, self.y))
        
class lemonade (object):            #lemonade object
    img = pygame.image.load(os.path.join("Assets", "Lemonade.png"))
    def __init__(self, x, y):
        self.x = x
        self.y = y
        LEMONADE_LIST.append(self)
    def draw(self, WIN):                #draw lemonade to screen
        WIN.blit(self.img, (self.x, self.y))

def drawing_items():
    for grape_item in GRAPE_LIST:        #draws grapes
            grape_item.draw(WIN)
            grape_rect = pygame.Rect(grape_item.x, grape_item.y, 49, 75)        #grape hitbox
            if duck.colliderect(grape_rect):                             #upon collision of grape 
                GRAPE_LIST.pop(GRAPE_LIST.index(grape_item))
                print(GRAPE_LIST)
                global SCORE
                SCORE += 1
                grapepopSound.play()
                global REAL_SCORE
                REAL_SCORE = int(SCORE/2)
            if grape_item.y > HEIGHT:
                GRAPE_LIST.pop(GRAPE_LIST.index(grape_item))          #remove item from screen if below screen
                #gameOverScreen2()
    for lemonade_item in LEMONADE_LIST:        #draws lemonade
            lemonade_item.draw(WIN)      
            lemonade_rect = pygame.Rect(lemonade_item.x, lemonade_item.y, 50, 60)          #lemonade hitbox 
            if duck.colliderect(lemonade_rect):                             #upon collision of lemonade 
                LEMONADE_LIST.pop(LEMONADE_LIST.index(lemonade_item))
                lemonadeloseSound.play()
                gameOverScreen1()            #line 155
            if lemonade_item.y > HEIGHT:
                LEMONADE_LIST.pop(LEMONADE_LIST.index(lemonade_item))

def draw_score():
    text_surface = my_font.render('Score = {}'.format(REAL_SCORE), False, (0, 0, 0))
    WIN.blit(text_surface, (10, 5))


def startscreen():

    ARROWS = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Arrow.png")),(250,90))

    run = True
    while run == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                init()
                game()
        WIN.blit(BACKGROUND,(0,0))        
        #click to play text
        Playtext = pygame.font.SysFont('Comic Sans MS', 60)
        play_text = Playtext.render("Press any key to start!", False, (0,0,0))
        WIN.blit(play_text, (230, HEIGHT/2 - 200))
        #high score text
        Highscore_font = pygame.font.SysFont('Comic Sans MS', 45)
        End_score = Highscore_font.render("High Score = {}".format(HIGHESTSCORE), False, (0,0,0))
        WIN.blit(End_score, (WIDTH - 730, HEIGHT - 500))   
        #controls text
        Arrowtext = pygame.font.SysFont('Comic Sans MS', 40)
        Arrow_keys_text = Arrowtext.render("Use Arrow Keys to Move", False, (0,0,0))
        WIN.blit(Arrow_keys_text, (WIDTH - 800, HEIGHT - 400))  
        #infotext
        info_font = pygame.font.SysFont('Comic Sans MS', 30)
        Infotext = info_font.render("Eat the Grapes, dodge the lemonade.", False, (0,0,0))
        WIN.blit(Infotext, (WIDTH - 830, HEIGHT - 200))   
        #arrowimage
        WIN.blit(ARROWS, (WIDTH - 730, HEIGHT - 300))

        pygame.display.update()


def gameOverScreen1():           #game over window drank lemonade
 
    global HIGHESTSCORE

    run = True
    while run == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                init()
                game()
        WIN.blit(BACKGROUND,(0,0))   


        if(HIGHESTSCORE < REAL_SCORE):
            HIGHESTSCORE= REAL_SCORE
        with open("highscore.txt", "w") as f:
            f.write(str(HIGHESTSCORE))


        #game over text
        Gameover_font = pygame.font.SysFont('Comic Sans MS', 100)
        End_score = Gameover_font.render("Game Over!".format(REAL_SCORE), False, (0,0,0))
        WIN.blit(End_score, (WIDTH/2 - 290, HEIGHT/2 - 250))
        #dranklemonadetext
        drank = pygame.font.SysFont('Comic Sans MS', 40)
        drank_lemon = drank.render("You drank the lemonade...".format(REAL_SCORE), False, (0,0,0))
        WIN.blit(drank_lemon, (WIDTH/2 - 240, HEIGHT - 520))
        #score text
        Large_font = pygame.font.SysFont('Comic Sans MS', 75)
        End_score = Large_font.render("Score = {}".format(REAL_SCORE), False, (0,0,0))
        WIN.blit(End_score, (WIDTH/2 - 200, HEIGHT/2 - 80))
        #High Score Text
        Highscore_font = pygame.font.SysFont('Comic Sans MS', 45)
        End_score = Highscore_font.render("High Score = {}".format(HIGHESTSCORE), False, (0,0,0))
        WIN.blit(End_score, (WIDTH - 730, HEIGHT - 370))
        #play new game text
        newgamefont = pygame.font.SysFont('Comic Sans MS', 45)
        End_score = newgamefont.render("Press any key to play again!", False, (0,0,0))
        WIN.blit(End_score, (WIDTH/2 - 300, HEIGHT - 220))
        
        pygame.display.update()

def gameOverScreen2():           #game over window lost grape
 
    global HIGHESTSCORE

    run = True
    while run == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                init()
                game()
        WIN.blit(BACKGROUND,(0,0))   


        if(HIGHESTSCORE < REAL_SCORE):
            HIGHESTSCORE= REAL_SCORE
        with open("highscore.txt", "w") as f:
            f.write(str(HIGHESTSCORE))


        #game over text
        Gameover_font = pygame.font.SysFont('Comic Sans MS', 100)
        End_score = Gameover_font.render("Game Over!".format(REAL_SCORE), False, (0,0,0))
        WIN.blit(End_score, (WIDTH/2 - 290, HEIGHT/2 - 250))
        #dranklemonadetext
        drank = pygame.font.SysFont('Comic Sans MS', 40)
        drank_lemon = drank.render("Oh no! You lost a grape!".format(REAL_SCORE), False, (0,0,0))
        WIN.blit(drank_lemon, (WIDTH/2 - 230, HEIGHT - 520))
        #score text
        Large_font = pygame.font.SysFont('Comic Sans MS', 75)
        End_score = Large_font.render("Score = {}".format(REAL_SCORE), False, (0,0,0))
        WIN.blit(End_score, (WIDTH/2 - 200, HEIGHT/2 - 80))
        #High Score Text
        Highscore_font = pygame.font.SysFont('Comic Sans MS', 45)
        End_score = Highscore_font.render("High Score = {}".format(HIGHESTSCORE), False, (0,0,0))
        WIN.blit(End_score, (WIDTH - 730, HEIGHT - 370))
        #play new game text
        newgamefont = pygame.font.SysFont('Comic Sans MS', 45)
        End_score = newgamefont.render("Press any key to play again!", False, (0,0,0))
        WIN.blit(End_score, (WIDTH/2 - 300, HEIGHT - 220))
        
        pygame.display.update()

def init():         #reset variables
    
    global GRAPE_LIST,LEMONADE_LIST,SCORE,REAL_SCORE, GRAPE_RANDOM_SPAWN_TIME_HIGH, GRAPE_RANDOM_SPAWN_TIME_LOW, duck, FRUIT_VELOCITY

    GRAPE_LIST = []
    LEMONADE_LIST = []
    SCORE = 0
    REAL_SCORE = 0
    GRAPE_RANDOM_SPAWN_TIME_HIGH = 500
    GRAPE_RANDOM_SPAWN_TIME_LOW = 400
    duck = pygame.Rect(WIDTH/2, STARTING_Y_HEIGHT, DUCK_RECT_WIDTH, DUCK_RECT_HEIGHT)
    FRUIT_VELOCITY = 1
 

def gethighscore():
    with open ("highscore.txt", "r" ) as f:
        return f.read()






if __name__ == "__main__":
    main()


 #color = (255,0,0)                                                                                  #####CREATES HITBOX 
            #pygame.draw.rect(WIN, color, duck)
            #pygame.display.flip()