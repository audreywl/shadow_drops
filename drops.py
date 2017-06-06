import pymunk
import pygame
import time
import random
from random import randint
import hsluv
import contouring
import cv2
import numpy as np

class ShadowSpace(object):
    """Wrapper for the shadow simulation in pymunk and pygame"""
    def __init__(self, windowed=False):
        pygame.init()
        pygame.display.init()
        if windowed:
            self.width = 640
            self.height = 480
            self.surface = pygame.display.set_mode((self.width, self.height))
        else:
            self.surface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            self.width = self.surface.get_width()
            self.height = self.surface.get_height()
        self.surface.fill((255, 255, 255))
        self.space = pymunk.Space()
        self.space.gravity = 0, -800
        self.balls = self.init_balls(10)

        self.ground = Ground(self.width/2, 450,10, self.width)
        l1 = self.ground.create_Ground()
        self.space.add(l1)
        self.contours = contouring.Contour(self.space, 0)
        cv2.namedWindow('img')


    def init_balls(self, n):
        color_list = []
        starting_hue = random.randint(0, 360)
        lightness = 65
        saturation = 65
        for j in range(n):
            hue = (starting_hue+j*100/float(n))%360
            color_list.append(([hue, saturation, lightness]))
        random.shuffle(color_list)
        ball_list = []
        for i in range(n):
            red, green, blue = hsluv.hsluv_to_rgb(color_list[i])
            ball = Ball(10, i*self.width/float(n), 0, (int(red*255), int(green*255), int(blue*255)), 10)
            ball.add(self.space)
            ball_list.append(ball)

        hugeball = Ball(50, 100, -400, (int(red*255), int(green*255), int(blue*255)), 10)
        hugeball.add(self.space)
        ball_list.append(hugeball)
        return ball_list


    def update(self):
        self.surface.fill((255, 255, 255))
        self.contours.update_contours()
        self.space.step(.02)
        balls_exist = len(self.balls)
        i = 0
        while balls_exist:
            if abs(self.balls[i].y) > self.height:
                del self.balls[i]
            else:
                self.balls[i].draw(self.surface)
            if randint(0,1000) == 3:
                self.random_ball()
            i += 1
            if i >= len(self.balls):
                balls_exist = False
        #print self.contours.img
        cv2.imshow('img', self.contours.img)
        cv2.imshow('contours_img', self.contours.contours_img)
        #cv2.waitKey()

        #pygame.display.update()

    def random_ball(self):
        color_list = []
        ball_list = self.balls
        starting_hue = random.randint(0, 360)
        lightness = 65
        saturation = 65
        for j in range(30):
            hue = (starting_hue+j*100/float(30))%360
            color_list.append(([hue, saturation, lightness]))
        random.shuffle(color_list)
        red, green, blue = hsluv.hsluv_to_rgb(color_list[randint(0,29)])
        ball = Ball(10, randint(0,30)*self.width/float(randint(1,30)), 0, (int(red*255), int(green*255), int(blue*255)), 10)
        ball.add(self.space)
        ball_list.append(ball)
        self.balls = ball_list


    #def check_collision()

class Ground(object):

    def __init__(self, x=0, y=0, mass=0, width=0):
        self.x = 0
        self.y = y-10
        self.mass = mass
        self.width = width
        self.color = (150,200,50)
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.body.elasticity = 0.999
        self.body.position = (self.x,-self.y)

    def create_Ground(self):
        print(-self.y)
        l1 = pymunk.Segment(self.body, (self.x, -self.y), (self.width, -self.y), 10)
        return(l1)

    def draw(self, surface):
        #print self.y
        pygame.draw.rect(surface, self.color, (int(self.x), abs(int(self.y)), self.width, 10),0)

class Ball(object):
    """it's a ball. it's got image and physics attributes"""
    def __init__(self, radius=10, x=0, y=0, color=(0,0,0), mass=1):
        self.radius = radius
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(self.mass, self.moment)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.999
        self.body.position = self.x, self.y

    def add(self, space):
        space.add(self.body, self.shape)

    def draw(self, surface):
        self.x, self.y = self.body.position

        pygame.draw.circle(surface, self.color, (int(self.x), abs(int(self.y))), self.radius)

if __name__ == '__main__':
    testSpace = ShadowSpace(True)
    running = True
    while  running:
        #pygame.display.update()
        testSpace.update()
        time.sleep(.03)
        cv2.waitKey(30)
        current_event = pygame.event.poll()
        #print current_event
        print 'running'
        if current_event.type == pygame.QUIT:
            running = False
            testSpace.kill_video()
        elif current_event.type == pygame.KEYDOWN and current_event.key == pygame.K_ESCAPE:
            running = False
            testSpace.kill_video()
            print 'QUIT!'
            #testSpace.drawCircle()
