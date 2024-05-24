import sys
# sys.path.append("..")
from ..game_logic import Player_model
import random
from typing import Tuple
from icecream import ic
class Dummy_player(Player_model):
    def player_move(self) -> Tuple[int, int, int]:
        ic(self.game_viewer.get_players_pattern_lines())
        ic(self.game_viewer.get_factories())
        ic(self.game_viewer.get_center_tiles())
        valid_move = False
        num_factories = len(self.game_viewer.get_factories())

        while valid_move == False:
            factory_index =  random.randint(0, num_factories) - 1
            tile_type = random.randint(1, 5)
            row_index = random.randint(0, 4)
            valid_move = self.validate_player_move(factory_index, tile_type, row_index)
        return (factory_index, tile_type, row_index)
