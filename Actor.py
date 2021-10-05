from pygame.sprite import Group
from Food import Food
from Engine import Object, ToolCollection
from pygame import Surface, K_d, K_a, K_s, K_w, K_LSHIFT, Vector2, draw

from StatusBar import StatusBar


class Direction:
    NONE = 0
    RIGHT = 1
    LEFT = 2
    DOWN = 3
    UP = 4


def create_head(size: int, color: tuple[int]):
    image = Surface((size, size))
    image.fill(color)
    return image


def get_color(piece_count: int):
    SNAKE_1 = (123, 216, 10)
    SNAKE_2 = (101, 176, 11)

    if piece_count & 1 == 0:
        return SNAKE_2
    return SNAKE_1


def create_body(size: int, color: tuple[int]):
    image = Surface((size, size))
    image.fill(color)
    return image


class Body(Object):
    def __init__(self, grid_size: int, color: tuple[int]):
        Object.__init__(self, create_body(grid_size, color))
        self.grid_size = grid_size
        self.move(Vector2(-100, -100))


class Actor(Object):

    def update(self, Tools: ToolCollection):

        resolution = Tools.Canvas.rect.size

        if Tools.Input.is_pressed(K_a):
            self.direction = Direction.LEFT

        elif Tools.Input.is_pressed(K_d):
            self.direction = Direction.RIGHT

        if Tools.Input.is_pressed(K_s):
            self.direction = Direction.DOWN

        elif Tools.Input.is_pressed(K_w):
            self.direction = Direction.UP

        movement = Vector2()
        mouth = None

        if self.direction == Direction.LEFT:
            movement.x = -1
            mouth = Vector2(*self.pos)
            mouth.x -= self.grid_size // 2

        elif self.direction == Direction.RIGHT:
            movement.x = 1
            mouth = Vector2(*self.pos)
            mouth.x += self.grid_size // 2

        if self.direction == Direction.UP:
            movement.y = -1
            mouth = Vector2(*self.pos)
            mouth.y -= self.grid_size // 2

        elif self.direction == Direction.DOWN:
            movement.y = 1
            mouth = Vector2(*self.pos)
            mouth.y += self.grid_size // 2

        if self.pos.x > resolution[0]:
            self.pos.x = 0

        elif self.pos.x < 0:
            self.pos.x = resolution[0]

        if self.pos.y > resolution[1]:
            self.pos.y = 0

        elif self.pos.y < 0:
            self.pos.y = resolution[1]

        if self.rect.colliderect(self.food):
            self.food.repositionate()
            for _ in range(10):
                self.grow(Tools)
            self.score += 1
            self.status_bar.display()

        for piece in self.body[self.min_index:]:
            if mouth and piece.rect.collidepoint(mouth) and self.moved:
                self.game_over(Tools)

        for i in range(len(self.body) - 1, 0, -1):
            piece: Body = self.body[i]
            back: Body = self.body[i - 1]
            piece.abs_move(Vector2(*back.pos))

        if movement.length() > 0:
            self.move(movement.normalize() *
                      self.speed * Tools.Time.delta_time)
            self.moved = True

    def grow(self, Tools: ToolCollection):

        piece = Body(self.grid_size, get_color(len(self.body)))
        self.body.append(piece)

        Tools.Game.add(piece, 'snake-body')

    def start(self, Tools: ToolCollection):
        for _ in range(self.start_size):
            self.grow(Tools)

        self.status_bar = Tools.Game.get_object_by_type(StatusBar)[0]
        self.food = Tools.Game.get_object_by_type(Food)[0]

    def game_over(self, Tools: ToolCollection):
        for piece in self.body:
            piece.kill()
        self.kill()

        # TODO: Game over screen
        Tools.Game.running = False

    def __init__(self, grid_size: int):
        Object.__init__(self, create_head(grid_size, get_color(0)))
        self.speed = 250
        self.direction = Direction.NONE
        self.grid_size = grid_size
        self.start_size = 10
        self.body: Object = [self]
        self.min_index = min(self.start_size, 4)
        self.moved = False
        self.score = 0
