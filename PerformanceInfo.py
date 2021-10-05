from hashlib import new
from Engine import Object, ToolCollection
from pygame import Rect, Surface, Vector2, draw
from random import randint


class Colors:
    TEXT = (255, 255, 255)


buffer = {}


def create_sprite(size: tuple[int]):
    return Surface(size)


class PerformanceInfo(Object):

    def update(self, Tools: ToolCollection):

        fps = int(Tools.Canvas.Time.fps)
        fps_string = f'{fps}'

        text = Tools.Game.Fonts['Arial'][18].render(
            fps_string, True, Colors.TEXT)

        rect: Rect = text.get_rect()

        self.image = create_sprite(rect.size)
        self.image.blit(text, (0, 0))

    def display(self):
        self.displayed_for = 0

    def start(self, Tools: ToolCollection):
        self.resolution = Tools.Canvas.rect.size

    def __init__(self):
        Object.__init__(self, create_sprite((0, 0)))
