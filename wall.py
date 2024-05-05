import pygame

from constants import GRID_SIZE, BLACK
from game_object import GameObject
from vec import Vec


# Class Wall
class Wall(GameObject):
    def __init__(self, size=1):
        self.size = size
        self.colliders = []  # list of Vec
        super().__init__(color=BLACK)

    def create(self):
        super().create()
        for i in range(self.size):
            for j in range(self.size):
                self.colliders.append(
                    Vec(self.position.x + i * GRID_SIZE, self.position.y + j * GRID_SIZE)
                )

    def draw(self, screen):
        rect = pygame.Rect((self.position.x, self.position.y), (self.size * GRID_SIZE, self.size * GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)
