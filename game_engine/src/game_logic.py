import numpy as np
import random
from typing import List


from icecream import ic


class Board():
    def __init__(self):
        self.score = 0

        # Zero means that the space is empty
        # from 1 to 6 are the types of tiles
        self.wall = np.zeros((5,5), dtype=int)
        self.pattern_line = [np.zeros(i+1, dtype=int) for i in range(5)]
        self.floor_line = np.zeros(7, dtype=int)
        
    def wall_tiling(self, row: int, tiles: List):
        pass

    def validate_wall_tiling(self, row: int, tiles: List):
        pass


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
            Number of players, from 1 to 4, by default 4

        Raises
        ------
        ValueError
            The number of players should be between 1 and 4
        """
        random.seed(1)

        if number_players < 0 or number_players > 4:
            raise ValueError("The number of players should be between 1 and 4")
        
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
        self.players_boards = [Board() for _ in range(number_players)]
        
    def get_tiles_from_factory(self, factorie_num: int, tile: int) -> List[int]:
        """ Take the tiles from one of the factories 

        Parameters
        ----------
        factorie_num : int
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

        return
        pass

    def validate_get_tiles_from_factory(self, factorie_num: int, tile: int) -> bool:
        """ Validates that it is possible to remove the tiles from the factory

        Parameters
        ----------
        factorie_num : int
            Number of the factory from which the tile will be taken
            from 1 to the number of factories
            0 to take tiles from the center.
        tile : int
            Tile to be removed, from 1 to 5


        Returns
        -------
        bool
            if movement is not possible, False will be sent
            if the movement is valid True
        """
        pass
    

    def fill_factories(self):
        """ Empty the tiles from the bag (self.bag_tiles) 
        to the factories (self.factories) 

        This method already takes into account the case where there are not enough
        tiles in the bag, so in that case it will empty the bag and refill as much as possible of the factories
        then refill the bag with the discarded tiles (self.discarted_tiles) and suffle the bag 
        finally fill in the missing factories
        """

        self.factories = [[] for _ in range(self.factories_num)]

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

            self.factories[full_tiles_num] = self.bag_tiles

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

 

game = Game_logic()
game.fill_factories()
game.fill_factories()