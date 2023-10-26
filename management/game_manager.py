import os

import pygame
import pygame.locals

from constants.sound_constants import GAME_LOST, WIN
from constants.sprite_constants import SCREEN_SIZE
from constants.ui_constants import GAME_OVER_TEXT, GAME_WON_TEXT, IMG_TUTORIAL, GAME_ENDED
from management.sound_manager import play
from map.map import Map
from constants.color_constants import WHITE, BLACK
from ui.screen import Screen
from ui.ui import UI

CLOCK = pygame.time.Clock()


class GameManager:

    def __init__(self):
        self.dt = 0
        self.ui = None
        self.pause = False
        self.running = False
        self.started = False
        self.game_over = False
        self.game_ended = False
        self.current_map = None
        self.game_over_ui = Screen(self)
        self.current_index_map = 0
        self.screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])

    def load_game(self):
        if not self.started:
            self.game_over_ui.set_image(IMG_TUTORIAL)
        self.running = True
        self.game_over = False
        self.current_index_map += 1
        self.current_map = Map(self, self.current_index_map)
        self.current_map.init_map()
        self.ui = UI(self)

        return self

    def game_loop(self):
        while self.running:
            # Reset the flags
            self.handle_keyboard()

            if self.started and not self.game_over and not self.pause:
                self.current_map.update(self.dt)
                self.ui.update()

            if not self.current_map.player.alive and not self.game_over:
                self.game_over = True
                self.game_over_ui.set_text(GAME_OVER_TEXT)
                play(GAME_LOST)
            elif self.current_map.game_won and not self.game_over:
                self.game_over = True
                self.__set_text_game_won()
                play(WIN)

            self.render()
            self.dt = CLOCK.tick(60)

        pygame.quit()

    def handle_keyboard(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] or (len(keys) > 0 and self.game_ended):
            self.running = False
        elif keys[pygame.K_p] and self.started and not self.game_over:
            self.pause = not self.pause
        elif keys[pygame.K_r]:
            if not self.started:
                self.started = True
            elif self.game_over and self.current_map.game_won:
                self.load_game()
            else:
                self.__reload_game()

    def render(self):
        if self.game_over or not self.started:
            self.screen.fill(BLACK)
            self.game_over_ui.render()
        else:
            self.__render_game()

        pygame.display.update()

    def __set_text_game_won(self):
        lst = os.listdir("assets/maps")  # your directory path
        if len(lst) > self.current_index_map:
            txt = GAME_WON_TEXT
        else:
            txt = GAME_ENDED
        self.game_over_ui.set_text(txt)

    def __reload_game(self):
        self.current_index_map -= 1
        self.load_game()

    def __render_game(self):
        self.screen.fill(WHITE)
        self.current_map.render()
        self.ui.render()
