import pygame
import os
import sys
from time import sleep
from constants import *
from feed import Feed
from game_object import GameObject
from snake import Snake
from wall import Wall


# Game class
class Game(object):
    def __init__(self):
        self.time = 0
        self.level = 1
        self.snake = Snake()
        self.feed = Feed()
        self.speed = 20
        self.walls = []
        self.create_random_wall()

    # Game event handling and control
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.control(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.control(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.control(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.control(RIGHT)
        return False

    # Perform game logic
    def run_logic(self):
        if not self.snake.move():
            self.gameover()

        self.check_eat(self.snake, self.feed)
        if self.time % 2 == 0:
            self.feed.new_flee(snake=self.snake, walls=self.walls)

        for wall in self.walls:
            if self.check_collide(self.snake, wall):
                # Game Over
                self.gameover()
                break
        self.speed = (20 + self.snake.length) / 4

        # 4개를 먹을 때마다 벽을 하나 생성
        if self.level < int(self.snake.length / 4) + 1:
            self.level += 1
            self.walls.append(Wall(size=self.level))

        self.time += 1

    def check_collide(self, snake: Snake, gameObject: GameObject):
        for collider in gameObject.colliders:
            if snake.positions[0] == collider:
                return True

    # Check if the snake has eaten the food
    def check_eat(self, snake: Snake, feed: Feed):
        if snake.positions[0] == feed.position:
            snake.eat()
            feed.create()

    def create_random_wall(self):
        import random
        for i in range(10):
            self.walls.append(Wall(size=random.randint(1, 5)))

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # Display game information
    def draw_info(self, level, length, speed, screen):
        info = "Level: {}    Length: {}    Speed: {}".format(level, length, round(speed, 2))
        font_path = resource_path("assets/NanumGothicCoding-Bold.ttf")
        font = pygame.font.Font(font_path, 26)
        text_obj = font.render(info, 1, GRAY)
        text_rect = text_obj.get_rect()
        text_rect.x, text_rect.y = 10, 10
        screen.blit(text_obj, text_rect)

    # Handle game frames
    def display_frame(self, screen):
        screen.fill(WHITE)
        self.draw_info(self.level, self.snake.length, self.speed, screen)
        self.snake.draw(screen)
        self.feed.draw(screen)
        for wall in self.walls:
            wall.draw(screen)
        screen.blit(screen, (0, 0))

    def gameover(self):
        sleep(1)
        print('snake length: ' + str(self.snake.length))
        self.time = 0
        self.level = 1
        self.walls = []
        self.create_random_wall()
        self.snake.create()


# Set resource path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    # Game initialization and environment setup
    pygame.init()
    pygame.display.set_caption('Snake Game')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    done = False
    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        pygame.display.flip()
        clock.tick(game.speed)

    pygame.quit()


if __name__ == '__main__':
    main()
