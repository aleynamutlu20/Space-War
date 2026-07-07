
from pygame import Rect
import pgzrun
import random


TITLE = "Space War"
WIDTH = 800
HEIGHT = 600

gamestate="menu"
start=Rect(300,300,200,60)
menu=Rect(300,300,200,60)
musicbutton=Rect(300,400,200,60)
exitbutton=Rect(300,500,200,60)
platform=Rect(0,465,800,50)
musicstate="ON"
music.play("startmusic")
meteors=[]
meteor_timing=0
lives=3
lasers=[]
enemy=None
game_timer=0
survived_time=0
win_time=60


    
class Player:
    def __init__(self,x,y,):
        self.actor=Actor("player1",(x,y))
        self.y_speed=0
        self.gravity=0.5
        self.jump_rate=-10
        self.inplatform=False
        self.isjumping=False
        self.isducking=False
        self.current_frame = 1
        self.timer = 0
        self.idle_timer=0

    def action(self):
        
        if (keyboard.right or keyboard.left) and not self.isjumping and not self.isducking:
            self.timer += 1
            
            
            if self.timer >= 10: 
                if self.current_frame == 1:
                    self.actor.image = "player3"
                    self.current_frame = 2
                else:
                    self.actor.image = "player2"
                    self.current_frame = 1
                
        else:
            
            self.actor.image = "player1"
            self.current_frame = 1
            self.timer = 0


        if keyboard.left or keyboard.a:
            self.actor.x-=5
        elif keyboard.right or keyboard.d:
            self.actor.x+=5
        


        if self.actor.left < 0:
            self.actor.left=0
        elif self.actor.right > 800:
            self.actor.right = 800
        
        if keyboard.space or keyboard.w or keyboard.up:
            if self.actor.bottom >= 465: 
                self.y_speed = self.jump_rate
                self.inplatform = False
                sounds.jump.play()


        
        self.y_speed += self.gravity
        self.actor.y += self.y_speed


        if self.actor.bottom>=465:
            self.actor.bottom=465
            self.y_speed=0
            self.inplatform=True
        else:
            self.inplatform=False


        if not self.inplatform:
           
            self.actor.image = "playerjump"
            self.isjumping=True
        elif keyboard.s or keyboard.down:
            
            self.actor.image = "playerduck"
            self.actor.bottom=465
            self.isducking=True
        else:
            self.idle_timer += 1
            if self.idle_timer >= 45: 
                if self.actor.image == "player1" :
                    self.actor.image = "player4" 
                else:
                    self.actor.image = "player1"      
                self.idle_timer = 0
            self.actor.bottom=465
            self.isjumping=False
            self.isducking=False

    def drawing(self):
        self.actor.draw()




   


class Meteor:
    def __init__(self):
        comings=[450,360]
        chosen_coming=random.choice(comings)
        self.actor=Actor("meteor",(850,chosen_coming))
        self.speed_x=random.randint(5,10)

    def action_meteor(self):
        self.actor.x -= self.speed_x
        

    def drawing_meteor(self):
        self.actor.draw()


class Enemy:
    global gamestate
    def __init__(self):
    
        self.actor = Actor("enemy", (850, 150)) 
        self.target_x = 700
        self.shoot_timer = 0
        self.life_timer=0
        self.isleaving=False
        self.direction_y=2

    def action_enemy(self):
        
        self.life_timer += 1
        
        
        if self.life_timer >= 900:
            self.isleaving = True

        
        if self.isleaving:
            
            self.actor.x += 4 
        else:
            
            if self.actor.x > self.target_x:
                self.actor.x -= 2
        
    

        if gamestate=="gamescreen":
            self.shoot_timer += 1
            if self.shoot_timer >= 90: 
            
                lasers.append(Laser(self.actor.x, self.actor.y))
                self.shoot_timer = 0
                sounds.lasersound.play()


        self.actor.y += self.direction_y

        if self.actor.y >= 250 or self.actor.y<=80:
            self.direction_y *= -1

    def drawing_enemy(self):
        self.actor.draw()


   
        
class Laser:
    def __init__(self,x,y):
        self.actor = Actor("laser", (x, y)) 
        self.speed_x = 7
        self.speed_y=3
    def action_laser(self):
        self.actor.x -= self.speed_x
        self.actor.y +=self.speed_y

    def drawing_laser(self):
        self.actor.draw()



def reset():
    global lives
    global survived_time
    global game_timer
    global meteor_timing
    global enemy

    lives=3
    survived_time=0
    game_timer=0
    meteor_timing=0
    meteors.clear()
    lasers.clear()
    enemy=None
    hero.actor.pos = (40, 450)
    hero.actor.image = "player1"
    hero.current_frame = 1
    hero.timer = 0
    hero.idle_timer = 0
    hero.y_speed=0
    hero.inplatform=True
    hero.isjumping=False
    hero.isducking=False



