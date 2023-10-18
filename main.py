import pygame

from management.game_manager import GameManager

pygame.init()
GameManager().load_game().game_loop()
