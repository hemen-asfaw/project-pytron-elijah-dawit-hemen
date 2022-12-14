# references 
# The game has been made a number of times, so we were able to find different guides on how to structure it.
# We worked with the TA's (Aidan D. and Julian) for debugging and on how to understand the previously made codes to generate 
# Our own on lines of code.  
# The videos below are the ones we referenced to most 
# Video1: https://youtu.be/hUC4cseJdBQ
# Video2: https://youtu.be/K6mJqSnwj1g
# Video3: https://youtu.be/wnBGG7JLrkg 
# link1: https://stackoverflow.com/questions/19882415/closing-pygame-window
# link2: https://www.pygame.org/docs/ we referenced pygame docs to better how pygame worked and some specific functions 
# We worked in pairs for a majority of the project. The pairs were Ruth and Hemen, Dawit and Elijah
# Hemen and Ruth worked on building the classes, for Iggy and the Obstacles, adding sounds and details on the menu screen.    
# Elijah and Dawit worked on the main function and the menu screen. 
# We all ended up taking shifts debugging and editing each other’s codes with the help of the TA's. 
 
 
import pygame
import os
import random
import sys
#import time
pygame.init()
pygame.mixer.init()#sounds

screen_x = 1280
screen_y = 720
screen = pygame.display.set_mode((screen_x, screen_y))
game_name_display = pygame.display.set_caption("Iggy Runs!!")
clock = pygame.time.Clock()
speed_game = 10
background_start = 0

#we downloaded and croped our pictures as needed 
#referenced video1 and video3
RUNNING =[] # List of running images
run1_image = pygame.image.load("assets/images/Running_1.PNG")
scale_run1_image = pygame.transform.scale(run1_image,(250, 140))
RUNNING.append(scale_run1_image) 
run2_image = pygame.image.load("assets/images/running_2.PNG")
scale_run2_image = pygame.transform.scale(run2_image,(250, 140))
RUNNING.append(scale_run2_image)

OBSTACLES = [] #List of obstacle images
kiwi_image = pygame.image.load("assets/images/kiki_bots.PNG") 
kiwi_rescaled = pygame.transform.scale(kiwi_image,(100, 100))
OBSTACLES.append(kiwi_rescaled)
book1_image = pygame.image.load("assets/images/obstacle_1.PNG") 
book1_rescaled = pygame.transform.scale(book1_image,(100, 100))
OBSTACLES.append(book1_rescaled)
book2_image = pygame.image.load("assets/images/obstacle_2.PNG") 
book2_rescaled = pygame.transform.scale(book2_image,(100, 100))
OBSTACLES.append(book2_rescaled)

#background image 
BACKGROUND = pygame.image.load(os.path.join("assets/images/background.JPG"))

#font to display texts 
game_font = pygame.font.Font("assets/font/Creampeach.ttf", 30)
game_font2 = pygame.font.Font("assets/font/new_font.ttf", 60)

#referenced video2 on how to add sounds
#sounds
game_over_snd = pygame.mixer.Sound("assets/sounds/game.over.wav")
theme_song_snd = pygame.mixer.Sound("assets/sounds/theme.song.wav")




