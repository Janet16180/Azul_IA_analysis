import pygame
from pathlib import Path
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, NUMBER_PLAYERS
from .game_logic import Game_logic, Game_viewer
import math
from .models.dummy_model import Dummy_player
from .run_simulation import Game_state_machine
import numpy as np
ROOT = Path(__file__).parent


class Game_GUI():
    def __init__(self, screen):
        self.screen = screen

        # simulation logic
        game_logic = Game_logic(number_players=NUMBER_PLAYERS)
        self.game_viewer = Game_viewer(game_logic)
        dummy_player_1 = Dummy_player(self.game_viewer, 0)
        dummy_player_2 = Dummy_player(self.game_viewer, 1)
        players = [dummy_player_1, dummy_player_2]
        self.game_state = Game_state_machine(game_logic, players)
        

        self.clock = pygame.time.Clock()
        self.running = True

        self.factories_positions = []

        self.factories_center_position = (0,0)
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

        radius_big_circle = 245

        cx = SCREEN_WIDTH//2
        cy = radius_big_circle + circle_radius + 10
        self.factories_center_position = (cx, cy)

        factories_num = len(self.game_viewer.get_factories())
        for i in range(factories_num):
            angle = 2 * math.pi * i / factories_num + 3*math.pi/2
            x = int(cx + radius_big_circle * math.cos(angle))
            y = int(cy + radius_big_circle * math.sin(angle))
            self.factories_positions.append((x,y))
            
            pygame.draw.circle(self.screen, circle_color, (x, y), circle_radius)
    
    def __create_spiral_order(self, array):
        n = math.ceil(math.sqrt(len(array)))
        # n = 4
        # print(n)
        spiral_matrix = [[0] * n for _ in range(n)]
        num = 1
        x, y = n // 2 - 1, n // 2 - 1
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        dir_idx = 0
        
        steps = 1  # Number of steps in the current direction
        while num <= n * n:
            for _ in range(2):  # Repeat for the same number of steps in two directions
                for _ in range(steps):
                    if num > n * n:
                        break
                    spiral_matrix[x][y] = num
                    num += 1
                    x += directions[dir_idx][0]
                    y += directions[dir_idx][1]
                dir_idx = (dir_idx + 1) % 4  # Change direction
            steps += 1

        spiral_matrix_indices = [element-1 for row in spiral_matrix for element in row]
        reorder_arr = [None for _ in range(len(spiral_matrix_indices))]

        for index, element in zip(spiral_matrix_indices, array):
            reorder_arr[index] = element

        return reorder_arr

    def draw_tiles(self):

        circle_color = (238,229,222)
        tile_size = 40
        separation = 5

        factories = self.game_viewer.get_factories()
        for i in range(len(factories)):
            factory_tiles = factories[i]
            factory_position = self.factories_positions[i]

            tile_1_position = (
                factory_position[0] + separation,
                factory_position[1] + separation,
                tile_size,
                tile_size
            )
            tile_2_position  = (
                factory_position[0] - tile_size - separation,
                factory_position[1] - tile_size - separation,
                tile_size,
                tile_size
            )
            tile_3_position  = (
                factory_position[0] - tile_size - separation,
                factory_position[1] + separation,
                tile_size,
                tile_size
            )
            tile_4_position  = (
                factory_position[0] + separation,
                factory_position[1] - tile_size - separation,
                tile_size,
                tile_size
            )
            tiles_positions = [
                tile_1_position,
                tile_2_position,
                tile_3_position,
                tile_4_position
            ]

            if len(factory_tiles) == 0:
                for i in range(4):
                    tile_color = circle_color
                    pygame.draw.rect(self.screen, tile_color, tiles_positions[i])
            else:
                for i, tile_type in enumerate(factory_tiles):
                    tile_color = self.tiles_colors_dict[tile_type]
                    pygame.draw.rect(self.screen, tile_color, tiles_positions[i])

        cx, cy = self.factories_center_position

        center_tiles = self.game_viewer.get_center_tiles()

        # center_tiles = [1,2,3,4,5]

        # If the square increase by 2 every time
        # 2x2=4
        # 4x4=16
        # 6x6=36
        # The sequence formula is f(x)=4n^2
        # To find the minimum value g(n)=sqrt(x/4) the inverse function
        # But if we want the square size (2n)(2n) size = 2n
        # where n = ceil(sqrt(x/4))
        needed_spaces = len(center_tiles)
        needed_spaces = 6*6
        square_size = 2*math.ceil(math.sqrt(needed_spaces / 4))
        relative_positions = []

        for i in range(square_size):
            for j in range(square_size):
                position_relative = np.array([j,i]) + np.array([-square_size//2,-square_size//2])
                relative_positions.append(position_relative)


        relative_positions = self.__create_spiral_order(relative_positions)
                
        for i, relative_position in enumerate(relative_positions):
            tile_position = (
                cx + relative_position[0]*(tile_size+separation),
                cy + relative_position[1]*(tile_size+separation),
                tile_size, 
                tile_size
            )

            if len(center_tiles) > i:
                tile_type = center_tiles[i]
                tile_color = self.tiles_colors_dict[tile_type]
            else:
                tile_color = (255,255,255)
            pygame.draw.rect(self.screen, tile_color, tile_position)



       

    def run(self):
        # self.game_state.next()
        # self.game_state.next()
        # self.game_state.next()
        # self.game_state.next()
        # self.game_state.next()
        # self.game_state.next()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            
            pygame.display.flip()  
            self.clock.tick(1)
            self.game_state.next()

            self.draw_tiles()

        pygame.quit()