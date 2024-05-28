import sys
# sys.path.append("..")
from ..game_logic import Player_model
import random
from typing import Tuple
from icecream import ic
class Dummy_player(Player_model):
    def player_move(self) -> Tuple[int, int, int]:
        valid_move = False
        num_factories = len(self.game_viewer.get_factories())

        while valid_move == False:
            factory_index =  random.randint(0, num_factories) - 1
            tile_type = random.randint(1, 5)
            row_index = random.randint(0, 5) -1
            valid_move = self.validate_player_move(factory_index, tile_type, row_index)
        return (factory_index, tile_type, row_index)
    


    # def validate_break_group_of_tiles(self, tiles: List[int]) -> bool:
    #     tile_type = tiles[0]

    #     possible_moves = False
        
    #     for i in range(5):
    #         wall_row = self.wall[i,]
    #         pattern_line_row = self.pattern_lines[i]

    #         # Row full, cannot lay tiles
    #         if np.count_nonzero(pattern_line_row) == len(pattern_line_row):
    #             continue

    #         # This row already contains tiles of another type
    #         if pattern_line_row[0] != tile_type and pattern_line_row[0] != 0:
    #             continue

    #         # This tile is already in the current row of the wall.
    #         if tile_type in wall_row:
    #             continue

    #         # There is an empty row where the tiles can be placed
    #         if pattern_line_row[0] == 0:
    #             warnings.warn(f"There is an empty row where the tiles can be placed, row with index {i}: {pattern_line_row}")
    #             possible_moves = True
    #             break

    #         # There is a row that is not full and you can still place tiles in it
    #         if pattern_line_row[0] == tile_type:
    #             warnings.warn(f"There is a row that is not full and you can still place tiles in it, row with index {i}: {pattern_line_row}")
    #             possible_moves = True
    #             break

    #     # As no movement is possible the tiles can be laid directly on the floor
    #     if possible_moves is False:
    #         return True
         
    #     return False
                