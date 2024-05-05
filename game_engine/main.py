import pygame
import sys
from pathlib import Path
from src.game_gui import Game_GUI
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT



def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My Pygame Project")
    
    game = Game_GUI(screen)
    game.run()

if __name__ == '__main__':
    main()