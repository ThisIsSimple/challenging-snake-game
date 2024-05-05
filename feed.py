from typing import List

from constants import ORANGE, GRID_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from game_object import GameObject
from snake import Snake
import math

from vec import Vec
from wall import Wall


# Class Feed
class Feed(GameObject):
    def __init__(self):
        super().__init__(color=ORANGE)

    def new_flee(self, snake: Snake, walls: List[Wall]):
        direction_vectors = [Vec(-1, 0), Vec(0, -1), Vec(1, 0), Vec(0, 1)]

        max_distance = 0
        new_direction = Vec(0, 0)
        for direction in direction_vectors:
            new = Vec(
                self.position.x + direction.x * GRID_SIZE,
                self.position.y + direction.y * GRID_SIZE,
            )
            print(new)

            if new.x < 0 or new.x >= SCREEN_WIDTH or new.y < 0 or new.y >= SCREEN_HEIGHT:
                continue

            is_collide = False
            for wall in walls:
                for collider in wall.colliders:
                    if new == collider:
                        is_collide = True
                        break
            if is_collide:
                continue

            distance = new.distance(snake.positions[0])
            if distance > max_distance:
                max_distance = distance
                new_direction = direction
        self.position = Vec(self.position.x + new_direction.x * GRID_SIZE, self.position.y + new_direction.y * GRID_SIZE)


    def flee(self, snake: Snake, walls: List[Wall]):
        sub = (self.position - snake.positions[0])
        distance = math.sqrt(sub.x ** 2 + sub.y ** 2)
        if distance == 0:
            return

        direction_vectors = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        # check out of screen
        if self.position.x < GRID_SIZE:
            direction_vectors.remove((-1, 0))
        if self.position.x >= SCREEN_WIDTH - GRID_SIZE:
            direction_vectors.remove((1, 0))
        if self.position.y < GRID_SIZE:
            direction_vectors.remove((0, -1))
        if self.position.y >= SCREEN_HEIGHT - GRID_SIZE:
            direction_vectors.remove((0, 1))

        # avoid walls
        index_to_remove = []
        for index, vector in enumerate(direction_vectors):
            new = Vec(self.position.x + vector[0] * GRID_SIZE, self.position.y + vector[1] * GRID_SIZE)
            for wall in walls:
                for collider in wall.colliders:
                    if collider == new:
                        index_to_remove.append(index)
        for index in index_to_remove:
            direction_vectors.pop(index)

        direction = (sub.x / distance, sub.y / distance)
        min_distance = 100
        min_index = -1
        for index, vector in enumerate(direction_vectors):
            distance = (vector[0] - direction[0]) ** 2 + (vector[1] - direction[1]) ** 2
            if distance < min_distance:
                min_distance = distance
                min_index = index

        final_direction = direction_vectors[min_index]

        new = Vec(self.position.x + final_direction[0] * GRID_SIZE, self.position.y + final_direction[1] * GRID_SIZE)
        self.position = new
