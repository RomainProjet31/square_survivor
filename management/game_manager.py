import pygame
import pygame.locals

from constants.sprite_constants import SCREEN_SIZE
from constants.text_constants import GAME_OVER_TEXT, GAME_WON_TEXT
from map.map import Map
from constants.color_constants import WHITE, BLACK
from ui.screen import Screen
from ui.ui import UI

CLOCK = pygame.time.Clock()


class GameManager:

    def __init__(self):
        self.dt = 0
        self.ui = None
        self.running = False
        self.game_over = False
        self.current_map = None
        self.game_over_ui = Screen(self)
        self.current_index_map = 0
        self.screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])

    def load_game(self):
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
            if not self.game_over:
                self.current_map.update(self.dt)
                self.ui.update()

            if not self.current_map.player.alive:
                self.game_over = True
                self.game_over_ui.set_text(GAME_OVER_TEXT)
            elif self.current_map.game_won:
                self.game_over = True
                self.game_over_ui.set_text(GAME_WON_TEXT)

            self.render()
            self.dt = CLOCK.tick(60)

        pygame.quit()

    def handle_keyboard(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False
        elif keys[pygame.K_r]:
            if self.current_map.game_won:
                self.load_game()
            else:
                self.__reload_game()

    def render(self):
        if self.game_over:
            self.screen.fill(BLACK)
            self.game_over_ui.render()
        else:
            self.__render_game()

        pygame.display.update()

    def __reload_game(self):
        self.current_index_map -= 1
        self.load_game()

    def __render_game(self):
        self.screen.fill(WHITE)
        self.current_map.render()
        self.ui.render()
