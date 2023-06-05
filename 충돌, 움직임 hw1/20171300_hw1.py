import pygame
import random
import math
import os

class Ball:
    def __init__(self,ii, px, py, r, m, vx, vy, col):
        self.posX = px+r  #사진의 중심
        self.posY = py+r
        self.velX = vx
        self.velY = vy
        self.colour = col
        self.rad = r
        self.mass = m
        self.im=ii
        #self.sound=s
#        print(vx,vy)
    def setPos(self):
        self.posX = toInt(self.posX + self.velX)
        self.posY = toInt(self.posY + self.velY)

    def draw(self):
        screen.blit(self.im, [self.posX-self.rad, self.posY-self.rad])  #그릴때는 왼쪽위 꼭짓점.
        #screen.blit(self.im, [self.posX, self.posX])
    def wallColl(self):     # Checks and handles wall collisions
        if self.posX - self.rad <= 0:
            sound.play()
            self.posX = self.rad + 1
            self.velX = - self.velX/5*4
        elif self.posX + self.rad >= screenWidth:
            sound.play()
            self.posX = screenWidth - self.rad - 1
            self.velX = - self.velX/5*4 
        if self.posY - self.rad <= 0:
            sound.play()   
            self.posY = self.rad + 1
            self.velY = - self.velY/5*4
        elif self.posY + self.rad >= screenHeight:
            sound.play()
            self.posY = screenHeight - self.rad - 1
            self.velY = - self.velY/5*4


def collision(ball1, ball2):        # Handles ball-ball collisions
    dist = math.sqrt(distanceSq(ball1, ball2))
    overlap = ball1.rad + ball2.rad - dist
    dx = abs(ball1.posX - ball2.posX)
    dy = abs(ball1.posY - ball2.posY)
    if(dist==0):
        dist=0.1
    overx = 0.5 * overlap * dx / dist
    overy = 0.5 * overlap * dy / dist
    if ball1.posX - ball2.posX < 0:
        ball1.posX -= toInt(overx)
        ball2.posX += toInt(overx)
    else:
        ball1.posX += toInt(overx)
        ball2.posX -= toInt(overx)
    if ball1.posY - ball2.posY > 0:
        ball1.posY += toInt(overy)
        ball2.posY -= toInt(overy)
    else:
        ball1.posY -= toInt(overy)
        ball2.posY += toInt(overy)
    dsq = distanceSq(ball1, ball2)
    f1 = ((ball1.velX - ball2.velX)*(ball1.posX - ball2.posX) + (ball1.velY - ball2.velY)*(ball1.posY - ball2.posY)) / dsq
    ball1.velX -= (2 * ball2.mass / (ball1.mass + ball2.mass)) * f1 * (ball1.posX - ball2.posX)
    ball1.velY -= (2 * ball2.mass / (ball1.mass + ball2.mass)) * f1 * (ball1.posY - ball2.posY)
    ball2.velX -= (2 * ball1.mass / (ball1.mass + ball2.mass)) * f1 * (ball2.posX - ball1.posX)
    ball2.velY -= (2 * ball1.mass / (ball1.mass + ball2.mass)) * f1 * (ball2.posY - ball1.posY)

def distanceSq(ballX, ballY):
    dx = ballX.posX - ballY.posX
    dy = ballX.posY - ballY.posY
    return dx ** 2 + dy ** 2

def toInt(x):
    if x - int(x) < 0.5:
        return int(x)
    else:
        return int(x+1)

pygame.init()
fps = pygame.time.Clock()
screenWidth = 1000
screenHeight = 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
COL1 = (128, 128, 128)
COL2 = (120, 15, 65)
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'abe')
sound = pygame.mixer.Sound(os.path.join(assets_path, 'sound.wav'))
#image = pygame.image.load(os.path.join(assets_path, 'keyboard.png'))
ballList = []
for i in range(101): 
    if(i<7):

        image = pygame.image.load(os.path.join(assets_path, 'a.png'))
    elif(i<14):
        image = pygame.image.load(os.path.join(assets_path, 'b.png'))
    elif(i<21):
        image = pygame.image.load(os.path.join(assets_path, 'c.png'))
    elif(i<28):
        image = pygame.image.load(os.path.join(assets_path, 'd.png'))
    elif(i<35):
        image = pygame.image.load(os.path.join(assets_path, 'e.png'))
    elif(i<42):
        image = pygame.image.load(os.path.join(assets_path, 'f.png'))
    elif(i<49):
        image = pygame.image.load(os.path.join(assets_path, 'g.png'))
    elif(i<56):
        image = pygame.image.load(os.path.join(assets_path, 'h.png'))
    elif(i<63):
        image = pygame.image.load(os.path.join(assets_path, 'i.png'))
    elif(i<70):
        image = pygame.image.load(os.path.join(assets_path, 'j.png'))
    elif(i<77):
        image = pygame.image.load(os.path.join(assets_path, 'k.png'))
    elif(i<84):
        image = pygame.image.load(os.path.join(assets_path, 'l.png'))
    elif(i<91):
        image = pygame.image.load(os.path.join(assets_path, 'm.png'))
    else:
        image = pygame.image.load(os.path.join(assets_path, 'n.png'))
    if(image.get_width()==20):
        r=10
        m=2
    elif(image.get_width()==30):
        r=15
        m=4
    elif(image.get_width()==40):
        r=20
        m=7
## x, y, 반지름, 질량, 속도x, 속도y, col
    ball=Ball(image,random.randint(70,800), random.randint(70,800), r, m, random.randint(1, 10), random.randint(1,10), WHITE)
    ballList.append(ball)
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Collision')
keyboard_x = int(screenWidth / 2)
keyboard_y = int(screenHeight / 2)
keyboard_dx = 0
keyboard_dy = 0
keyboard_image = pygame.image.load(os.path.join(assets_path, 'keyboard.png'))
def main():
    screen.fill(BLACK)
    for ball in ballList:
        ball.draw()
        ball.wallColl()
        for ball2 in ballList:
            if ball != ball2 and distanceSq(ball, ball2) <= (ball.rad + ball2.rad) ** 2:
                collision(ball, ball2)
        ball.setPos()
    screen.blit(keyboard_image, [keyboard_x, keyboard_y])
    pygame.display.flip()

while True:
    main()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                keyboard_dx = -3
            elif event.key == pygame.K_RIGHT:
                keyboard_dx = 3
            elif event.key == pygame.K_UP:
                keyboard_dy = -3
            elif event.key == pygame.K_DOWN:
                keyboard_dy = 3
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                keyboard_dx = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                keyboard_dy = 0                
    keyboard_x += keyboard_dx
    keyboard_y += keyboard_dy

    fps.tick(60)

pygame.quit()
