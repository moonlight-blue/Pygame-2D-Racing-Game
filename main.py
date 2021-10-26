import pygame
import time
import math
from utils import scale_image, blit_rotate_center

GRASS=scale_image(pygame.image.load("imgs/grass.jpg"),2)

TRACK=scale_image(pygame.image.load("imgs/track.png"),0.65)
TRACK_BORDER=scale_image(pygame.image.load("imgs/track-border.png"),0.65)
TRACK_BORDER_MASK=pygame.mask.from_surface(TRACK_BORDER)

RED_CAR=scale_image(pygame.image.load("imgs/red-car.png"),0.45)
GREEN_CAR=scale_image(pygame.image.load("imgs/green-car.png"),0.45)

FINISH=scale_image(pygame.image.load("imgs/finish.png"),0.6)
FINISH_POSITION=(100,220)
FINISH_MASK=pygame.mask.from_surface(FINISH)

def draw(win,imgs,player_car):
    for img, pos in imgs:
        win.blit(img,pos)
    player_car.draw(win)
    pygame.display.update()

WIDTH, HEIGHT=TRACK.get_width(), TRACK.get_height()
WIN=pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Racing")

class AbstractCar:

    def __init__(self, max_vel, rotation_vel):
        self.img=self.IMG
        self.max_vel=max_vel
        self.vel=0
        self.rotation_vel=rotation_vel
        self.angle=0
        self.x,self.y=self.START_POS
        self.acceleration=0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x,self.y), self.angle)

    def move_forward(self):
        self.vel=min(self.max_vel, self.vel+self.acceleration)
        self.move()
    
    def move_backward(self):
        self.vel=max(-self.max_vel/2, self.vel-self.acceleration)
        self.move()

    def move(self):
        radians=math.radians(self.angle)
        vertical=math.cos(radians)*self.vel
        horizontal=math.sin(radians)*self.vel

        self.y-=vertical
        self.x-=horizontal

    def collide(self, mask, x=0,y=0):
        car_mask=pygame.mask.from_surface(self.img)
        offset=(int(self.x-x),int(self.y-y))
        poi=mask.overlap(car_mask,offset)
        return poi

    

class PlayerCar(AbstractCar):
    IMG=RED_CAR
    START_POS=(105,180)

    def reduce_vel(self):
        self.vel=max(self.vel-self.acceleration/2, 0)
        self.move()

    def bounce(self):
        self.vel=-self.vel/3
        self.move()
    
    def reset(self):
        self.x,self.y=self.START_POS
        self.angle=0
        self.vel=0

def moved(player_car):
    keys=pygame.key.get_pressed()
    moved=False
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved=True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved=True
        player_car.move_backward()
    if not moved:
        player_car.reduce_vel()

imgs=((GRASS,(0,0)),(TRACK,(0,0)), (FINISH,FINISH_POSITION),(TRACK_BORDER,(0,0)))
player_car=PlayerCar(4,4)
FPS=70
run=True

clock=pygame.time.Clock()

while run:

    clock.tick(FPS)
    draw(WIN, imgs, player_car)    
    

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            break
    moved(player_car)
    if player_car.collide(TRACK_BORDER_MASK)!=None:
        player_car.bounce()
    
    finish_poi=player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if finish_poi!=None and finish_poi[1]==0:
        player_car.bounce()
    elif finish_poi!=None:
        player_car.reset()


    
pygame.quit()
