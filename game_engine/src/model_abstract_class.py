from abc import ABC, abstractmethod
from .game_logic import Game_viewer
from typing import Tuple

class Player_model(ABC):
    def __init__(self, Game_viewer: Game_viewer, player_index: int):
        self.game_viewer = Game_viewer
        self.player_index = player_index

    @abstractmethod
    def player_move(self) -> Tuple[int, int, int]:
        pass

    def validate_player_move(self, factory_index: int, tile_type: int, row_index: int):
        result = self.game_viewer.validate_player_move(self.player_index, factory_index, tile_type, row_index)
        return result
