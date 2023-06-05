# Shmup game
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
import pygame
import random
from os import path
import math

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 800
HEIGHT = 800
FPS = 60
POWERUP_TIME = 5000
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
def draw_text1(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
def draw_text2(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    global random_big_moster_time
    global for_time_check
    global boss_time
    if(score>boss_time*10000):
        boss_time+=1
        #여기서 보스추가해주면됨.
        #print("boss time!") 
        m=Mob(2)
    elif(for_time_check>=random_big_moster_time):
        random_big_moster_time=random.randint(1000,1700)
        for_time_check=0
        #체력 높은 몬스터
        m = Mob(1)
    else:    
        cho=random.randint(0,100)
        if cho>=(98-boss_time):
        #여기서 확률로 공격 몬스터 출현. 공격몬스터 타입은 3 
           # print('가차성공')
            m = Mob(3)
        else:
            m=Mob(0)
    all_sprites.add(m)
    mobs.add(m)
    mob_list.append(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.original_img=self.image.copy()
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        #y축으로도 이동
        self.speedy=0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        ##스피드업아이템 체크시간
        self.speedup_time=pygame.time.get_ticks()
        self.speed=8
   ##공격 타입 1이면 총 2이면 레이저 3이면 미사일
        self.type=1
       ##무적 시간
        self.mujuk_time=pygame.time.get_ticks()
        self.powerpower=1
        self.tick=50

        ##아이템 샷 딜레이 구분위해
    def update(self):
        # timeout for powerups
        if (self.power >= 2 or self.type!=1)  and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power = 1
            self.power_time = pygame.time.get_ticks()
            if(self.speed>=10):
                self.shoot_delay=220-(15*boss_time)
            else:
                self.shoot_delay=250
            self.type=1
        #스피드업은 공격아이템과 독립
        if self.speed>=10 and pygame.time.get_ticks() - self.speedup_time > POWERUP_TIME:
            self.speed=8
            #스피드업 중에 다른것 먹엇다면 다른것의 샷딜레이로
            if(self.power!=1):
                self.shoot_delay=250
            else:
                self.shoot_delay=250-(5*self.power*boss_time)
            self.speedup_time = pygame.time.get_ticks()
        #무적은 공격아이템과 독립
        if self.powerpower!=1 and pygame.time.get_ticks() - self.mujuk_time > POWERUP_TIME:
            self.powerpower=1
            self.mujuk_time = pygame.time.get_ticks()    
            self.tick=20
            #이미지 원상복구
            self.image=self.original_img    
            #bgm원상복구
            pygame.mixer.music.load(path.join(snd_dir, bgm_list[now_music]))
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(loops=-1)                
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        #무적이라면..    
        if(self.powerpower==2):
            self.tick+=1
            if(self.tick>17):
                self.tick=1
                new_image = random.choice(unpower_img_list)
                new_image=pygame.transform.scale(new_image, (50, 38))
                new_image.set_colorkey(BLACK)
                old_center = self.rect.center
                self.image = new_image
                self.rect = self.image.get_rect()
                self.rect.center = old_center
        self.speedx = 0
        #y축속도 초기화
        self.speedy=0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -self.speed
        if keystate[pygame.K_RIGHT]:
            self.speedx =self.speed 
        if keystate[pygame.K_UP]:
            self.speedy = -self.speed
        if keystate[pygame.K_DOWN]:
            self.speedy = self.speed               
        if keystate[pygame.K_SPACE]:
            if(self.type==1):
                self.shoot()
            #print("space")
            elif(self.type==2):
                self.lazer_shoot()
            elif(self.type==3):
                self.missile_shot()

        self.rect.x += self.speedx
        self.rect.y+=self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            #경계체크 추가
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT    
    def unlimit(self):
        self.powerpower=2
        self.mujuk_time = pygame.time.get_ticks()  
        pygame.mixer.music.load(path.join(snd_dir, musuk_sound))
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(loops=-1)
    def powerup(self):
        self.type=1
        self.power = 2
        #샷 딜레이는 스피드업 아이템 먹은것 우선으로체크
        if(self.speed!=17):
            self.shoot_delay=250-(10*boss_time)
        self.power_time = pygame.time.get_ticks()
#3개 총발사 먹을시
    def powerupup(self):
        self.type=1
        self.power = 3
        #샷 딜레이는 스피드업 아이템 먹은것 우선으로체크
        if(self.speed!=17):
            self.shoot_delay=250-(15*boss_time)
        self.power_time = pygame.time.get_ticks()
 #스피드업아이템   
    def speedup(self):
        self.speed=17
        self.shoot_delay=220-(15*boss_time)
        self.speedup_time = pygame.time.get_ticks()
 #레이저 아이템
    def lala(self):
        self.type=2
        #총 다연발 아이템이나 레이저 아이템이나 시간은 공유
        self.power_time = pygame.time.get_ticks()
#미사일 아이템
    def mimi(self):
        self.type=3
        #총 다연발 아이템이나 레이저 아이템이나 미사일 시간은 공유
        self.power_time = pygame.time.get_ticks()
    def lazer_shoot(self):
        lazer = Lazer(self.rect.centerx, self.rect.top)
        all_sprites.add(lazer)
        lazer_s.add(lazer)    
        shoot_sound.play()
    def missile_shot(self):
        now = pygame.time.get_ticks()
        #살짝 짧은 슛 딜레이
        if now - self.last_shot > 150:
            self.last_shot = now
            M = Missile(self.rect.centerx, self.rect.top)
            all_sprites.add(M)
            missiles.add(M)     
            missile_launch.play()     
    def shoot(self): 
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.power== 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            elif self.power>= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self,t):
        pygame.sprite.Sprite.__init__(self)
        self.type=t
        if(self.type==0):
            self.image_orig = random.choice(meteor_images)
            self.image_orig.set_colorkey(BLACK)
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.radius = int(self.rect.width * .85 / 2)
            # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.bottom = random.randrange(-80, -20)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)
            self.rot = 0
            self.rot_speed = random.randrange(-8, 8)
            self.last_update = pygame.time.get_ticks()
            #크기별로 몹의 체력추가
            self.health=int(self.radius/10)+1
        #큰 몬스터. 아래로만 움직인다.    
        elif(self.type==1):
            self.image=bit_moster_img
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.radius = 15*boss_time/2
            self.rect.x = 0
            self.rect.bottom = random.randrange(-80, -20)
            self.speedy = 2    
            self.speedx = 0    
            self.health=30+(boss_time*3)
        #보스 몬스터    
        elif(self.type==2):
            self.image=boss_moster_img
            self.image.set_colorkey(BLACK)
            self.rect=self.image.get_rect()
            self.radius=100
            self.rect.centerx = WIDTH / 2
            self.rect.bottom=0
            self.speedy=1
            self.speedx=random.randrange(-40, 40)
            self.last_update = pygame.time.get_ticks()
            self.last_shoot=pygame.time.get_ticks()
            self.health=170+((boss_time-1)*4)
            self.shoot_delay = 1000-90*(boss_time-1)
        #스페셜 몬스터 목표: 0~20사이에서 y축의 움직임. x는 자유롭게    
        elif(self.type==3):
            self.image=special_monster_img
            self.image.set_colorkey(BLACK)
            self.rect=self.image.get_rect()
            self.radius=10*(boss_time)/2
            self.rect.centerx = WIDTH / 2
            self.rect.bottom=0
            self.speedy=2
            self.speedx=random.randrange(-40, 40)
            self.last_update = pygame.time.get_ticks()
            self.last_shoot=pygame.time.get_ticks()
            self.health=12+(boss_time)*4
            self.shoot_delay = 2000-100*(boss_time)
            self.screen_in=1
        #몹의 유형 0일시 일반 1일시 좀 큰몹 2일시 보스

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        if(self.type==0):
            self.rotate()
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        elif(self.type==1):
            self.rect.y+=self.speedy
        elif(self.type==2):
            if(self.rect.top<0):
                self.rect.y+=self.speedy            
            self.shoot(boss_time-1)
            now=pygame.time.get_ticks()
            if(now>=self.last_update+100):
                self.rect.x+=self.speedx
                self.speedx=random.randint(-40,40)
                self.last_update=now
                if(self.rect.left<0):
                    self.rect.left=0
                if(self.rect.right>=800):
                    self.rect.right=800
        elif(self.type==3):
            #일단 화면 밖에서  내려오고
            if(self.screen_in==1):
                if(self.rect.top<0):
                    self.rect.y+=self.speedy
                if(self.rect.top>= 0):
                    #화면에 보이면
                    self.screen_in=2
            elif(self.screen_in==2):
                self.shoot(boss_time)
                now=pygame.time.get_ticks()
                if(now>=self.last_update+200):
                    self.last_update=now
                    self.speedx=random.randint(-200,200)
                    self.speedy=random.randint(-20,20)
                    self.rect.x+=self.speedx
                    self.rect.y+=self.speedy
                    if(self.rect.left<0):
                        self.rect.left=0
                    if(self.rect.right>800):
                        self.rect.right=800
                    if(self.rect.bottom>100):
                        self.rect.bottom=100
                    if (self.rect.top<0):
                        self.rect.top=0
                          
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            if(self.type==0):
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 8)
                #게임 밖에 나갔을때 재등장하는것임. 즉 체력 초기화.
                self.health=int(self.radius/10)+1
            #큰 놈은 화면에서 사지면 그냥 out
            elif(self.type==1):
                self.kill()
                mob_list.remove(self)
                newmob()
    def shoot(self,dd):
        now=pygame.time.get_ticks()
        if now-self.last_shoot > self.shoot_delay:
            self.last_shoot=now
            bullet=Monster_Bullet(self.rect.centerx,self.rect.bottom,dd)
            all_sprites.add(bullet)
            monster_bullets.add(bullet)
            other_gun.play()
def leng(x,y):
    lens=math.sqrt(x*x+y*y)
    #print(lens)
    return lens
class Monster_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y,damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = monster_bullet_im
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10*(boss_time-1)
        #데미지 추가
        self.damage=7*damage
        self.targetx=player.rect.center[0]
        self.targety=player.rect.center[1]
        self.speedx=(self.targetx-x)
        self.speedy=(self.targety-y)
        #목표위치찾고 그에맞춰 이미지 회전
        self.rotate()
        lens=leng(self.speedx,self.speedy)
        if(lens==0):
            lens=0.1
        #목표에게 가는 레이저 속도는 10    
        #print(self.speedx,self.speedy)
        #print("monster: ",x,y)
        #print("my: ",self.targetx,self.targety)
        self.speedx=self.speedx/lens*10
        self.speedy=self.speedy/lens*10

    def update(self):
        self.rect.y += self.speedy
        self.rect.x+=self.speedx
        # kill if it moves off the top of the screen
        if self.rect.bottom > 800:
            self.kill()
    def rotate(self):
        if(self.speedy!=0):
            angle=math.atan(self.speedx/self.speedy)
            rot=(angle*180/math.pi)      
        elif(self.speedy==0): 
            if(self.rect.x<self.targetx):
                rot=90
            else:
                rot=-90

        new_image = pygame.transform.rotate(self.image, rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center  

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        #데미지 추가
        self.damage=1

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()
##레이저 객체. 속도는 없이 그냥 2틱후 삭제            
class Lazer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = random.choice(lazer_img_list)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 0
        self.tick=0

    def update(self):
        self.tick+=1
        # kill if it moves off the top of the screen
        if self.tick >=2:
            self.kill()       
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = missile_img
        self.image=self.image_orig.copy()

        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        c=random.randint(0,len(mob_list)-1)
        '''for i in mob_list:
            if i.rect.center[1]<y:
                break
            else:
                c+=1
        if(c==len(mob_list)):
            c-=1  '''
        self.target=c
        #이거 플레이어 좌표임. 
        self.rect.bottom = y
        self.rect.centerx = x


        self.targetx=mob_list[self.target].rect.center[0]
        self.targety=mob_list[self.target].rect.center[1]
        self.speedy = 0
        self.speedx= 0
 #회전 주기용
        self.last_update = pygame.time.get_ticks()        
    def update(self):
        #목표 몹의 중심좌표
        self.targetx=mob_list[self.target].rect.center[0]
        self.targety=mob_list[self.target].rect.center[1]
        #print("target: ",self.targety)
        self.speedx=self.targetx-self.rect.centerx
        self.speedy=self.targety-self.rect.bottom
        lens=leng(self.speedx,self.speedy)
        if(lens==0):
            lens==0.1
        #print("my : ",self.rect.bottom)
        #print(self.speedy)
        #self.speedx=self.speedx/7
        #self.speedy=self.speedy/20
        self.speedx=self.speedx/lens*22
        self.speedy=self.speedy/lens*22
        #최소 속도 20

        self.rect.x+=self.speedx
        self.rect.y += self.speedy

        # kill if it moves off the top of the screen
        if self.rect.bottom < 0 or self.rect.top>=800 or self.rect.left>=800 or self.rect.right<0:
            self.kill()    
        self.rotate()    
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now   
            rot=0 
            if(self.rect.y>self.targety and self.speedx!=0):
                angle=math.atan(self.speedy/self.speedx)
                rot=(angle*180/math.pi)
                if rot<0:
                    rot=-(angle*180/math.pi)-45
                else:
                    rot=180-(angle*180/math.pi)-45                 
            elif(self.speedx==0):
                if(self.rect.y>self.targety):
                    rot=45
                else:
                    rot=225   
            elif(self.rect.y<self.targety and self.speedx!=0):
                angle=math.atan(self.speedy/self.speedx)
                rot=(angle*180/math.pi)
                if rot>0:
                    rot=360-(angle*180/math.pi )-45
                else:
                    rot=-(angle*180/math.pi)-45+180                 
            new_image = pygame.transform.rotate(self.image_orig, rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center   

class Pow(pygame.sprite.Sprite):
    def __init__(self, center,kill_type):
        pygame.sprite.Sprite.__init__(self)
        self.must=kill_type
        if(kill_type==2):
            self.type='unlimit'
        elif(kill_type==1):
            self.type=random.choice(['gun','super_gun','faster','laser_gun','missile_gun'])
        elif(kill_type==3):
            rans=random.randint(0,100)
            if(rans>=90):
                self.type='unlimit'
            else:
                self.type = random.choice(['shield', 'gun','super_gun','faster','laser_gun','missile_gun'])
        else:
            rans=random.randint(0,100)
            if(rans<40):
                self.type=random.choice(['shield','faster'])
            elif(rans<77):
                self.type=random.choice(['gun','super_gun'])
            elif(rans<98):
                self.type=random.choice(['laser_gun','missile_gun'])
            else:
                #print(rans," ok")
                self.type='unlimit'              
        #self.type = random.choice(['shield', 'gun','super_gun','faster','laser_gun','missile_gun','unlimit'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def show_go_screen():
    screen.blit(background, background_rect)
    global now_music
    pygame.mixer.music.load(path.join(snd_dir, bgm_list[now_music]))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 5)
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT*2 / 5)
    draw_text(screen, "Press a up,down key to change bgm.", 18, WIDTH / 2, HEIGHT * 3 / 5)
    draw_text(screen, "Press a  other key to begin.", 18, WIDTH / 2, HEIGHT * 4 / 5)
    pygame.display.flip()
    waiting = True
    end=False
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end=True
                waiting=False
                #pygame.quit()            
            ##bgm추가 완료
            if event.type == pygame.KEYDOWN:
                if(event.key==pygame.K_UP):

                    now_music+=1
                    if(now_music>=len(bgm_list)):
                        now_music=len(bgm_list)-1
                    pygame.mixer.music.load(path.join(snd_dir, bgm_list[now_music]))
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play(loops=-1)
                elif(event.key==pygame.K_DOWN):
                    now_music-=1
                    if(now_music<0):
                        now_music=0
                    pygame.mixer.music.load(path.join(snd_dir, bgm_list[now_music]))
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play(loops=-1)
                else:
                    waiting = False
    if(end==True):
        pygame.quit()                
#게임 종료시 나오는 함수
def show_end_screen():
    #print("hi")
    end=False
    fp=open("rank.txt","a")
    fp.write(" {}".format(score))
    fp.close()
    fp1=open("rank.txt","r")
    input_data=fp1.readline()
    ranklist=input_data.split(" ")
    rr=[]
    #실수로 변환
    for i in ranklist:
        if(i==''):
            continue
        else:
            fa=float(i)
            rr.append(round(fa,1))
    fp1.close()
    #print(rr)
    rr.sort(reverse=True)
    screen.blit(endground, endground_rect)
    k=1
    draw_text2(screen,"Game Over!!",50,120,20)
    draw_text2(screen,str(score),50,120,70)
    for i in rr:
        draw_text1(screen,"{}s: {}".format(k,i), 14, WIDTH / 2, HEIGHT * k / 50)
        k+=1
    draw_text(screen, "Press Enter key to restart.", 18, WIDTH / 2, HEIGHT * 4 / 5)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end=True
                waiting=False
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    waiting=False 
    if(end==True):
        pygame.quit()
# Load all game graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
endground=pygame.image.load(path.join(img_dir,"end_background.png")).convert()
endground_rect=endground.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png']
#큰 몬스터
bit_moster_img=pygame.image.load(path.join(img_dir, "bigbigmoster.png")).convert()
#보스 몬스터
boss_moster_img=pygame.image.load(path.join(img_dir, "boss_monster.png")).convert()
#스페셜 몬스터
special_monster_img=pygame.image.load(path.join(img_dir, "monster.png")).convert()

#레이저 랜덤사진 리스트    
lazer_1=pygame.image.load(path.join(img_dir, "lazer_red.png")).convert()
lazer_2=pygame.image.load(path.join(img_dir, "lazer_green.png")).convert()
lazer_3=pygame.image.load(path.join(img_dir, "lazer_blue.png")).convert()
lazer_4=pygame.image.load(path.join(img_dir, "lazer_yellow.png")).convert()

#미사일 이미지
missile_img=pygame.image.load(path.join(img_dir, "missile.png")).convert()
##무적 플레이어 이미지.
power_1=pygame.image.load(path.join(img_dir, "red_one.png")).convert()
power_2=pygame.image.load(path.join(img_dir, "blue_one.png")).convert()
power_3=pygame.image.load(path.join(img_dir, "yellow_one.png")).convert()
power_4=pygame.image.load(path.join(img_dir, "green_one.png")).convert()
#몬스터 총알(내것에서 회전. 나중에 업데이트)
monster_bullet_im=pygame.image.load(path.join(img_dir, "monster_bb.png")).convert()


lazer_img_list=[lazer_1,lazer_2,lazer_3,lazer_4]
unpower_img_list=[power_1,power_2,power_3,power_4]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
#3개 총발사 추가
powerup_images['super_gun'] = pygame.image.load(path.join(img_dir, 'bbolt_gold.png')).convert()
#스피드업 아이템 추가
powerup_images['faster'] = pygame.image.load(path.join(img_dir, 'faster.png')).convert()
#레이저 아이템 추가
powerup_images['laser_gun'] = pygame.image.load(path.join(img_dir, 'lazer_item.png')).convert()
#미사일 아이템 추가
powerup_images['missile_gun'] = pygame.image.load(path.join(img_dir, 'missile_item.png')).convert()
##무적 아이템 추가
powerup_images['unlimit'] = pygame.image.load(path.join(img_dir, 'star_mu.png')).convert()
# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow4.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow5.wav'))
gun_hit_sound=pygame.mixer.Sound(path.join(snd_dir, 'gun_hit_sound.wav'))
expl_sounds = []
bgm1='tgfcoder-FrozenJam-SeamlessLoop.wav'
bgm2='second_bgm.wav'
bgm3='bgm_1.wav'
bgm4='bgm_2.wav'
bgm5='bgm_3.wav'
bgm6='bgm_4.wav'
bgm7='bgm_5.wav'
bgm8='bgm_6.wav'
bgm9='bgm_7.wav'



bgm_list=[bgm3,bgm2,bgm1,bgm4,bgm5,bgm6,bgm7,bgm8,bgm9]
now_music=0
type1_s=pygame.mixer.Sound(path.join(snd_dir, 'type1_dye.wav'))
type2_s=pygame.mixer.Sound(path.join(snd_dir, 'type2_dye.wav'))
type3_s=pygame.mixer.Sound(path.join(snd_dir, 'type3_dye.wav'))
###폭발 사운드
for snd in ['expl3.wav', 'expl6.wav','exp1.wav','exp2.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.wav'))
#pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.wav'))
#pygame.mixer.music.set_volume(0.4)
missile_launch= pygame.mixer.Sound(path.join(snd_dir, 'missile_launch.wav'))
missile_hit= pygame.mixer.Sound(path.join(snd_dir, 'missile_hit.wav'))