def draw():
    screen.clear()
    
    if (gamestate=="menu"):
        screen.fill((24, 28, 56 ))
        screen.draw.text("SPACE WAR", center=(400, 150), fontsize=70, color="cyan", ocolor="white", owidth=1)
        screen.draw.filled_rect(start,(9,35,234))
        screen.draw.text("Start Game",center=start.center,fontsize=24,color="white")
        screen.draw.filled_rect(musicbutton,(9,35,234))

        if musicstate=="ON":

            screen.draw.text("Music=ON",center=musicbutton.center,fontsize=24,color="white")
        else:
            screen.draw.text("Music=OFF",center=musicbutton.center,fontsize=24,color="white")

        screen.draw.filled_rect(exitbutton,(9,35,234))
        screen.draw.text("Exit",center=exitbutton.center,fontsize=24,color="white")




    elif(gamestate=="gamescreen"):
        screen.blit("background",(0,0))
        screen.draw.filled_rect(platform,(149,165,166))
        hero.drawing()
        screen.blit("lives",(30,30))
        screen.draw.text(f"x {lives}", (70, 30), fontsize=24, color="white")
        

        for m in meteors:
            m.drawing_meteor()


        if enemy is not None:
            enemy.drawing_enemy()

        for l in lasers[:]:
            l.drawing_laser()

        screen.draw.text(f"Süre: {int(survived_time)} / {win_time}", (650, 30), fontsize=24, color="white")

    elif gamestate=="gameover":
        screen.fill((24, 28, 56 ))
        screen.draw.text("GAME OVER", center=(400, 150), fontsize=70, color="cyan", ocolor="white", owidth=1)
        screen.draw.filled_rect(menu,(9,35,234))
        screen.draw.text("Menu",center=menu.center,fontsize=24,color="white")

    elif gamestate == "gamewin":
        screen.fill((16, 44, 27)) 
        screen.draw.text("YOU WIN!", center=(400, 150), fontsize=70, color="lime", ocolor="white", owidth=1)
        screen.draw.filled_rect(menu, (9, 35, 234))
        screen.draw.text("Menu", center=menu.center, fontsize=24, color="white")



def on_mouse_down(pos):
    global gamestate
    global musicstate
    if gamestate=="menu":
        if start.collidepoint(pos):
            gamestate="gamescreen"
            if musicstate=="ON":
                music.stop()
                music.play("gamemusic")
            
        elif musicbutton.collidepoint(pos):
            if musicstate=="ON":
                musicstate="OFF"
                music.stop()
            elif musicstate=="OFF":
                musicstate="ON"
                music.play("startmusic")
        elif exitbutton.collidepoint(pos):
            exit()
    if gamestate=="gameover":
        if menu.collidepoint(pos):
            gamestate="menu"
            music.play("startmusic")
            reset()

    if gamestate=="gamewin":
        if menu.collidepoint(pos):
            gamestate = "menu"
            music.play("startmusic")
            reset()
    
            
        
            


def update():
    global gamestate
    global meteor_timing
    global lives
    global game_timer
    global enemy
    global survived_time

    if gamestate != "gamescreen":
        return


    if gamestate=="gamescreen":
        hero.action()
        survived_time += 1/60
        if survived_time>=win_time:
            gamestate="gamewin"
            music.stop()
            lasers.clear()
            meteors.clear() 
            enemy = None
            
        
    if hero.actor.colliderect(platform):
        hero.y_speed=0
        hero.actor.bottom=platform.top
        hero.inplatform=True
    else:
        hero.inplatform=False

    

    meteor_timing+=1

    if meteor_timing==90:
        meteors.append(Meteor())
        meteor_timing=0

    for m in meteors[:]:
        m.action_meteor()

        if hero.actor.colliderect(m.actor):
            lives-=1
            meteors.remove(m)


            if lives==0:
                gamestate="gameover"
                sounds.gameover.play()
                music.stop()
                reset()


        if m.actor.right<0:
            meteors.remove(m)
    
    game_timer +=1
    if game_timer>=120 and enemy is None and game_timer<1300:
        enemy=Enemy()

    if enemy is not None:
        enemy.action_enemy()
        if enemy.isleaving and enemy.actor.left > 850:
                enemy = None
                game_timer=0

    for l in lasers[:]:
        l.action_laser()
        
        if hero.actor.colliderect(l.actor):
            
            lives -=1
            lasers.remove(l)
            
            if lives==0:
                gamestate="gameover"
                sounds.gameover.play()
                lasers.clear()
                music.stop()
                enemy=None
                reset()
        elif l.actor.right<0:
            lasers.remove(l)
            



hero=Player(40,450)
pgzrun.go()
