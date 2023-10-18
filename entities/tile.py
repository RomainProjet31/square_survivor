from entities.entity import Entity
from constants.sprite_constants import TILE_SIZE
from constants.color_constants import FLOOR, WALL


class Tile(Entity):
    def __init__(self, current_map, collides, x, y):
        super().__init__(current_map, TILE_SIZE, 0, x, y, collides, WALL if collides else FLOOR)
