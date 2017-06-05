import pymunk
import pygame
import time
import random
import hsluv

class ShadowSpace(object):
    """Wrapper for the shadow simulation in pymunk and pygame"""
    def __init__(self):
        self.width = 960
        self.height = 640
        pygame.init()
        pygame.display.init()
        self.surface = pygame.display.set_mode((self.width,self.height))
        #self.surface = pygame.Surface((720, 640))
        self.surface.fill((255, 255, 255))
        self.space = pymunk.Space()
        self.space.gravity = 0, -800
        #self.testball = Ball(10, 50)
        #self.testball.add(self.space)
        self.balls = self.init_balls(30)

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
            ball = Ball(10, i*self.width/float(n), 0, (int(red*255), int(green*255), int(blue*255)))
            ball.add(self.space)
            ball_list.append(ball)
        return ball_list

    def update(self):
        self.surface.fill((255, 255, 255))
        self.space.step(.02)
        for ball in self.balls:
            ball.draw(self.surface)
        pygame.display.update()


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
        self.body.position = self.x, self.y

    def add(self, space):
        space.add(self.body, self.shape)
    def draw(self, surface):
        self.x, self.y = self.body.position
        #print self.y
        pygame.draw.circle(surface, self.color, (int(self.x), abs(int(self.y))), self.radius)

if __name__ == '__main__':
    testSpace = ShadowSpace()
    while True:
        #testSpace.drawCircle()

        #pygame.display.update()
        testSpace.update()
        time.sleep(.01)