#referenced video1             
class Iggy(): # Our Iggy class contains the methods init, update, run, display and jump.  
    GRAVITY = 10
    
    def __init__(self): #this method initializes our basic funtions that we'll be using
        self.iggy_jump = False 
        self.run_img = RUNNING
        self.y = 250
        self.x = 510
        self.gravity = self.GRAVITY 
        self.current_image = 0 
        self.image = self.run_img[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
    def update(self, inputs): #The different actions of iggy that will change as game goes on 
        if inputs[pygame.K_SPACE] or inputs[pygame.K_UP]:
            self.iggy_jump = True

        if self.iggy_jump:
            self.jump()
        else:
            self.y = 510
            self.x = 250
            self.run()

        self.rect.x = self.x
        self.rect.y = self.y

    def run(self): #function that we controls iggys running function
        self.current_image += 0.08 
        if self.current_image >= 2:
            self.current_image = 0 
        self.image = self.run_img[int(self.current_image)]
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def display(self): #controls what's being displayed on the screen 
        screen.blit(self.image, self.rect)


    def jump(self): #controls iggys jumps 
        if self.iggy_jump:
            self.y -= self.gravity * 4
            self.gravity -= 0.5 # change speed of the jump
        if self.gravity < -(self.GRAVITY):
            self.iggy_jump = False
            self.gravity = self.GRAVITY

class Obstacles(): # This class is for our obstacles (books & kiwi) and has the methods update and 

    def __init__(self, type): #initializes all the functions we'll be using 
        #the type parameter is for the type of obstacle which is either kiwi or the book 
        self.y = 250
        self.x = 510
        self.image = OBSTACLES[type] 
        self.type = type 
        self.rect = self.image.get_rect(center=(self.x, self.y))   
        self.rect.x = screen_x

    def update(self): #updates the obstacles as the game goes 
        self.rect.x -= speed_game 

    def display(self, screen): #controls what's being displayed on the screen 
        screen.blit(self.image, self.rect)

class kiwibot(Obstacles): # Sub class for obstacles 
    def __init__(self):
        super().__init__(0)
        self.rect.y = 550


class Book(Obstacles): # Sub class for obstacles 
    def __init__(self): 
        super().__init__(random.randint(1,2)) 
        self.rect.y = 400


def main_function(): # contains the global variables/obstacle list/death counter 
    global speed_game, background_start, points 
    player = Iggy()
    points = 0
    active_obstacles = [] # List of obstacles on the screen at any given moment 
    demise_counter  = 0


    def score(): # Score for our game that appears on the right corner
        global points, speed_game
        points +=1
        if points % 300 == 0 :
            speed_game += 1  
        text = game_font.render("Points: "+ str(points), True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        screen.blit(text, textRect)
        
    #referenced video2
    while True: #contains all the things that should be runnning contantly throughout the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #link1
                print("quitting")
                pygame.quit()
                sys.exit() 
        
        player_input = pygame.key.get_pressed() #keys player presses 

        screen.fill("light blue") #screen color for menu screen 

        # background design and display  
        background_rescaled = pygame.transform.scale(BACKGROUND, (1280,720))  
        speed_game += 0.0025
        background_start -= speed_game
        background_start -=1
        screen.blit(background_rescaled, (background_start, 0))
        screen.blit(background_rescaled, (background_start + 1280, 0))
        
        if background_start <= -1280: #keeps the ground running on an infinate loop
            background_start = 0

        player.display()
        player.update(player_input)

        if len(active_obstacles) == 0: #having obstacles appear 
            spawn_rate = random.randint(0,2)
            if spawn_rate == 0:
                active_obstacles.append(kiwibot())
            elif spawn_rate == 1:
                active_obstacles.append(Book())


        for obstacle in active_obstacles:
            obstacle.display(screen)
            obstacle.update()
            if player.rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                speed_game = 9
                demise_counter += 1
                menu(demise_counter)

                #pygame.draw.rect(screen , (255, 0, 0), player.rect, 2)
            theme_song_snd.play()
            if obstacle.rect.x < - obstacle.rect.width:
                active_obstacles.pop()
                
     

        score()

        pygame.display.update()

#referenced Video3         
def menu(demise_counter): #the menu screen that contains all the visuals and sound effects 
    global points 
    while True:
        screen.fill("light blue")
        
        if demise_counter == 0:
            
            welcome_var = game_font2.render("WELCOME TO IGGY'S RUN!" , True, (0, 0, 0))
            screen.blit(welcome_var, (300, 100))

            text_var = "Press Any Key to Make Iggy Run!"  
            start_text = game_font.render(text_var, True, (0,0,0))

            start_init = game_font.render("Press the space bar or up key to jump!" , True, (0, 0, 0))
            screen.blit(start_init, (460, 410))

            rules_0 = game_font.render("Rules!" , True, (0, 0, 0))
            screen.blit(rules_0, (1000, 410))

            rules_1 = game_font.render("1. Jump over the kiwi bots!" , True, (0, 0, 0))
            screen.blit(rules_1, (900, 450))

            rules_2 = game_font.render("2. Don't let the flying books get you" , True, (0, 0, 0))
            screen.blit(rules_2, (880, 490))

            rules_3 = game_font.render("3. HAVE FUN!!!" , True, (0, 0, 0))
            screen.blit(rules_3, (970, 530))

        elif demise_counter > 0:
            theme_song_snd.stop()
            game_over_snd.play()
            start_text = game_font.render("Press the space bar to try again :(", True, (0, 0, 0))
            score = game_font.render("Iggy Points: " + str(points), True, (0, 0, 0))
            score_rect = score.get_rect()
            score_rect.center = (screen_x // 2, screen_y // 2 + 50)
            screen.blit(score, score_rect)
            

        text_rect = start_text.get_rect()
        text_rect.center = (screen_x // 2, screen_y // 1.9)
        screen.blit(start_text, text_rect)
        screen.blit(RUNNING[0], (screen_x // 2.6 - 20, screen_y // 2 - 140))
        screen.blit(OBSTACLES[0], (200, 500))
        screen.blit(OBSTACLES[1], (250, 200))
        screen.blit(OBSTACLES[2], (1000, 100))
        pygame.display.update()

        for event in pygame.event.get(): #link1
            if event.type == pygame.QUIT:
                print("quitting")
                pygame.quit()
                sys.exit() 

            if event.type == pygame.KEYDOWN:
                main_function()


menu(demise_counter=0)


        


