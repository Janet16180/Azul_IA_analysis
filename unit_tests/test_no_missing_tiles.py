import pytest
import pandas as pd
import sys 
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

# sys.path.append(str(Path(ROOT / "game_engime" / "src")))
# print(str(Path(ROOT, "game_engime", "src")))
# sys.path.append(str(Path(ROOT.parent, "game_engine", "src", "models")))

# from models.dummy_model import Dummy_model
from game_engine.src.models.dummy_model import Dummy_player
from game_engine.src.game_logic import Game_logic, Game_viewer
from game_engine.src.run_simulation import Game_state_machine, Game_states
from icecream import ic
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

def validate_game_view(game_view: Game_viewer):
    players_walls = game_view.get_players_wall()
    players_line_patterns = game_view.get_players_pattern_lines()
    players_floors = game_view.get_players_floor_lines()

    center_tiles = game_view.get_center_tiles()
    bag_tiles = game_view.get_bag_tiles()
    discarted_tiles = game_view.get_discarted_tiles()
    factories_tiles = game_view.get_factories()

    all_tiles = center_tiles + bag_tiles + discarted_tiles

    for tiles in players_walls:
        all_tiles += list(tiles[tiles != 0])

    for player_line_patterns in players_line_patterns:
        for tiles in player_line_patterns:
            all_tiles += list(tiles[tiles != 0])

    for tiles in players_floors:
        all_tiles += list(tiles[tiles != 0])

    for tiles in factories_tiles:
        all_tiles += tiles

    if len(all_tiles) != 100:
        raise RuntimeError(f"The total number of tiles is not 100, number of tiles: {len(all_tiles)}")
    
    all_tiles = np.array(all_tiles)

    for i in range(1,6):
        tiles_by_type = all_tiles[all_tiles == i]
        if len(tiles_by_type) != 20:
            raise RuntimeError(f"The number of tiles of type {i} is not equal to 20, total: {len(tiles_by_type)}")




@pytest.mark.parametrize(
    "num_players",
    [1, 2, 3, 4]
)
@pytest.mark.parametrize(
    "seed",
    [i for i in range(100)]
)
def test_random_games_dummy_model(num_players, seed):
    game_logic = Game_logic(number_players=num_players, seed=seed)
    game_view = Game_viewer(game_logic)
    players = []
    for i in range(num_players):
        players.append(
            Dummy_player(game_view, i)
        )

    game_state = Game_state_machine(game_logic, players)
    while game_state.state != Game_states.GAME_END:
        validate_game_view(game_view)
        game_state.next()


    