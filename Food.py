from Engine import Object, ToolCollection
from pygame import Surface, Vector2
from random import randint


def create_sprite(size: int, color: tuple[int]):
    image = Surface((size, size))
    image.fill(color)
    return image

class Food(Object):

    def repositionate(self):
        x = randint(0, self.resolution[0])
        y = randint(0, self.resolution[1])

        x += self.grid_size // 2
        y += self.grid_size // 2

        self.pos = Vector2(x, y)
        self.move(Vector2())

    def start(self, Tools: ToolCollection):
        self.resolution = Tools.Canvas.rect.size
        self.repositionate()

    def __init__(self, grid_size: int, color: tuple[int]):
        Object.__init__(self, create_sprite(grid_size, color))
        self.speed = 100
        self.grid_size = grid_size
