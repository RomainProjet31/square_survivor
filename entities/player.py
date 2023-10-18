import pygame.draw

from constants.mecanic_constant import DAMAGE_DELAY, BLINK_DELAY
from constants.sprite_constants import PLAYER_SIZE
from entities.enemy import Enemy
from entities.entity import Entity
from constants.color_constants import BLUE
from entities.weapon import Weapon


class Player(Entity):
    def __init__(self, current_map, x, y):
        super().__init__(current_map, PLAYER_SIZE, 0.5, x, y, True, BLUE)
        self.weapon = Weapon(self.current_map, self)
        self.tick_damage = DAMAGE_DELAY
        self.tick_blink = BLINK_DELAY
        self.hp = 3

    def update(self, dt):
        self.handle_keyboard()
        self.handle_collision()
        self.handle_collision_enemy(dt)
        self.update_blink(dt)
        super().update(dt)

        self.weapon.update(dt)

    def render(self):
        super().render()
        self.weapon.render()

    def update_blink(self, dt):
        if self.tick_damage < DAMAGE_DELAY and self.tick_blink >= BLINK_DELAY:
            alpha = 0
            if self.surf.get_alpha() == 0:
                alpha = 255
            self.surf.set_alpha(alpha)
            self.tick_blink = 0
        elif self.tick_damage > DAMAGE_DELAY:
            self.surf.set_alpha(255)
        else:
            self.tick_blink += dt

    def handle_keyboard(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.vel.x = 1
        elif keys[pygame.K_LEFT]:
            self.vel.x = -1

        if keys[pygame.K_UP]:
            self.vel.y = -1
        elif keys[pygame.K_DOWN]:
            self.vel.y = 1

        if keys[pygame.K_SPACE]:
            self.weapon.shoot()

    def handle_collision_enemy(self, dt):
        for entity in self.current_map.entities[1]:
            if isinstance(entity, Enemy) and self.rect.colliderect(entity.rect) and self.tick_damage >= DAMAGE_DELAY:
                self.__take_damage()

        if self.tick_damage < DAMAGE_DELAY:
            self.tick_damage += dt

    def __take_damage(self):
        if self.hp > 0:
            self.hp -= 1
            self.tick_damage = 0

        if self.hp <= 0:
            self.alive = False
