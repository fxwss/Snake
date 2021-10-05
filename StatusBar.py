from hashlib import new
from Engine import Object, ToolCollection
from pygame import Rect, Surface, Vector2, draw
from random import randint


class Colors:
    TEXT = (255, 255, 255)


buffer = {}


def create_sprite(size: tuple[int]):
    return Surface(size)


class StatusBar(Object):

    def update(self, Tools: ToolCollection):

        if self.displayed_for <= self.display_time:

            score_string = f'{self.ref.score}'

            text = Tools.Game.Fonts['Arial'][32].render(
                score_string, True, Colors.TEXT)

            rect: Rect = text.get_rect()

            self.image = create_sprite(rect.size)
            self.image.blit(text, (0, 0))

            new_position = Vector2(
                self.ref.pos.x - rect.w // 2,
                self.ref.pos.y - rect.h * 2
            )

            opacity = (-(self.displayed_for / self.display_time) * 255) + 255

            self.image.set_alpha(opacity)
            self.abs_move(new_position)
            self.displayed_for += Tools.Time.delta_time

    def display(self):
        self.displayed_for = 0

    def start(self, Tools: ToolCollection):
        self.resolution = Tools.Canvas.rect.size

    def __init__(self, head: Object):
        self.ref = head
        self.display_time = 2
        self.displayed_for = self.display_time
        Object.__init__(self, create_sprite((0, 0)))
