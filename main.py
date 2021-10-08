import pygame as pg
import random as r
import sys

print('''RULES
1. Hit any balloons you want on the night background, but keep track of them, because in the future you are going to need to remember those
2. On the day background, hit the same balloons you hit on the night background
3. If you hit the correct balloons, you get a point
4. Hit different balloons each time you're on the night background! Don't hit the same balloon, (unless you really want to cheat your brain)
Haven't found a way to stop that yet :(

''')
print("Sorry, it's taking a minute...")

pg.init()

gun_sound = pg.mixer.Sound('gun.wav')
gun_sound.set_volume(0.2)
balloon_sound = pg.mixer.Sound('balloon.wav')
balloon_sound.set_volume(0.2)
night = pg.mixer.Sound('night_sound.wav')
night.set_volume(0.2)
morning = pg.mixer.Sound('morning_sound.wav')
morning.set_volume(0.2)
myfont = pg.font.SysFont('arial black', 30)

bg = pg.image.load('background.jpg')# Background Image #
bg = pg.transform.scale(bg, (688,387))
new_bg = pg.image.load('background2.jpg')
new_bg = pg.transform.scale(new_bg, (688,387))

radius = 30
diameter = 2 * radius

num_balloons = 7
num_hits = 0
bullets_colors_ls = []
iterator = -1

num_balloon_list = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7]
balloon_list_index = 0
scene_1_balloons_popped = []
scene_2_balloons_popped = []
number_of_balloons_popped = 0
number_incorrect = 0
lost = False

def create_balloons():
    global balloon_list
    global colors

    for i in range(num_balloons):
        while True:
            candidate = r.randint(0, 500)
            if all(abs(candidate-x) >= diameter for x in balloon_list):
                break
        balloon_list.append(candidate)

def draw_balloons(y):
    for i in range(num_balloons):
        screen.blit(colors[i], (balloon_list[i] , y-50))


def check_collisions(x, y):
    global hit_var, hit, score, scoretext, bg_bool
    global num_balloon_list, balloon_list_index, num_hits
    global num_balloons, new_hit_var
    global balloon_hit, game_over, number_of_balloons_popped 
    
    for i in range(num_balloons):
        gun_rect = gun.get_rect(topleft = (x,y))
        gun_mask = pg.mask.from_surface(gun)
        
        balloon_rect = colors[i].get_rect(topleft = (balloon_list[i], y-100))
        balloon_mask = pg.mask.from_surface(colors[i])

        offset = (balloon_rect.x - gun_rect.x), (balloon_rect.y - gun_rect.y)
        if gun_mask.overlap(balloon_mask, offset):
            hit = True
            if bg_bool == False:                  
                scene_1_balloons_popped.append(i)
                morning.play()
                night.stop()
            elif bg_bool == True:                  
                scene_2_balloons_popped.append(i)
                night.play()
                morning.stop()
                
            balloon_sound.play()
            num_balloons -= 1
            num_hits += 1
            number_of_balloons_popped += 1
            num_hits_needed = num_balloon_list[balloon_list_index]
            game_end = balloon_list_index == len(num_balloon_list) - 1
            if num_hits == num_hits_needed and not game_end:
                num_balloons += num_hits
                num_hits = 0
                balloon_list_index += 1
                bg_bool = not bg_bool
            break

            


            


def bullets_colors():
    for i in range(1,8):
        bulletsvar = (r.choice([0,255]), r.randint(0,255), r.choice([0,255])) # bullets color auto generated using random #
        bullets_colors_ls.append(bulletsvar)
        
def make_bullets():
    global iterator
    global bullets_colors_ls
    for i in range(7):
        iterator += 1
        
        pg.draw.circle(screen, bullets_colors_ls[iterator],(x, y), radius=15)
        

def you_lost():
    youlost = myfont.render("YOU LOST!", 1, (0,0,0))
    message1 = myfont.render("Your memory is kinda garbage, sorry", 1, (0,0,0))
    message2 = myfont.render("If I 'Remember' correctly, you only got a 4", 1, (0,0,0))
    message3 = myfont.render("Good job! You have great memory!", 1, (0,0,0))
    screen.blit(youlost, (230, 150))
    if score <= 3:
        screen.blit(message1, (40, 200))
    if score == 4:
        screen.blit(message2, (30, 200))
    elif score >= 5:
        screen.blit(message3, (50, 200))
    

        
# Vars #
x = 0
y = 250
velocity = 5
score = 0
hit = False
bg_bool = False
testvar1 = True
clock = pg.time.Clock()


screen = pg.display.set_mode((688 ,387)) # Size of the screen #
caption = pg.display.set_caption("Remember") # Title of the window #

balloon_list = []
b1 = pg.image.load('balloons/1.png').convert_alpha()
b1 = pg.transform.scale(b1, (63,131))
b2 = pg.image.load('balloons/2.png').convert_alpha()
b2 = pg.transform.scale(b2, (63,131))
b3 = pg.image.load('balloons/3.png').convert_alpha()
b3 = pg.transform.scale(b3, (63,131))
b4 = pg.image.load('balloons/4.png').convert_alpha()
b4 = pg.transform.scale(b4, (63,131))
b5 = pg.image.load('balloons/5.png').convert_alpha()
b5 = pg.transform.scale(b5, (63,131))
b6 = pg.image.load('balloons/6.png').convert_alpha()
b6 = pg.transform.scale( b6, (63,131))
b7 = pg.image.load('balloons/7.png').convert_alpha()
b7 = pg.transform.scale(b7, (63,131))
colors = [b1, b2, b3, b4, b5, b6, b7]




gun = pg.image.load('game-gun.png').convert_alpha()
gun = pg.transform.scale(gun, (150,150))

create_balloons()

pg.mixer.music.load('main-song.wav')
pg.mixer.music.set_volume(0.4)
pg.mixer.music.play(-1)

pg.display.flip() # Updating #

running = True # Game loop bool #

while running: # Game loop #
    clock.tick(60)
    scoretext = myfont.render("SCORE: "+str(score), 1, (0,0,0))
    if bg_bool == False:
        screen.blit(bg, (0, 0))
        screen.blit(scoretext, (5, 10))

      
    elif bg_bool == True:
        screen.blit(new_bg, (0,0))
        screen.blit(scoretext, (5, 10))

            
    if hit == True:
        r.shuffle(balloon_list)
        hit = False
        if len(scene_1_balloons_popped) > 0 and len(scene_2_balloons_popped) > 0:             
            for b in range(min(len(scene_1_balloons_popped), len(scene_2_balloons_popped))):  
                if scene_1_balloons_popped[b] != scene_2_balloons_popped[b]:                  
                    lost = True                                                               
                    break
            if not lost and len(scene_1_balloons_popped) == len(scene_2_balloons_popped):  
                score += 1
            
                   
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        
            if event.key == pg.K_SPACE:
                gun_sound.play()
                bullets_colors()
                make_bullets() 
                check_collisions(x, y)

    draw_balloons(y)
    
    keys = pg.key.get_pressed()
    x += keys[pg.K_RIGHT] - keys[pg.K_LEFT] * velocity
    x -= keys[pg.K_LEFT] - keys[pg.K_RIGHT] * velocity
    if lost:       
        you_lost()  
    
        
     
    screen.blit(gun, (x, y))
    pg.display.update()
    

