import pygame
from pathlib import Path
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT
import math

ROOT = Path(__file__).parent

class Game():
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.expositors_num = 9
        self.expositors_positions = []

        self.__init_screen_setup()
        self.draw_tiles()

    def __init_screen_setup(self):
        board_image_path = Path(ROOT, "assets", "azul-board-500px.jpg")
        board_image = pygame.image.load(board_image_path)
        botton_position = SCREEN_HEIGHT - board_image.get_height()

        self.screen.fill((255, 255, 255)) 
        self.screen.blit(board_image, (0, botton_position))
        self.screen.blit(board_image, (board_image.get_width(), botton_position))
        self.screen.blit(board_image, (board_image.get_width()*2, botton_position))
        self.screen.blit(board_image, (board_image.get_width()*3, botton_position))

        circle_color =  (238,229,222)
        circle_radius = 70

        radius_big_circle = 220
        cx, cy = SCREEN_WIDTH//2, radius_big_circle + circle_radius + 10

        for i in range(self.expositors_num):
            angle = 2 * math.pi * i / self.expositors_num + 3*math.pi/2
            x = int(cx + radius_big_circle * math.cos(angle))
            y = int(cy + radius_big_circle * math.sin(angle))
            self.expositors_positions.append((x,y))
            
            pygame.draw.circle(self.screen, circle_color, (x, y), circle_radius)
    
    def draw_tiles(self):

        tile_color = (87,161,196)
        for expositor_position in self.expositors_positions:
            tile_size = 40
            separation = 5

            tile_1 = (
                expositor_position[0] + separation,
                expositor_position[1] + separation,
                tile_size,
                tile_size
            )
            tile_2 = (
                expositor_position[0] - tile_size - separation,
                expositor_position[1] - tile_size - separation,
                tile_size,
                tile_size
            )
            tile_3 = (
                expositor_position[0] - tile_size - separation,
                expositor_position[1] + separation,
                tile_size,
                tile_size
            )
            tile_4 = (
                expositor_position[0] + separation,
                expositor_position[1] - tile_size - separation,
                tile_size,
                tile_size
            )

            pygame.draw.rect(self.screen, tile_color, tile_1)
            pygame.draw.rect(self.screen, tile_color, tile_2)
            pygame.draw.rect(self.screen, tile_color, tile_3)
            pygame.draw.rect(self.screen, tile_color, tile_4)

       

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            pygame.display.flip()  
            # self.clock.tick(FPS)  

        pygame.quit()