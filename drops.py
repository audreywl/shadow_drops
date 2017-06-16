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
        #start the pygame window
        pygame.init()
        pygame.display.init()
        if windowed:
            self.width = 1500
            self.height = 900
            self.surface = pygame.display.set_mode((self.width, self.height))
        else:
            self.surface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            self.width = self.surface.get_width()
            self.height = self.surface.get_height()
        self.surface.fill((255, 255, 255))

        #make the pymunk space
        self.space = pymunk.Space()
        self.space.gravity = -400, -800

        #add balls to the space
        self.balls = self.init_balls(40)

        #option to add ground to the space
        #self.ground = Ground(self.width/2, 450,10, self.width)
        #self.ground.add(self.space)

        #create the contour-processing object
        self.contours = contouring.Contour(self.space, 0, self.height)

        #option to use openCV to debug
        #cv2.namedWindow('contours_img')


    def init_balls(self, n):
        """create the rain of balls at the beginning of the simulation"""
        ball_list = []
        self.color_list = pretty_colors(n)
        for i in range(n):
            ball = Ball(10, i*self.width/float(n), -30, self.color_list[i], 10)
            ball.add(self.space)
            ball_list.append(ball)

        #hugeball = Ball(50, 100, -400, color_list[0], 10)
        #hugeball.add(self.space)
        #ball_list.append(hugeball)
        return ball_list

    def update(self):
        """step forward the physics simulation and the pygame visualization"""
        #remove all previous pygame drawings
        self.surface.fill((255, 255, 255))
        #update what shadows are being seen
        tuple_contours = self.contours.update_contours()
        self.create_shadows(tuple_contours)
        #step the pymunk simulation forward
        self.space.step(.02)
        self.space.reindex_static()
        if randint(0,10) == 3:
            self.random_ball()
        #draw all the new ball positions, but remove them from the list when they fall offscreen
        balls_exist = len(self.balls)
        i = 0
        while balls_exist:
            if abs(self.balls[i].y) > self.height:
                del self.balls[i]
            else:
                self.balls[i].draw(self.surface)
            i += 1
            if i >= len(self.balls):
                balls_exist = False
        #print self.contours.img
        cv2.imshow('img', self.contours.debug_img)
        #cv2.imshow('contours_img', self.contours.contours_img)
        #cv2.waitKey(5000)
        pygame.display.update()
        print self.space.shapes

    def random_ball(self):
        """drop a randomly placed ball from the top of the simulation"""
        x = randint(0,30)*self.width/float(randint(1,30))
        ball = Ball(10, x, 0, random.choice(self.color_list), 10)
        ball.add(self.space)
        self.balls.append(ball)

    def create_shadows(self, contours):
        """use the countours to add an updated shadow shape to the simulation"""
        self.remove_shadows()
        #print len(contours)
        for cont in contours:
            body = pymunk.Body(0,0,pymunk.Body.STATIC)
            contour_shape = pymunk.Poly(body, cont)
            #print('vertices')
            #print(contour_shape.get_vertices())
            self.space.add(body, contour_shape)
            self.space.reindex_shape(contour_shape)
            self.space.reindex_shapes_for_body(body)


    def remove_shadows(self):
        """remove all shadows left from the previous step in simulation"""
        for body in self.space.bodies:
            if body.body_type == pymunk.Body.STATIC:
                self.space.remove(body)
                for shape in body.shapes: #pymunk can assign multiple shapes to a body. there shouldn't be multiple, but just in case
                    self.space.remove(shape)

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
        """put the ball in the simulation"""
        space.add(self.body, self.shape)

    def draw(self, surface):
        """make a pygame drawing of the ball"""
        self.x, self.y = self.body.position
        pygame.draw.circle(surface, self.color, (int(self.x), abs(int(self.y))), self.radius)

class Ground(object):
    """optional class for putting a ground in the simulation, not used in normal operation"""
    def __init__(self, x=0, y=0, mass=0, width=0):
        self.x = 0
        self.y = y-10
        self.mass = mass
        self.width = width
        self.color = (150,200,50)
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.body.elasticity = 0.999
        self.body.position = (self.x,-self.y)
        self.shape = pymunk.Segment(self.body, (self.x, -self.y), (self.width, -self.y), 10)

    def add(self, space):
        space.add(self.body, self.shape)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (int(self.x), abs(int(self.y)), self.width, 10),0)

def pretty_colors(n, lightness=65, saturation=65):
    """returns a list of random colors (rbg tuples) with length n that are all similar hues with the same lightness and saturation according to hsluv standard"""
    color_list = []
    starting_hue = random.randint(0, 360)
    for j in range(n):
        hue = (starting_hue+j*100/float(n))%360
        red, green, blue = hsluv.hsluv_to_rgb(([hue, saturation, lightness]))
        color_list.append((int(red*255), int(green*255), int(blue*255)))
    random.shuffle(color_list)
    return color_list

if __name__ == '__main__':
    testSpace = ShadowSpace(True)
    running = True
    while  running:
        testSpace.update()
        time.sleep(.03)
        cv2.waitKey(30)
        current_event = pygame.event.poll()
        if current_event.type == pygame.QUIT:
            running = False
            testSpace.contours.kill_video()
        elif current_event.type == pygame.KEYDOWN and current_event.key == pygame.K_ESCAPE:
            running = False
            testSpace.contours.kill_video()
            print 'QUIT!'
