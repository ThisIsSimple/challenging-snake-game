import random
import pygame
from constants import *
from vec import Vec


# Snake Object
class Snake(object):
    def __init__(self):
        self.create()

    # Snake create
    def create(self):
        self.length = 2
        self.positions = [Vec(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    # Control snake direction
    def control(self, xy):
        if (xy[0] * -1, xy[1] * -1) == self.direction:
            return
        else:
            self.direction = xy

    # Snake movement
    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = Vec(cur.x + (x * GRID_SIZE), cur.y + (y * GRID_SIZE))

        # If the snake touches its own body, the snake is recreated from the beginning
        if new in self.positions[2:]:
            return False
        # If the snake goes beyond the game screen, the snake is recreated from the beginning
        elif new.x < 0 or new.x >= SCREEN_WIDTH or \
                new.y < 0 or new.y >= SCREEN_HEIGHT:
            return False
        # If the snake moves normally
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    # When the snake eats the food
    def eat(self):
        self.length += 1

    # Draw snake
    def draw(self, screen):
        red, green, blue = 50 / (self.length - 1), 150, 150 / (self.length - 1)
        for i, p in enumerate(self.positions):
            color = (100 + red * i, green, blue * i)
            rect = pygame.Rect((p.x, p.y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, color, rect)
