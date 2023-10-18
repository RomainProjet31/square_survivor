import math

import pygame
from pygame import Rect

from constants.mecanic_constant import SHOOT_DELAY
from constants.sprite_constants import WEAPON_SIZE
from entities.enemy import Enemy
from entities.entity import Entity


class Weapon(Entity):
    def __init__(self, current_map, player):
        super().__init__(current_map, WEAPON_SIZE, 2, player.rect.x, player.rect.y, True)
        self.player = player
        self.angle = 0
        self.displacement_speed = 4
        self.mid_x = self.rect.w / 2.0
        self.mid_y = self.rect.h / 2.0
        self.bullets = []
        self.shoot_delay = SHOOT_DELAY

    def update(self, dt):
        self.shoot_delay += dt
        self.__handle_shifting(dt)
        self.__handle_bullets(dt)

    def shoot(self):
        if self.shoot_delay >= SHOOT_DELAY:
            self.__add_bullet()
            self.shoot_delay = 0

    def render(self):
        super().render()
        for bullet in self.bullets:
            bullet.render(self.current_map.game_manager.screen)

    def __add_bullet(self):
        rect_bullet = pygame.Rect(self.rect.x, self.rect.y, 5, 5)
        self.bullets.append(Bullet(rect_bullet, math.radians(self.angle)))

    def __handle_bullets(self, dt):
        for bullet in self.bullets:
            bullet.update(dt, self.current_map.entities[0], self.__get_enemies())
            if not bullet.alive:
                self.bullets.remove(bullet)

    def __handle_shifting(self, dt):
        self.angle += self.displacement_speed
        rad = math.radians(self.angle)
        center = self.player.rect.center
        self.rect.x = (center[0] - math.cos(rad) * self.speed * dt) - self.mid_x
        self.rect.y = (center[1] - math.sin(rad) * self.speed * dt) - self.mid_y

    def __get_enemies(self):
        enemies = []
        for entity in self.current_map.entities[1]:
            if isinstance(entity, Enemy):
                enemies.append(entity)
        return enemies


class Bullet:
    def __init__(self, rect: Rect, rad):
        self.rect = rect
        self.rad = rad
        self.speed = 0.5
        self.alive = True
        self.surf = pygame.Surface((self.rect.w, self.rect.h))

    def update(self, dt, tiles, enemies):
        for tile in tiles:
            if tile.collider and tile.rect.colliderect(self.rect):
                self.alive = False

        for enemy in enemies:
            if enemy.rect.colliderect(self.rect):
                enemy.alive = False
                self.alive = False

        if self.alive:
            self.__move(dt)

    def render(self, screen):
        screen.blit(self.surf, self.rect)

    def __move(self, dt):
        self.rect.x -= math.cos(self.rad) * self.speed * dt
        self.rect.y -= math.sin(self.rad) * self.speed * dt
