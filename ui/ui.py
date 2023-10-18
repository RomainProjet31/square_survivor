import pygame.draw
from pygame import Rect, Surface, draw

from constants.color_constants import WHITE, BLACK, RED
from constants.mecanic_constant import SHOOT_DELAY
from constants.sprite_constants import SCREEN_SIZE

timer_w = 80
timer_h = 25
circle_size = 10
circle_offset = 15
vertical_alignment = 10
circle_alignment = vertical_alignment + circle_size / 2
begin_hp_coord = (SCREEN_SIZE / 3, vertical_alignment)


class UI:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.fill_timer = Rect(10, vertical_alignment, timer_w, timer_h)
        self.frame_timer = Rect(10, vertical_alignment, timer_w, timer_h)
        self.player = self.game_manager.current_map.player
        self.health_icons_x = []

    def update(self):
        percent = 1 if self.player.weapon.shoot_delay > SHOOT_DELAY else self.player.weapon.shoot_delay / SHOOT_DELAY
        self.fill_timer.w = self.frame_timer.w * percent

        self.health_icons_x.clear()
        for i in range(self.player.hp):
            offset_n = (i * circle_size + circle_offset * i)
            self.health_icons_x.append(begin_hp_coord[0] + offset_n)

    def render(self):
        pygame.draw.rect(self.game_manager.screen, BLACK, self.fill_timer)
        pygame.draw.rect(self.game_manager.screen, WHITE, self.frame_timer, 2)

        for circle_x in self.health_icons_x:
            pygame.draw.circle(self.game_manager.screen, RED, (circle_x, circle_alignment), circle_size)
