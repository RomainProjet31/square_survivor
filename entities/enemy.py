from constants.color_constants import RED
from constants.sprite_constants import ENEMY_SIZE
from entities.entity import Entity


class Enemy(Entity):
    def __init__(self, x, y, current_map, player):
        super().__init__(current_map, ENEMY_SIZE, .1, x, y, True, RED)
        self.player = player

    def update(self, dt):
        self.compute_astar()
        self.handle_collision()
        super().update(dt)

    def compute_astar(self):
        # TODO: Add A* algorithm
        dir_x = self.player.rect.x - self.rect.x
        dir_y = self.player.rect.y - self.rect.y
        if dir_x < 0:
            self.vel.x = -1
        elif dir_x > 0:
            self.vel.x = 1

        if dir_y < 0:
            self.vel.y = -1
        elif dir_y > 0:
            self.vel.y = 1
