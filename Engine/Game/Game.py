from Engine.Object.Object import Object
from Engine.defs import ToolCollection
from Engine.Events.Events import Events
from Engine.Input.Input import Input
from Engine.Time.Time import Time
from Engine.Canvas.Canvas import Canvas
from threading import Event, Thread

from pygame.sprite import RenderUpdates as Group, collide_rect
from pygame import QUIT
from pygame.display import set_caption

import pygame
from pygame import font


class Game:

    def get_object_by_type(self, t):
        result = []
        for sprite in self.Groups['__all__'].sprites():
            if isinstance(sprite, t):
                result.append(sprite)
        return result

    def add(self, object: Object, group_name: str = ''):
        self.Groups['__all__'].add(object)

        if object.has_sprite:
            self.Groups['__draw__'].add(object)

        if group_name and group_name in self.Groups:
            self.Groups[group_name].add(object)

    def create_group(self, group_name: str):
        self.Groups[group_name] = Group()

    def start(self):
        Thread(target=self.Canvas.run, daemon=True).start()
        Thread(target=self.Events.run, daemon=True).start()
        Thread(target=self.Input.run, daemon=True).start()

        for group_name in self.Groups:
            for sprite in self.Groups[group_name].sprites():
                sprite.start(self.ToolCollection)

        self.run()

    def update(self):
        for group_name in self.Groups:
            self.Groups[group_name].update(self.ToolCollection)

    def run(self):
        try:
            self.Events.on(QUIT, self.stop)
            self.loop()
        except Exception as e:
            print(f'Error in game: {e}')

    def stop(self, event: Event):
        self.running = False

    def loop(self):
        self.running = True
        while self.running:
            self.Time.tick(64)
            pygame.event.pump()
            self.update()

    def load_font(self, name: str, sizes: list[int]):
        if not name in self.Fonts:
            self.Fonts[name] = {}

        for size in sizes:
            self.Fonts[name][size] = font.SysFont(name, size)

    def __init__(self, title: str, resolution: tuple[int] = (0, 0)):

        pygame.init()

        set_caption(title)

        self.Groups = {
            '__all__': Group(),
            '__draw__': Group(),
        }
        draw_group = self.Groups['__draw__']

        self.running = False

        self.Fonts = {}
        self.Canvas = Canvas(draw_group, resolution)
        self.Time = Time()
        self.Events = Events()
        self.Input = Input(self.Events)

        self.ToolCollection = ToolCollection(
            self,
            self.Canvas,
            self.Input,
            self.Events,
            self.Time
        )
