# -*- coding: utf-8 -*- 

import pygame
import numpy as np 
import os
import math
#

# 게임 윈도우 크기
WINDOW_WIDTH = 1900
WINDOW_HEIGHT = 1000

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 200, 180)
STAR_C=(255,255,204)
YELLOW=(255,255,0)
def Rmat(degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array( [[ c, -s, 0], [s, c, 0], [0, 0, 1] ] )
    return R

def Tmat(a,b):
    H = np.eye(3)
    H[0,2] = a
    H[1,2] = b
    return H
# Pygame 초기화
pygame.init()
info = pygame.display.Info()
print(WINDOW_WIDTH, WINDOW_HEIGHT)




# 윈도우 제목
pygame.display.set_caption("star")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

# 게임 종료 전까지 반복
done = False
class stars:
    def __init__(self,cor,color):
        self.center=cor
        self.color=color
        self.cout=1
        self.c=0
    def update(self):
        if(self.cout>100):
            self.c=-10
        elif(self.cout<0):
            self.c=0
            self.cout=0
            self.color=(153,153,0)
        self.cout+=self.c

# 폰트 선택(폰트, 크기, 두껍게, 이탤릭)
font = pygame.font.SysFont('FixedSys', 40, True, False)
starslist=[]
for i in range(100):
    a=stars([np.random.randint(0,WINDOW_WIDTH),np.random.randint(0,WINDOW_HEIGHT)],(153,153,0))
    starslist.append(a)
def twinkle():
    randomlist=[]
    i=1
    while i<=20:
        random=np.random.randint(0,100)
        if random in randomlist:
            continue
        else:
            randomlist.append(random)
            i+=1
    for i in range(20):
        starslist[randomlist[i]].color=YELLOW
        starslist[randomlist[i]].cout=101
    #print(randomlist)
def check():
    global dx 
    global dy
    if(x<40 or x>WINDOW_WIDTH-20):
        dx*=-1
    elif(y<40 or y>WINDOW_HEIGHT-20):
        dy*=-1
    if(dx<0 and dy<0):
        pic=pygame.transform.rotate(starship,90)
    elif(dx<0 and dy>0):
        pic=pygame.transform.rotate(starship,180)      
    elif(dx>0 and dy<0):
        pic=starship 
    else:
        pic=pygame.transform.rotate(starship,270)  
    screen.blit(pic,[x-20, y-20])    
for_timer=0



current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'folder')
im = pygame.image.load(os.path.join(assets_path, 'sun.png'))
venus=pygame.image.load(os.path.join(assets_path, 'venus.png'))
earth=pygame.image.load(os.path.join(assets_path, 'earth.png'))
moon=pygame.image.load(os.path.join(assets_path, 'moon.png'))
saturn=pygame.image.load(os.path.join(assets_path, 'saturn.png'))
taitan=pygame.image.load(os.path.join(assets_path, 'taitan.png'))
starship=pygame.image.load(os.path.join(assets_path, 'stars_ship.png'))
##각자의 위치,각도(원점이 태양이라 생각 변환후 이동)
#금성
ve = np.array([100,0, 1])
ve_dg = 10
#지구와 달
ea=np.array([200,0,1])
ea_dg=20
mo_dg=20
#지구~달의 거리
mo=np.array([70,0,1])

##토성과 달 타원임이건.
xRadius = 450
yRadius = 300
sa=np.array([300,0,1])
sa_dg=20
ta_dg=20
#공전주기 29년
for_cal=360/(29*12*30)
#토성~달의 거리
ta=np.array([80,0,1])

#우주선 움직이기
dx=2
dy=2
x=220
y=120

# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # 게임 로직 구간
    for_timer+=1
    # 각도 계산
    ve_dg+=360/225
    ea_dg+=360/365
    mo_dg+=360/27
    sa_dg+=for_cal
    ta_dg+=360/16
    # 윈도우 화면 채우기
    screen.fill(BLACK)
    for i in range(100):
        pygame.draw.circle(screen,starslist[i].color,starslist[i].center,2)
        starslist[i].update()
    # 안티얼리어스를 적용하고 검은색 문자열 렌더링
    if for_timer>=100:
        twinkle()
        for_timer=1
    ##태양그리고(중심 고정)
    screen.blit(im, [WINDOW_WIDTH/2-60, WINDOW_HEIGHT/2-60])    

    ##금성 그리고 (태양중심 회전)
    #pygame.draw.circle(screen,WHITE,[WINDOW_WIDTH/2,WINDOW_HEIGHT/2],100,1)
    H = Tmat(WINDOW_WIDTH/2,WINDOW_HEIGHT/2) @ Rmat(ve_dg)
    corp = H @ ve
    screen.blit(venus, corp[:2]-[20,20])

    ##지구와 달(달은 지구 중심이다.)
    #pygame.draw.circle(screen,WHITE,[WINDOW_WIDTH/2,WINDOW_HEIGHT/2],200,1)    
    H = Tmat(WINDOW_WIDTH/2,WINDOW_HEIGHT/2) @ Rmat(ea_dg)
    corp = H @ ea
    screen.blit(earth, corp[:2]-[35,35])
    H=Tmat(corp[0],corp[1]) @ Rmat(mo_dg)
    corp = H @ mo
    screen.blit(moon, corp[:2]-[10,10])

    ##토성과 달
    #타원계산, 그후 달 변환
    x1 = int(math.cos(sa_dg * 2*  math.pi / 360) * xRadius) + WINDOW_WIDTH/2
    y1 = int(math.sin(sa_dg * 2* math.pi / 360) * yRadius) + WINDOW_HEIGHT/2
    #pygame.draw.ellipse(screen, WHITE, [500, 200, 900, 600], 1)
    screen.blit(saturn,[x1-44, y1-44])
    H=Tmat(x1,y1) @ Rmat(ta_dg)
    corp = H @ ta
    screen.blit(taitan, corp[:2]-[10,10])

    ##우주선



    x+=dx
    y+=dy
    check()
    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

# 게임 종료
pygame.quit()