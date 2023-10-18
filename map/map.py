import random

from constants.map_config_contant import CONFIGS
from constants.sprite_constants import TILE_SIZE
from entities.enemy import Enemy
from entities.player import Player
from entities.tile import Tile

PATH_MAP = "assets/maps/map_{0}.txt"

TILE_LAYER = 0
SPRITE_LAYER = 1


class Map:
    def __init__(self, game_manager, idx_map):
        self.idx_map = idx_map
        self.game_manager = game_manager
        self.player = None
        self.config = None
        self.enemies_spawn_left = 0
        self.enemies_spawn_tick = 0
        self.game_won = False
        self.entities = []
        """ the layers: 
                0 -> Tiles;
                1 -> Enemies and Player
                """

    def init_map(self):
        # will load the map using an external file
        matrix = self.__get_map()
        self.entities.append([])
        self.entities.append([])
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                type_tile = int(matrix[i][j])
                y = i * TILE_SIZE + 1
                x = j * TILE_SIZE + 1
                if type_tile == 2:
                    # Extracted because used for some computations
                    self.player = Player(self, x, y)
                    self.entities[SPRITE_LAYER].append(self.player)
                    collides = False
                else:
                    collides = type_tile == 1
                self.entities[TILE_LAYER].append(Tile(self, collides, x, y))

        self.config = CONFIGS[self.idx_map - 1]
        self.enemies_spawn_left = self.config.nb_enemies

        self.__handle_enemy_spawn()

    def __get_map(self):
        matrix = []
        with open(PATH_MAP.format(self.idx_map)) as file:
            for line in file:
                current_array = line.replace("\n", "").split(",")
                matrix.append(current_array)
        return matrix

    def update(self, dt):
        for arr in self.entities:
            for entity in arr:
                if entity.alive:
                    entity.update(dt)
                else:
                    arr.remove(entity)
        self.__update_enemy_spawn(dt)
        if len(self.entities[SPRITE_LAYER]) == 1 and self.player.alive:
            self.game_won = True

    def render(self):
        for arr in self.entities:
            for entity in arr:
                entity.render()

    def __update_enemy_spawn(self, dt):
        if self.enemies_spawn_tick > self.config.delay_enemy and self.enemies_spawn_left > 0:
            self.__handle_enemy_spawn()
        elif self.enemies_spawn_left > 0:
            self.enemies_spawn_tick += dt

    def __handle_enemy_spawn(self):
        for _ in range(self.config.nb_per_spawn):
            if self.enemies_spawn_left > 0:
                self.__add_enemy()
                self.enemies_spawn_left -= 1

    def __add_enemy(self):
        floors = self.__get_floors()
        idx_tile = random.randint(0, len(floors) - 1)
        floor = floors[idx_tile]
        self.entities[SPRITE_LAYER].append(Enemy(floor.rect.x, floor.rect.y, self, self.player))

    def __get_floors(self):
        floors = []
        for tile in self.entities[TILE_LAYER]:
            if isinstance(tile, Tile) and not tile.collider:
                floors.append(tile)
        return floors
