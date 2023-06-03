import pygame as pg
import pymunk as pm
from math import degrees, radians, sin, cos


class Player:
    def __init__(self, screen, space, pos, imageName, imageSize, additionalAngle, keys, color):
        self.screen = screen
        self.space = space
        self.body = pm.Body(body_type=pm.Body.DYNAMIC)
        self.body.position = pos
        self.shape = pm.Circle(self.body, 30)
        self.shape.friction = 1
        self.shape.elasticity = 0
        self.shape.density = 1
        self.image = pg.transform.scale(pg.image.load(imageName), imageSize)
        self.color = color
        self.upKey, self.downKey, self.leftKey, self.rightKey = keys
        self.forward_dist = 4
        self.additionalAngle = additionalAngle
        space.add(self.body, self.shape)

    def draw(self):
        angle = self.body.angle
        # rot_image = self.image
        rot_image = pg.transform.rotate(self.image, degrees(angle + radians(self.additionalAngle)))
        size = rot_image.get_size()
        pos = self.body.position
        imagePos = [pos[0] - size[0] // 2, pos[1] - size[1] // 2]
        self.screen.blit(rot_image, imagePos)

    def process(self, pressed_keys):
        if pressed_keys[self.upKey] or pressed_keys[self.downKey] or pressed_keys[self.leftKey] or pressed_keys[
            self.rightKey]:
            self.additionalAngle = -90
            if pressed_keys[self.upKey] and pressed_keys[self.rightKey]:
                self.body.angle = radians(45)
            elif pressed_keys[self.upKey] and pressed_keys[self.leftKey]:
                self.body.angle = radians(135)
            elif pressed_keys[self.leftKey] and pressed_keys[self.downKey]:
                self.body.angle = radians(225)
            elif pressed_keys[self.downKey] and pressed_keys[self.rightKey]:
                self.body.angle = radians(315)
            elif pressed_keys[self.upKey]:
                self.body.angle = radians(90)
            elif pressed_keys[self.downKey]:
                self.body.angle = radians(270)
            elif pressed_keys[self.leftKey]:
                self.body.angle = radians(180)
            elif pressed_keys[self.rightKey]:
                self.body.angle = radians(0)
            self.forward()

    def forward(self):
        angle = self.body.angle
        dx = self.forward_dist * cos(angle)
        dy = self.forward_dist * sin(angle)
        pos = self.body.position
        new_pos = [pos[0] + dx, pos[1] - dy]
        self.body.position = new_pos
