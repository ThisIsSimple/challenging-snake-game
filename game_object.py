import pygame
from constants import ORANGE, GRID_WIDTH, GRID_HEIGHT, GRID_SIZE
from vec import Vec


# Class GameObject
class GameObject(object):
    def __init__(self, position=Vec(0, 0), color=ORANGE):
        self.position: Vec = position
        self.color = color
        self.create()

    def create(self):
        import random
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        self.position = Vec(x * GRID_SIZE, y * GRID_SIZE)

    def move(self, position: Vec):
        self.position = position

    def draw(self, screen):
        rect = pygame.Rect((self.position.x, self.position.y), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)
