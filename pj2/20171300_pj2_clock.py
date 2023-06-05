import pygame
import numpy as np
import datetime
# 게임 윈도우 크기
WINDOW_WIDTH = 590
WINDOW_HEIGHT = 599

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

def drawclock():
    pygame.draw.circle(screen,BLACK,[285,285],290,1)
    for i in range(1,13):
        k=i
        text = font.render(str(k), True, BLACK)
        radian=np.deg2rad(30*(k-3))
        if(i==9):
            screen.blit(text, [(np.cos(radian))*290+299, (np.sin(radian))*290+285])   
        elif(i==12):
            screen.blit(text, [(np.cos(radian))*290+285, (np.sin(radian))*290+299])  
        else:
            screen.blit(text, [(np.cos(radian))*290+285, (np.sin(radian))*290+285])        
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
font = pygame.font.SysFont('FixedSys', 20, True, False)

# poly: 4 x 3 matrix
spoly = np.array( [[0, 0, 1], [270, 0, 1],[290,10,1], [270, 20, 1], [0, 20, 1]])
spoly = spoly.T # 3x4 matrix 
mpoly = np.array( [[0, 0, 1], [200, 0, 1],[220,10,1], [200, 20, 1], [0, 20, 1]])
mpoly = mpoly.T # 3x4 matrix 
hpoly = np.array( [[0, 0, 1], [150, 0, 1],[170,10,1], [150, 20, 1], [0, 20, 1]])
hpoly = hpoly.T # 3x4 matrix 

cor = np.array([10, 10, 1])
s=datetime.datetime.now()
sec=s.second
min=s.minute
hour=s.hour
degree = 10
degree2=10
degree3=10
screen.fill(WHITE)
drawclock()
# 게임 반복 구간
while not done:
# 이벤트 반복 구간

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    s=datetime.datetime.now()
    if(sec!=s.second): ##1초마다 이벤트 발생(초침변경)
        sec=s.second
        screen.fill(WHITE)
        drawclock()
        min=s.minute
        hour=s.hour
        degree=sec
        # 각도 조절
        #print(sec,min,hour)
        #print(degree,degree2,degree3)
        degree =(sec*6)-90
        degree2=(min*6)-90
        degree3=((hour%12)*30)-90
        #초침
        H = Tmat(285, 285) @ Rmat(degree)
        pp = H @ spoly
        corp = H @ cor
        # print(pp.shape, pp, pp.T )

        q = pp[0:2, :].T # N x 2 matrix
        pygame.draw.polygon(screen, RED, q, 4)
        pygame.draw.circle(screen, (255, 128, 128), corp[:2], 3)

        #분침
        H = Tmat(285, 285) @ Rmat(degree2)@Tmat(0,-5)
        pp = H @ mpoly

        q = pp[0:2, :].T # N x 2 matrix
        pygame.draw.polygon(screen, BLACK, q, 4)
        #시침
        H = Tmat(285, 285) @ Rmat(degree3)@Tmat(-8,0)
        pp = H @ hpoly
        q = pp[0:2, :].T # N x 2 matrix
        pygame.draw.polygon(screen, GREEN, q, 4)
        # 화면 업데이트
        pygame.display.flip()
    clock.tick(60)

# 게임 종료
pygame.quit()