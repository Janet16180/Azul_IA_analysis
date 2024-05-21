import pygame
from pathlib import Path
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, NUMBER_PLAYERS
from .game_logic import Game_logic, Game_viewer
import math

ROOT = Path(__file__).parent

class Game_GUI():
    def __init__(self, screen):
        self.screen = screen

        self.game_logic = Game_logic(number_players=NUMBER_PLAYERS)
        # self.game_logic.fill_factories()

        self.game_viewer = Game_viewer(self.game_logic)


        self.clock = pygame.time.Clock()
        self.running = True

        self.factories_positions = []

        self.__init_screen_setup()

        self.tiles_colors_dict = {
            1: (87,161,196),
            2: (3,3,2),
            3: (235,65,74),
            4: (99,209,223),
            5: (238,194,114),
        }

        self.draw_tiles()

    def __init_screen_setup(self):
        board_image_path = Path(ROOT, "assets", "azul-board-500px.jpg")
        board_image = pygame.image.load(board_image_path)
        botton_position = SCREEN_HEIGHT - board_image.get_height()

        self.screen.fill((255, 255, 255)) 

        # Draw players boards
        for i in range(self.game_viewer.get_number_of_players()):
            self.screen.blit(board_image, (board_image.get_width()*i, botton_position))

        # Draw factories circles
        circle_color = (238,229,222)
        circle_radius = 70

        radius_big_circle = 220

        cx = SCREEN_WIDTH//2
        cy = radius_big_circle + circle_radius + 10

        factories_num = len(self.game_viewer.get_factories())
        for i in range(factories_num):
            angle = 2 * math.pi * i / factories_num + 3*math.pi/2
            x = int(cx + radius_big_circle * math.cos(angle))
            y = int(cy + radius_big_circle * math.sin(angle))
            self.factories_positions.append((x,y))
            
            pygame.draw.circle(self.screen, circle_color, (x, y), circle_radius)
    
    def draw_tiles(self):

        tile_color = (87,161,196)

        factories = self.game_viewer.get_factories
        for i in range(len(factories)):
            factory_tiles = factories[i]
            factory_position = self.factories_positions[i]
            
            tile_size = 40
            separation = 5

            tile_1 = (
                factory_position[0] + separation,
                factory_position[1] + separation,
                tile_size,
                tile_size
            )
            tile_2 = (
                factory_position[0] - tile_size - separation,
                factory_position[1] - tile_size - separation,
                tile_size,
                tile_size
            )
            tile_3 = (
                factory_position[0] - tile_size - separation,
                factory_position[1] + separation,
                tile_size,
                tile_size
            )
            tile_4 = (
                factory_position[0] + separation,
                factory_position[1] - tile_size - separation,
                tile_size,
                tile_size
            )
            
            tile_colors =  [self.tiles_colors_dict[tile_type] for tile_type in factory_tiles]

            pygame.draw.rect(self.screen, tile_colors[0], tile_1)
            pygame.draw.rect(self.screen, tile_colors[1], tile_2)
            pygame.draw.rect(self.screen, tile_colors[2], tile_3)
            pygame.draw.rect(self.screen, tile_colors[3], tile_4)

       

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            pygame.display.flip()  
            # self.clock.tick(FPS)  

        pygame.quit()