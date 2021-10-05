from Food import Food
from Engine.Object.Object import Object
from pygame import draw
from Engine.Draw import Line, Rectangle
import Engine
import pygame

from pygame.math import Vector2

from Actor import Actor
from PerformanceInfo import PerformanceInfo
from StatusBar import StatusBar


class Colors:
    LINE = (10, 10, 10)
    APPLE = (255, 0, 0)


class Config:
    resolution = (800, 600)
    grid_size = 20


def create_grid(resolution: tuple[int], grid_size: int):
    surface: pygame.Surface = pygame.Surface(resolution)

    for row in range(0, resolution[1] // grid_size):
        start = (0, row * grid_size)
        end = (resolution[0], row * grid_size)
        draw.line(surface, Colors.LINE, start, end, 1)

    for column in range(0, resolution[0] // grid_size):
        start = (column * grid_size, 0)
        end = (column * grid_size, resolution[1])
        draw.line(surface, Colors.LINE, start, end, 1)

    return Object(surface)


def main():
    game = Engine.Game("Snake 🐍", Config.resolution)
    game.load_font('Arial', [18, 32])
    game.create_group('snake-body')

    center = Vector2(*game.Canvas.rect.center)

    center.x = (center.x // Config.grid_size) * Config.grid_size
    center.y = (center.y // Config.grid_size) * Config.grid_size

    player = Actor(Config.grid_size)
    player.move(Vector2(
        center.x + Config.grid_size // 2,
        center.y + Config.grid_size // 2
    ))

    grid = create_grid(Config.resolution, Config.grid_size)
    grid.move(center)

    apple = Food(Config.grid_size, Colors.APPLE)
    status_bar = StatusBar(player)
    performance_info = PerformanceInfo()

    game.add(grid)
    game.add(apple)
    game.add(player)
    game.add(status_bar)
    game.add(performance_info)

    game.start()


if __name__ == '__main__':
    main()
