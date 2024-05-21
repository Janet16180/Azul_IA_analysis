from __future__ import annotations
import numpy as np
import random
from typing import List
import warnings
from collections import deque
from enum import Enum, auto
from itertools import cycle
from .model_abstract_class import Player_model
from icecream import ic


class Board():
    def __init__(self, game_logic: Game_logic):
        self.game_logic = game_logic

        self.score = 0

        # Zero means that the space is empty
        # from 1 to 6 are the types of tiles
        self.wall = np.zeros((5,5), dtype=int)
        self.pattern_lines = [np.zeros(i+1, dtype=int) for i in range(5)]
        self.floor_line = np.zeros(7, dtype=int)
        
        self.wall_default_pattern = self.__get_wall_default_patter()

        self.floor_line_minus_points = np.array([-1, -1, -2, -2, -2, -3, -3], dtype=int)

        self.init_player = False

    def __get_wall_default_patter(self) -> np.array:
        """ Creates the default pattern that has the player's board

        This creates a 5x5 array where each number is the type of 
        tile that should go in each box

        Returns
        -------
        np.array
            Array of integers with dimension 5x5 with the default pattern
        """

        circular_list = deque([1, 2, 3, 4, 5])
        wall_default_pattern = []

        for _ in range(5):
            row = list(circular_list)
            circular_list.rotate(1)
            wall_default_pattern.append(row)

        wall_default_pattern = np.array(wall_default_pattern)
        return wall_default_pattern

    def __update_score(self, new_tiles_index: tuple[int, int]) -> None:
        """ Updates the player's score during each tiling phase

        Parameters
        ----------
        new_tiles_index : tuple[int, int]
            Index of the new tile that was placed on the wall

        Raises
        ------
        ValueError
            Invalid status due to an error in the code logic
            this should not occur if the score logic is correct
        """

        new_tile_i, new_tile_j = new_tiles_index
        row = self.wall[new_tile_i]
        column = self.wall[:, new_tile_j]

        # Add points if fill row
        if np.count_nonzero(row) == 5:
            self.game_logic.game_end = True
            self.score += 2

        # Add points if fill column
        if np.count_nonzero(column) == 5:
            self.score += 7

        unique_values, counts = np.unique(self.wall, return_counts=True)
        tile_type = self.wall_default_pattern[new_tile_i, new_tile_j]

        unique_values_tile_index = np.where(unique_values == tile_type)[0][0]
        new_tile_total_count = counts[unique_values_tile_index]
        
        # Add points if fill all colors
        if new_tile_total_count == 5:
            self.score += 10

        
        # Count row new points
        count_from_row = 0
        for i in range(new_tile_j, -1, -1):
            row_tile_type = row[i]
            if row_tile_type ==  0:
                break

            count_from_row += 1

        for i in range(new_tile_j+1, 5):
            row_tile_type = row[i]
            if row_tile_type ==  0:
                break

            count_from_row += 1


        # Count column new points
        count_from_column = 0
        for i in range(new_tile_i, -1, -1):
            column_tile_type = column[i]
            if column_tile_type ==  0:
                break

            count_from_column += 1

        for i in range(new_tile_i+1, 5):
            column_tile_type = column[i]
            if column_tile_type ==  0:
                break

            count_from_column += 1


        # This logic is to avoid double counting the new tile
        if count_from_row == 1 and count_from_column == 1:
            self.score += 1
        elif count_from_row == 1 and count_from_column > 1:
            self.score += count_from_column
        elif count_from_row > 1 and count_from_column == 1:
            self.score += count_from_row
        # We only count the same tile twice if it connects with other 
        # tiles horizontally and vertically.
        elif count_from_row > 1 and count_from_column > 1:
            self.score += count_from_column + count_from_row
        else:
            # Theoretically this state should not be possible
            # but I add a raise ValueError just in case
            raise ValueError("Invalid count statue")

    def wall_tiling(self):
        """ When a round ends, this is the phase where the filled rows are
        placed on the wall and the points are counted

        1.- This function performs several tasks, it moves the tiles from
        the pattern lines (self.pattern_lines) to the wall (self.wall)

        2.- Count the points

        3.- Move tiles from the floor line (self.floor_line) and remove 
        excess tiles at the completion of a row (self.floor_line[row]) to the discard pile
        """

        discard_tiles = []
        for row in range(5):
            actual_row = self.pattern_lines[row]
            if np.count_nonzero(actual_row) != len(actual_row):
                continue

            tile_type = actual_row[0]
            row_default_pattern = self.wall_default_pattern[row]
            wall_tile_index = np.where(row_default_pattern == tile_type)[0][0]

            self.wall[row, wall_tile_index] = tile_type
            self.__update_score((row, wall_tile_index))
            
            row_discard_tiles = actual_row.copy()
            row_discard_tiles[0] = 0
            discard_tiles += list(row_discard_tiles[1:])
            actual_row[:] = 0 
        
        
        floor_tiles_discart = self.floor_line[:np.count_nonzero(self.floor_line)]
        floor_tiles_discart = list(floor_tiles_discart)

        # subtract the floor line tiles to the final score
        self.score += self.floor_line_minus_points[:len(floor_tiles_discart)].sum()

        # If the final score is less than zero, the result is set to zero
        if self.score < 0:
            self.score = 0

        if self.score >= 100:
            self.game_logic.game_end = True

        # If the first tile is the initial player's tile set self.init_player to True otherwise False
        if -1 in floor_tiles_discart:
            # Remove the first player tile form the floor_tiles_discart to avoid 
            # put that tile in the discard pile (self.game_logic.discarted_tiles)
            floor_tiles_discart.remove(-1)
            self.init_player = True
        else:
            self.init_player = False


        self.game_logic.discarted_tiles += floor_tiles_discart
        self.floor_line[:] = 0

        self.game_logic.discarted_tiles += discard_tiles
            
    def laying_tiles(self, row: int, tiles: List[int]) -> None:
        """ Place the tiles taken from the factory to one of the rows of the pattern lines (self.pattern_lines)

        Parameters
        ----------
        row : int
            Row to which you want to place the new tiles, there are 5 rows
            from o to 4
        tiles : List[int]
            List of tiles to be laid, all tiles must be of the same type

        Raises
        ------
        RuntimeError
            An error is thrown when trying to make an invalid move
            must first check that the movement is valid with validate_laying_tiles
        """

        if not self.validate_laying_tiles(row, tiles):
            raise RuntimeError("It is not possible to make such a move")
        
        floor_leftover_tiles = []

        actual_row = self.pattern_lines[row]

        non_zero_index = np.count_nonzero(actual_row)
        free_spaces = len(actual_row) - non_zero_index

        # All tiles can be laid in the row 
        if len(tiles) <= free_spaces:
            actual_row[non_zero_index: len(tiles)+non_zero_index] = tiles
        else:
            # Fill in the row and place the remaining tiles on the floor line (self.floor_line)
            leftover_tiles = tiles[free_spaces:]
            useful_tiles = tiles[:free_spaces]
            actual_row[non_zero_index:] = useful_tiles


            floor_index = np.count_nonzero(self.floor_line)
            floor_free_spaces = 7 - floor_index
            if len(leftover_tiles) <= floor_free_spaces:
                self.floor_line[floor_index: len(leftover_tiles)+floor_index] = leftover_tiles
            else:
                # There is a special case where the player has already filled 
                # all 7 available floor_line spaces
                # In that case the remaining tiles are placed in the discard_tiles space.
                floor_leftover_tiles = leftover_tiles[floor_free_spaces:]
                floor_useful_tiles = leftover_tiles[:floor_free_spaces]
                self.floor_line[floor_index:] = floor_useful_tiles

                # We place the remaining tiles in the discarted_tiles
                self.game_logic.discarted_tiles += floor_leftover_tiles

    def validate_laying_tiles(self, row: int, tiles: List[int]) -> bool:
        """ Validates if the movement to be made to place 
        the tiles in the pattern lines row (self.pattern_lines[row]) is valid

        Parameters
        ----------
        row : int
            Row to which you want to place the new tiles, there are 5 rows
            from o to 4
        tiles : List[int]
            List of tiles to be laid, all tiles must be of the same type

        Returns
        -------
        bool
            True if the movement is valid otherwise False
        """
        
        tiles_set = set(tiles)


        if len(tiles_set) != 1:
            warnings.warn(f"All tiles to be taken must be identical {tiles}")
            return False
        
        
        tile_type = tiles[0]
        
        actual_row = self.pattern_lines[row]
        
        if np.count_nonzero(actual_row) != 0 and tile_type not in actual_row:
            warnings.warn(f"These type of tiles '{tile_type}' cannot be placed, there is already another type of tile {actual_row}")
            return False

        wall_row = self.wall[row]
        if tile_type in wall_row:
            warnings.warn(f"This type of tile '{tile_type}' is already completed in this row")
            return False

        return True

        
