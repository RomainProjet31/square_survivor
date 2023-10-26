import pygame

from constants.color_constants import WHITE
from constants.sprite_constants import SCREEN_SIZE, FONT_SIZE_SCREEN
from utils.math_utils import Vec

IMG_PATH = "assets/images/"


class Screen:
    def __init__(self, game_manager):
        self.font = None
        self.__text = ""
        self.__img = None
        self.game_manager = game_manager
        self.wallpaper = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
        self.rect_wallpaper = self.wallpaper.get_rect()
        self.text_pos = Vec(0, 0)

    def set_image(self, img_path):
        self.__img = pygame.image.load(IMG_PATH + img_path).convert()

    def set_text(self, text):
        self.__text = text
        self.font = pygame.font.SysFont(None, FONT_SIZE_SCREEN)
        self.__img = self.font.render(self.__text, True, WHITE)
        txt_size = self.font.size(text)
        self.text_pos.x = self.rect_wallpaper.w / 2 - txt_size[0] / 2
        self.text_pos.y = self.rect_wallpaper.h / 2 - txt_size[1] / 2

    def render(self):
        self.game_manager.screen.blit(self.__img, (self.text_pos.x, self.text_pos.y))
