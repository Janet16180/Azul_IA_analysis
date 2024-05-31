from enum import Enum, auto
from itertools import cycle
from .game_logic import Game_logic
from .game_logic import Player_model
from .game_logic import Game_viewer
from typing import List
from .models.dummy_model import Dummy_player
from icecream import ic

class Game_states(Enum):
    INIT_GAME = auto()
    FILL_FACTORY = auto()
    PLAYER_MOVE = auto()
    ROUND_END = auto()
    WALL_TILING = auto()
    GAME_END = auto()

class Player_cycle:
    def __init__(self, items):
        self.items = list(items)
        self.cycle = cycle(self.items)
        self.current = next(self.cycle)  

    def next(self):
        self.current = next(self.cycle)
        return self.current

    def set(self, value):
        if value in self.items:
            while self.current != value:
                self.current = next(self.cycle)
        else:
            raise ValueError(f"{value} is not in the cycle items.")
        
class Game_state_machine():
    def __init__(self, game_logic: Game_logic, players_models: List[Player_model]):
        self.state = Game_states.INIT_GAME

        self.game_logic = game_logic
        self.game_logic.players_boards[0].init_player = True

        self.player_cycle = Player_cycle(range(self.game_logic.number_players))
        self.current_player_index = 0

        if len(self.game_logic.players_boards) != len(players_models):
            raise ValueError(
                f"There must be a model for each player, number of players {len(self.game_logic.players_boards)}\n"
                f"number of models {len(players_models)}"
            )
        
        self.players_models = players_models

        self.state_methods_dict = {
            Game_states.INIT_GAME: self.init_game,
            Game_states.FILL_FACTORY: self.fill_factory,
            Game_states.PLAYER_MOVE: self.player_move,
            Game_states.WALL_TILING: self.wall_tiling,
            Game_states.ROUND_END: self.round_end,
            Game_states.GAME_END: self.game_end,
        }
        self.state_methods_dict[self.state]() # Execute first state

    def init_game(self):
        pass

    def fill_factory(self):
        self.game_logic.fill_factories()

    def player_move(self):
        player_model = self.players_models[self.current_player_index]

        player_move_tuple = player_model.player_move()
        factory_index, tile_type, row_index = player_move_tuple

        player_board = self.game_logic.players_boards[self.current_player_index]
        
        tiles = self.game_logic.get_tiles_from_factory(factory_index, tile_type)

        player_board.laying_tiles(row_index, tiles)

    def round_end(self):
        for player in self.game_logic.players_boards:
            player.wall_tiling()


    def wall_tiling(self):
        for player in self.game_logic.players_boards:
            player.wall_tiling()

    def game_end(self):
        pass

    def next(self):
        round_end = all(not sublist for sublist in self.game_logic.factories) and len(self.game_logic.center_tiles) == 0
        result = list((not sublist for sublist in self.game_logic.factories))
  
        next_state = None
        if self.state == Game_states.INIT_GAME:
            next_state = Game_states.FILL_FACTORY
        elif self.state == Game_states.FILL_FACTORY:
            next_state = Game_states.PLAYER_MOVE
        elif self.state == Game_states.PLAYER_MOVE and not round_end:
            self.__next_player()
            next_state = Game_states.PLAYER_MOVE
        elif self.state == Game_states.PLAYER_MOVE and round_end:
            next_state = Game_states.ROUND_END
        elif self.state == Game_states.ROUND_END: 
            next_state = Game_states.WALL_TILING
        elif self.state == Game_states.ROUND_END and self.game_logic.game_end:
            next_state = Game_states.GAME_END
        elif self.state == Game_states.WALL_TILING and not self.game_logic.game_end:
            self.__set_player_first_move()
            next_state = Game_states.FILL_FACTORY
        elif self.state == Game_states.WALL_TILING and self.game_logic.game_end:
            next_state = Game_states.GAME_END
        elif self.state == Game_states.GAME_END:
            next_state = Game_states.GAME_END

        exec_method = self.state_methods_dict[next_state]
        exec_method()

        self.state = next_state
        return self.state
    
    def __next_player(self):
        self.current_player_index = self.player_cycle.next()

    def __set_player_first_move(self):
        start_player_index = 0
        for i, player in enumerate(self.game_logic.players_boards):
            if player.init_player:
                start_player_index = i
                break

        self.current_player_index = start_player_index
        self.player_cycle.set(start_player_index)


    def print_state(self):
        if self.state == Game_states.PLAYER_MOVE:
            print(f"{self.state}_{self.current_player_index}")
        else:
            print(f"{self.state}")


def run_simulation(players_models: List, seed: int = 1):
    number_players = len(players_models)

    game_logic = Game_logic(number_players=number_players, seed=seed)
    game_view = Game_viewer(game_logic)

    players = []
    for i in range(players_models):
        players.appennd(
            players_models[i](game_view, i)
        )

    game_state = Game_state_machine(game_logic, players)

    while game_state.state != Game_states.GAME_END:
        game_state.next()