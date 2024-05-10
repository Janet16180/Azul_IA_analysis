from __future__ import annotations
import numpy as np
import random
from typing import List
import warnings

from icecream import ic


class Board():
    def __init__(self, game_logic: Game_logic):
        self.game_logic = game_logic

        self.score = 0

        # Zero means that the space is empty
        # from 1 to 6 are the types of tiles
        self.wall = np.zeros((5,5), dtype=int)
        self.pattern_line = [np.zeros(i+1, dtype=int) for i in range(5)]
        self.floor_line = np.zeros(7, dtype=int)

    def wall_tiling(self):
        pass
        
    def pick_tiles(self, row: int, tiles: List[int]):

        if not self.validate_pick_tiles(row, tiles):
            raise RuntimeError("It is not possible to make such a move")
        
        floor_leftover_tiles = []

        actual_row = self.pattern_line[row]

        non_zero_index = np.count_nonzero(actual_row)
        free_spaces = len(actual_row) - non_zero_index

        # All tiles can be laid in the row 
        if len(tiles) <= free_spaces:
            self.pattern_line[row][non_zero_index: len(tiles)+non_zero_index] = tiles
        else:
            # Fill in the row and place the remaining tiles on the floor line (self.floor_line)
            leftover_tiles = tiles[free_spaces:]
            useful_tiles = tiles[:free_spaces]
            self.pattern_line[row][non_zero_index:] = useful_tiles


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


    def validate_pick_tiles(self, row: int, tiles: List[int]) -> bool:
        
        tiles_set = set(tiles)


        if len(tiles_set) != 1:
            warnings.warn(f"All tiles to be taken must be identical {tiles}")
            return False
        
        tile_type = tiles[0]
        
        actual_row = self.pattern_line[row]
        
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

    def fill_factories(self):
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

game = Game_logic(4)
game.fill_factories()

tiles = game.get_tiles_from_factory(0, 3)

tiles = [3,3,3]
ic(tiles)

board_player = game.players_boards[0]
board_player.pick_tiles(3, tiles)

rows = board_player.pattern_line
ic(rows)

board_player.pick_tiles(3, tiles)
rows = board_player.pattern_line
ic(rows)


board_player.pick_tiles(3, tiles)
rows = board_player.pattern_line
ic(rows)

board_player.pick_tiles(3, tiles)
rows = board_player.pattern_line
ic(rows)

board_player.pick_tiles(3, tiles)
rows = board_player.pattern_line
ic(rows)

discard = game.discarted_tiles
ic(discard)


player_board = board_player.floor_line
ic(player_board)