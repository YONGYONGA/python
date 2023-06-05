# Draw a robot arm with multiple joints, controlled with keyboard inputs
#
# -*- coding: utf-8 -*- 

import pygame
import numpy as np
import os
# 게임 윈도우 크기
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 900
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'folder')
im = pygame.image.load(os.path.join(assets_path, 'windmill_background.png'))
# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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

# 윈도우 제목
pygame.display.set_caption("Drawing")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

# 게임 종료 전까지 반복
done = False
# 폰트 선택(폰트, 크기, 두껍게, 이탤릭)
font = pygame.font.SysFont('FixedSys', 40, True, False)
font1 = pygame.font.SysFont('FixedSys', 20, True, False)
#연결 라인
connect=np.array( [[0, 0, 1], [40, 0, 1], [40, 10, 1], [0, 10, 1]])
connect=connect.T
joint=np.array([33,5,1])
# 날개
poly = np.array( [[0, 0, 1], [200, 0, 1], [200, 59, 1], [0, 59, 1]])
poly = poly.T # 3x4 matrix 

cor = np.array([10, 10, 1])

cor1 = np.array([70, 0, 1])
cor11 = np.array([70, 59, 1])
cor2 = np.array([140, 0, 1])
cor22 = np.array([140, 59, 1])
cor3= np.array([0,30 , 1])
cor33= np.array([200, 30, 1])


joint1=np.array([90,10,1])

hand = np.array( [[0, 0, 1], [50, 0, 1], [50, 30, 1], [0, 30, 1]])
finger=np.array( [[0, 0, 1], [7, 0, 1], [7, 30, 1], [0, 30, 1]])
#hand = np.array( [[0, 0, 1], [100, 0, 1], [100, 20, 1], [0, 20, 1]])
hand = hand.T # 3x4 matrix 
finger=finger.T
fin1=np.array([17, 20, 1])
fin2=np.array([34, 20, 1])

degree = 10
degree2=10
degree3=10
degree4=-80
wind_dg=10
def muls(k):
    one=k@cor1
    two=k@cor11
    three=k@cor2
    four=k@cor22
    five=k@cor3
    six=k@cor33
    pygame.draw.line(screen,BLACK,one[:2],two[:2],2)
    pygame.draw.line(screen,BLACK,three[:2],four[:2],2)
    pygame.draw.line(screen,BLACK,five[:2],six[:2],2) 
speed=1   
# 게임 반복 구간
while not done:
    screen.fill(WHITE)
    screen.blit(im,(0,0))
# 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_UP]:
        speed+=0.5
    elif keystate[pygame.K_DOWN]:
        speed-=0.5           
    wind_dg+=speed
    # 윈도우 화면 채우기

    #windmill
    pygame.draw.polygon(screen,(150,75,0),[[200,900],[200,400],[300,300],[400,400],[400,900]])
    pygame.draw.rect(screen, WHITE, [250,450,100,100])
    pygame.draw.line(screen,BLACK,[300,450],[300,550],2)
    pygame.draw.line(screen,BLACK,[250,500],[350,500],2)
    ##중심
    pygame.draw.circle(screen,GREEN,[300,350],2)

    ##풍차와 연결connect 연결
    H = Tmat(300, 350) @ Rmat(wind_dg)
    pp = H @ connect
    joint11=H@joint
    q = pp[0:2, :].T # N x 2 matrix
    pygame.draw.polygon(screen, RED, q)
    pygame.draw.circle(screen, (255, 128, 128), joint11[:2], 3)

    H = Tmat(300, 350) @ Rmat(wind_dg+90)
    pp = H @ connect
    joint22=H@joint
    q = pp[0:2, :].T # N x 2 matrix
    pygame.draw.polygon(screen, RED, q)
    pygame.draw.circle(screen, (255, 128, 128), joint22[:2], 3)    

    H = Tmat(300, 350) @ Rmat(wind_dg+180)
    pp = H @ connect
    joint33=H@joint
    q = pp[0:2, :].T # N x 2 matrix
    pygame.draw.polygon(screen, RED, q)
    pygame.draw.circle(screen, (255, 128, 128), joint33[:2], 3)

    H = Tmat(300, 350) @ Rmat(wind_dg+270)
    pp = H @ connect
    joint44=H@joint
    q = pp[0:2, :].T # N x 2 matrix
    pygame.draw.polygon(screen, RED, q)
    pygame.draw.circle(screen, (255, 128, 128), joint44[:2], 3)    

    ##connect와 날개 연결 joint11 ~~joint44를 이용해 연결하면됨
    H = Tmat(joint11[0],joint11[1]) @ Rmat(wind_dg)
    pp = H @ poly
    q = pp[0:2, :].T # N x 2 matrix
    pygame.draw.polygon(screen, GREEN, q)
    muls(H)
    
    H = Tmat(joint22[0],joint22[1]) @ Rmat(wind_dg+90)
    pp = H @ poly
    q = pp[0:2, :].T # N x 2 matrix
    pygame.draw.polygon(screen, GREEN, q) 
    muls(H)

    H = Tmat(joint33[0],joint33[1]) @ Rmat(wind_dg+180)
    pp = H @ poly
    q = pp[0:2, :].T # N x 2 matrix
    pygame.draw.polygon(screen, GREEN, q)
    muls(H)

    H = Tmat(joint44[0],joint44[1]) @ Rmat(wind_dg+270)
    pp = H @ poly
    q = pp[0:2, :].T # N x 2 matrix
    pygame.draw.polygon(screen, GREEN, q)
    muls(H)

##여까지 연결 완
    text = font.render("NOW SEEPD : {}".format(speed), True, BLACK)
    screen.blit(text, [100, 30])
    text = font1.render("Adjust the speed using the up and down keys", True, BLACK)
    screen.blit(text, [20, 70])
    pygame.display.flip()
    clock.tick(60)

# 게임 종료
pygame.quit()