class Game_logic():
    """ This class contains the main logic of the game

    Attributes
    ----------
    number_players : int
        Number of players
    bag_tiles : List[int]
        List with numbers representing the tiles
        there are 5 types of tiles so this list contains 
        20 times 1, 20 times 2, 20 times 3, etc up to 5.
        The numbers are scrambled and the number of tiles decreases as the game progresses
    discarted_tiles : List[int]
        List of discarded tiles
    factories_num : int
        Number of factors being used in the current game
        this value depends on the number of players
    factories : List[List[int]]
        Contains the status information of each of the factories
        this is a list where each sublist represents a factory
        and each factory can have a maximum of 4 tiles.
    game_end : bool
        Indicates if the game is over, True for when some of the players 
        reach the end game condition

    """
    def __init__(self, number_players: int = 4):
        """ 

        Parameters
        ----------
        number_players : int, optional
            Number of players, from 2 to 4, by default 4

        Raises
        ------
        ValueError
            The number of players should be between 2 and 4
        """
        random.seed(1)

        if number_players < 1 or number_players > 4:
            raise ValueError("The number of players should be between 2 and 4")
        
        self.number_players = number_players

        tiles = [
            i
            for i in range(1,5+1)
            for j in range(20)
        ]
        random.shuffle(tiles)
        self.bag_tiles = tiles

        self.discarted_tiles = []


        factories_num = 0
        if number_players == 2:
            factories_num = 5
        elif number_players == 3:
            factories_num = 7
        else:
            factories_num = 9
        self.factories_num = factories_num

        self.factories = [[] for _ in range(self.factories_num)]
        self.center_tiles = []
        self.players_boards = [Board(self) for _ in range(number_players)]

        self.game_end = False
    
    def get_tiles_from_factory(self, factory_num: int, tile: int) -> List[int]:
        """ Take the tiles from one of the factories 

        Parameters
        ----------
        factory_num : int
            Number of the factory from which the tile will be taken
            from 1 to the number of factories
            0 to take tiles from the center.
        tile : int
            Tile to be removed, from 1 to 5

        Returns
        -------
        List[int]
            List of tiles
        """
        if factory_num == -1:
            factory_tiles = self.center_tiles
        else:
            factory_tiles = self.factories[factory_num]

        if not self.validate_get_tiles_from_factory(factory_num, tile):
            raise RuntimeError("It was not possible to remove the tiles")

        delete_items = []
        factory_list_copy = factory_tiles[:]
        for val_list in factory_list_copy:
            if val_list == tile:           
                factory_tiles.remove(tile)
                delete_items.append(tile)

        return delete_items

    def validate_get_tiles_from_factory(self, factory_num: int, tile: int) -> bool:
        """ Validates that it is possible to remove the tiles from the factory

        Parameters
        ----------
        factory_num : int
            Number of the factory from which the tile will be taken
            from 0 to the number of factories
            -1 to take tiles from the center.
        tile : int
            Tile to be removed, from 1 to 5


        Returns
        -------
        bool
            if movement is not possible, False will be sent
            if the movement is valid True
        """

        if factory_num < -1 or factory_num > self.factories_num:
            warnings.warn(f"Invalid factory num {factory_num}")
            return False
        
        if tile < 1 or tile > 5:
            warnings.warn(f"Invalid type of tile {tile}")

        if factory_num == -1:
            factory_tiles = self.center_tiles
        else:
            factory_tiles = self.factories[factory_num]

        if tile not in factory_tiles:
            warnings.warn(f"The required tile is not in that factory {factory_tiles}, required tile {tile}")
            return False
        
        return True

    def fill_factories(self) -> None:
        """ Empty the tiles from the bag (self.bag_tiles) 
        to the factories (self.factories) 

        This method already takes into account the case where there are not enough
        tiles in the bag, so in that case it will empty the bag 
        and refill as much as possible of the factories
        then refill the bag with the discarded tiles (self.discarted_tiles) and suffle the bag 
        finally fill in the missing factories
        """
        if not all(not sublist for sublist in self.factories) or self.center_tiles != []:
            raise RuntimeError("It is not possible to fill the factories because they are not empty")


        if len(self.bag_tiles) >= self.factories_num*4:
            tiles = self.bag_tiles[:self.factories_num*4]
            self.bag_tiles = self.bag_tiles[self.factories_num*4:]

            for expositor_num in range(self.factories_num):
                self.factories[expositor_num] = tiles[expositor_num:expositor_num+4]

        else:
            full_tiles_num = len(self.bag_tiles)//4

            tiles = self.bag_tiles[:full_tiles_num*4]
            self.bag_tiles = self.bag_tiles[full_tiles_num*4:]

            for expositor_num in range(full_tiles_num):
                self.factories[expositor_num] = tiles[expositor_num:expositor_num+4]

            self.factories[full_tiles_num] = self.bag_tiles[:]

            # Pour the discarded tiles back into the bag
            self.bag_tiles = self.discarted_tiles
            random.shuffle(self.bag_tiles)
            self.discarted_tiles = []


            # Fill in the remaining factories
            for _ in range(len(self.factories[full_tiles_num]), 4):
                self.factories[full_tiles_num].append(
                    self.bag_tiles.pop()
                )

            for factory_num in range(full_tiles_num+1, self.factories_num):
                tiles = self.bag_tiles[:4]
                self.bag_tiles = self.bag_tiles[4:]

                self.factories[factory_num] = tiles