other_gun=pygame.mixer.Sound(path.join(snd_dir, 'alien_laser.wav'))

musuk_sound='limit_power_sound.wav'
#총알 맞는소리
hitted=pygame.mixer.Sound(path.join(snd_dir, 'ss1.wav'))
ting=pygame.mixer.Sound(path.join(snd_dir, 'ting.wav'))

#pygame.mixer.music.play(loops=-1)
# Game loop
game_over = True
running = True
score=0
game_time=0
end_time=0
#random_big_moster_time=random.randint(500,1500)
random_big_moster_time=random.randint(1000,1700)
while running:
    if game_over:
        #재시작 할시. 이게 다름
        if(game_time!=end_time):
            #이전 몹 정보들 삭제(미사일용)
            for i in mobs:
                i.kill()
                mob_list.remove(i)
                #print("응애응애")
            for i in all_sprites:
                i.kill()
                #print("응애")  
            #랭킹 체킹 함수
            show_end_screen()
            end_time+=1
          
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        lazer_s=pygame.sprite.Group()
        missiles=pygame.sprite.Group()
        #몬스터의 총알. 플레이어와의 충돌만 생각
        monster_bullets=pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        mob_list=[]
        for_time_check=0
        musuk_attack_time=0
        boss_time=1
        score = 0
        for i in range(12):
            newmob()

        game_time+=1
    for_time_check+=1
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
    for hit in hits:
        hit.health-=(1*(boss_time))
        if(hit.health<=0):
            hit.kill()
            mob_list.remove(hit)
            for_item=random.random()
            score += 20 + hit.radius
            #다양한 폭발음
            if(hit.type==1):
                type1_s.play()
                for_item=1
            elif(hit.type==2):
                type2_s.play()
                for_item=1
            elif(hit.type==3):
                ran=random.randint(0,100)
                if(ran<=85):
                    type3_s.play()
                else:
                    random.choice(expl_sounds).play()  
                for_item=1      
            else:            
                random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if for_item > 0.7+(boss_time/90):
                pow = Pow(hit.rect.center,hit.type)
                all_sprites.add(pow)
                powerups.add(pow)
            newmob()
        else:
            gun_hit_sound.play()

    hits = pygame.sprite.groupcollide(mobs, lazer_s, False, False)
    for hit in hits:
        hit.health-=(0.3+(boss_time/20))
        #print(hit.health)
        if(hit.health<=0):
            mob_list.remove(hit)
            hit.kill()
            score += 20 + hit.radius
            for_item=random.random()
            if(hit.type==1):
                type1_s.play()
                for_item=1
            elif(hit.type==2):
                type2_s.play()
                for_item=1
            elif(hit.type==3):
                for_item=1
                ran=random.randint(0,100)
                if(ran<=85):
                    type3_s.play()
                else:
                    random.choice(expl_sounds).play()        
            else:            
                random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if for_item > 0.7+(boss_time/90):
                pow = Pow(hit.rect.center,hit.type)
                all_sprites.add(pow)
                powerups.add(pow)
 
            newmob()
        else:
            gun_hit_sound.play()
    hits = pygame.sprite.groupcollide(mobs, missiles, False, True)
    for hit in hits:
        hit.health-=(5+boss_time/2)
        if(hit.health<=0):
            mob_list.remove(hit)
            hit.kill()
            score += 20 + hit.radius
            for_item=random.random()
            if(hit.type==1):
                type1_s.play()
                for_item=1
            elif(hit.type==2):
                type2_s.play()
                for_item=1
            elif(hit.type==3):
                for_item=1
                ran=random.randint(0,100)
                if(ran<=85):
                    type3_s.play()
                else:
                    random.choice(expl_sounds).play()        
            else:            
                random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if for_item > 0.7+(boss_time/90):
                pow = Pow(hit.rect.center,hit.type)
                all_sprites.add(pow)
                powerups.add(pow)
 
            newmob()
        else:
           missile_hit.play()
    #플레이어와 몬스터 총알의 충돌
    hits = pygame.sprite.spritecollide(player, monster_bullets, True)#, pygame.sprite.collide_circle)
    for hit in hits:
        if(player.powerpower==1):
            #print("총이 아파")
            hitted.play()
            player.shield -= hit.damage
            if player.shield <= 0:
                player_die_sound.play()
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100      
                #죽을시 무적아이템 하나
                pow = Pow([WIDTH/2,10],2)
                all_sprites.add(pow)
                powerups.add(pow)
        else:
            ting.play()
    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, False)#, pygame.sprite.collide_circle)
    for hit in hits:
        if(player.powerpower==1):
            #print("아파")
            #print(hit, hit.radius)
            player.shield -= hit.radius * 2
            expl = Explosion(hit.rect.center, 'sm')
            if(hit.type==1):
                type1_s.play()
            elif(hit.type==2):
                type2_s.play()
            elif(hit.type==3):
                ran=random.randint(0,100)
                if(ran<=85):
                    type3_s.play()
                else:
                    random.choice(expl_sounds).play()        
            else:            
                random.choice(expl_sounds).play()
            all_sprites.add(expl)
            hit.kill()
            mob_list.remove(hit)
            newmob()
            if player.shield <= 0:
                player_die_sound.play()
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100
                #죽을시 무적아이템 하나
                pow = Pow([WIDTH/2,10],2)
                all_sprites.add(pow)
                powerups.add(pow)
        #무적시엔 돌만 파괴. 내체력은 달지 않음
        else:
            if(pygame.time.get_ticks()>=musuk_attack_time+40 and hit.type!=2):
                musuk_attack_time=pygame.time.get_ticks()
                #if(hit.type!=2):  보스몹은 무적에 안맞게?
                hit.health-=(10)
                #print(hit.health)
                if(hit.health<=0):
                    mob_list.remove(hit)
                    hit.kill()
                    for_item=random.random()
                    score += 20 + hit.radius
                    if(hit.type==1):
                        type1_s.play()
                        for_item=1
                    elif(hit.type==2):
                        type2_s.play()
                        for_item=1
                    elif(hit.type==3):
                        for_item=1
                        ran=random.randint(0,100)
                        if(ran<=85):
                            type3_s.play()
                        else:
                            random.choice(expl_sounds).play()        
                    else:            
                        random.choice(expl_sounds).play()
                    expl = Explosion(hit.rect.center, 'lg')
                    all_sprites.add(expl)
                    if for_item > 0.7+(boss_time/90):
                        pow = Pow(hit.rect.center,hit.type)
                        all_sprites.add(pow)
                        powerups.add(pow)
        
                    newmob()
                else:
                    gun_hit_sound.play()
            
            '''score += 20 + hit.radius
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            mob_list.remove(hit)
            if random.random() > 0.1:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow) 
            newmob()'''
          

    # check to see if player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            shield_sound.play()
            if player.shield >= 100:
                #print(player.shield)
                player.shield = 100
                #print(player.shield)
        if hit.type == 'gun':
            player.powerup()
            power_sound.play()
        if hit.type == 'super_gun':
            player.powerupup()
            power_sound.play()    
        if hit.type=='faster':
            player.speedup()
            power_sound.play()        
        if hit.type=='laser_gun':
            player.lala()
            power_sound.play()            
        if hit.type=='missile_gun':
            player.mimi()
            power_sound.play()    
        if hit.type=='unlimit':
            player.unlimit()
            musuk_attack_time=pygame.time.get_ticks()
           # print(musuk_attack_time)

    # if the player died and the explosion has finished playing
    if player.lives == 0:# and not death_explosion.alive():
        game_over = True

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # *after* drawing everything, flip the display 
    pygame.display.flip()

pygame.quit()
