import pygame
import sys
from pathlib import Path
from src.game_gui import Game_GUI
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.run_simulation import run_simulation


def main():
    # run_simulation()
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Azul IA simulation")
    
    game = Game_GUI(screen)
    game.run()

if __name__ == '__main__':
    main()
