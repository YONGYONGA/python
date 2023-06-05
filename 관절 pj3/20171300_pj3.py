# Draw a robot arm with multiple joints, controlled with keyboard inputs
#
# -*- coding: utf-8 -*- 

import pygame
import numpy as np

# 게임 윈도우 크기
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 900

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
font1=pygame.font.SysFont('FixedSys', 27, True, False)

# poly: 4 x 3 matrix
poly = np.array( [[0, 0, 1], [100, 0, 1], [100, 20, 1], [0, 20, 1]])
poly = poly.T # 3x4 matrix 

cor = np.array([10, 10, 1])
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
mode=2
# 게임 반복 구간
while not done:
# 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_1:
                mode=1
            elif event.key==pygame.K_2:
                mode=2
    if(mode==2):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            degree += 1
        elif keystate[pygame.K_s]:
            degree2+=1
        elif keystate[pygame.K_d]:
            degree3+=1           
        elif keystate[pygame.K_f]:
            degree4+=1
        elif keystate[pygame.K_q]:
            degree-=1
        elif keystate[pygame.K_w]:
            degree2-=1           
        elif keystate[pygame.K_e]:
            degree3-=1 
        elif keystate[pygame.K_r]:
            degree4-=1                 
    elif(mode==1):
        degree+=np.random.randint(-2,2)    
        degree2+=np.random.randint(-2,2)
        degree3+=np.random.randint(-2,2)
        degree4+=np.random.randint(-2,2)  
        

    # 윈도우 화면 채우기
    screen.fill(WHITE)
    text = font.render("1:auto 2:control", True, BLACK)
    screen.blit(text, [300, 50])
    text = font.render("NOW MODE : {}".format(mode), True, BLUE)
    screen.blit(text, [300, 100])
    text = font1.render("q,w,e,r for -degree", True, BLACK)
    screen.blit(text, [400, 170])
    text = font1.render("a,s,d,f for +degree", True, BLACK)
    screen.blit(text, [400, 200])
    pygame.draw.rect(screen, BLACK, [0,100,80,170], 4)
    pygame.draw.circle(screen, BLACK,[50,160] , 4)
    pygame.draw.rect(screen, BLACK, [0,220,40,20], 4)
    pygame.draw.rect(screen, BLACK, [0,270,170,500], 4)
    pygame.draw.polygon(screen,BLACK,[[100,690],[130,690],[150,900],[120,900]],4)
    # 다각형 그리기
    # poly: 3xN 
    #pygame.draw.polygon(screen, GREEN, poly[:2].T, 4)


    H = Tmat(100, 400) @ Tmat(10, 10) @ Rmat(degree)
    pp = H @ poly
    corp = H @ cor
    joint11=H@joint1
    # print(pp.shape, pp, pp.T )

    q = pp[0:2, :].T # N x 2 matrix
    pygame.draw.polygon(screen, RED, q, 4)
    pygame.draw.circle(screen, (255, 128, 128), corp[:2], 3)
    pygame.draw.circle(screen, (255, 128, 128), joint11[:2], 3)


    #첫번째 관절 업데이트
    H = Tmat(joint11[0],joint11[1]) @ Rmat(degree2)@ Tmat(-10, -10)
    pp = H @ poly
    corp = H @ cor
    joint22=H@joint1    
    q = pp[0:2, :].T 
    pygame.draw.polygon(screen, GREEN, q, 4)
    pygame.draw.circle(screen, (255, 128, 128), corp[:2], 3)
    pygame.draw.circle(screen, (255, 128, 128), joint22[:2], 3)

    ##두번째 관절
    H = Tmat(joint22[0],joint22[1]) @ Rmat(degree3)@ Tmat(-10, -10)
    pp = H @ poly
    corp = H @ cor
    joint33=H@joint1    
    q = pp[0:2, :].T 
    pygame.draw.polygon(screen, BLUE, q, 4)
    pygame.draw.circle(screen, (255, 128, 128), corp[:2], 3)
    pygame.draw.circle(screen, (255, 128, 128), joint33[:2], 3)

    ##손
    H = Tmat(joint33[0],joint33[1]) @ Rmat(degree4)@ Tmat(-24, -10)
    pp = H @ hand
    fins = H @ fin1
    finss=H@fin2
    q = pp[0:2, :].T 
    pygame.draw.polygon(screen, (100,100,100), q, 4)
    pygame.draw.circle(screen, (255, 128, 128), fins[:2], 3)
    pygame.draw.circle(screen, (255, 128, 128), finss[:2], 3)
    ##손가락
    H = Tmat(fins[0],fins[1]) @ Rmat(degree4)@Tmat(-2,0)
    pp = H @ finger
    q = pp[0:2, :].T 
    pygame.draw.polygon(screen, BLACK, q, 4)

    H = Tmat(finss[0],finss[1]) @ Rmat(degree4)@Tmat(-2,0)
    pp = H @ finger
    q = pp[0:2, :].T 
    pygame.draw.polygon(screen, BLACK, q, 4)

    # 안티얼리어스를 적용하고 검은색 문자열 렌더링
    #text = font.render("Hello Pygame", True, BLACK)
    #screen.blit(text, [200, 600])

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

# 게임 종료
pygame.quit()