class Game_viewer():
    def __init__(self, game_logic: Game_logic):
        self.game_logic = game_logic

        self.__factories = game_logic.factories
        self.__center_tiles = game_logic.center_tiles

        self.__players_boards = game_logic.players_boards

    def get_factories(self):
        return self.__factories
    
    def get_center_tiles(self):
        return self.__center_tiles
    
    def get_number_of_players(self):
        return self.game_logic.number_players
    
    def get_players_wall(self):
        walls = []
        for player in self.__players_boards:
            wall = player.wall
            walls.append(wall)

        return walls
    
    def get_players_floor_lines(self):
        floor_lines = []
        for player in self.__players_boards:
            fllor_line = player.floor_line
            floor_lines.append(fllor_line)

        return floor_lines
    
    def get_players_pattern_lines(self):
        pattern_lines = []
        for player in self.__players_boards:
            player_pattern_lines = player.pattern_lines
            pattern_lines.append(player_pattern_lines)
        
        return pattern_lines

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

        if len(self.game_logic.players_boards) == len(players_models):
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

        player_move_get_tiles = player_model.get_move_tiles_from_factory()
        player_move_laying_tiles = player_model.get_move_laying_tiles()

        player_board = self.game_logic.players_boards[self.current_player_index]
        
        tiles = self.game_logic.get_tiles_from_factory(*player_move_get_tiles)

        player_board.laying_tiles(player_move_laying_tiles, tiles)

    def round_end(self):
        pass

    def wall_tiling(self):
        for player in self.game_logic.players_boards:
            player.wall_tiling()

    def game_end(self):
        pass

    def next(self):
        round_end = all(not sublist for sublist in self.game_logic.factories) and len(self.game_logic.center_tiles) == 0

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
        elif self.state == Game_states.WALL_TILING and not self.game_logic.game_end:
            self.__set_player_first_move()
            next_state = Game_states.FILL_FACTORY
        elif self.state == Game_states.WALL_TILING and self.game_logic.game_end:
            next_state = Game_states.GAME_END
        elif self.state == Game_states.GAME_END:
            next_state = Game_states.GAME_END
        
        exec_method = self.state_methods_dict[self.state]
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