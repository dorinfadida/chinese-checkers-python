import copy

from colorama import Style, Fore
from helper import empty_board
from player import Player
from helper import color_codes
from typing import List, Dict, Tuple, Any

Coordinates = Tuple[int, int]


class Board:
    """
    Represents the game board for Chinese Checkers, accommodating 2, 3, 4, or 6 players.
    The board is a hexagon with a star shape, consisting of a grid of spaces where pieces can move.

    Attributes:
    rows (int): The number of rows in the board.
    columns (int): The number of columns in the board.
    board (list[list[int]]): A 2D list representing the board.
    -1 represents a space not on the board, -2 represents an empty space, and other values represent player pieces.

    Methods:
    print_board(players: List[Player]) -> None:
        prints the board with player pieces(*) colored according to their color.
    print_player_turn_board(players: List[Player], player_play: int) -> None:
        prints the board with player pieces colored.
        according to their color, with the current player's pieces numbered.
    print_possible_move_board(players: List[Player], player_play: Player, possible_moves: Dict[str, Coordinates])
     -> None:
        prints the board with player pieces colored according to their color,
        with the current player's pieces numbered and possible moves marked with letters.
    get_value(cord: Coordinates) -> int:
        returns the value of the place in the board at the specified coordinates.
    clean_place(cord: Coordinates) -> None:
        clears the place in the board at the specified coordinates.
    set_value(cord: Coordinates, value: Any) -> None:
        sets the value of the place in the board at the specified coordinates.
    """

    def __init__(self):
        self.rows = 17
        self.columns = 25
        self.board = copy.deepcopy(empty_board)

    def print_board(self, players: list[Player]) -> None:
        """receive a list of players and print the board with colors for each player in the game."""
        temp_board: List[list[Any]] = self.board
        # place in the temp board the players pieces
        for player_index in range(len(players)):
            player = players[player_index]
            for piece in player.pieces.values():
                temp_board[piece.x][piece.y] = player.color

        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col] == -1:  # if the place is not in the board
                    print(" ", end="")

                else:
                    if self.board[row][col] == -2:  # if the place is empty
                        print("*", end="")
                    else:  # if the place is a player piece
                        color_name = temp_board[row][col]  # get the color of the player
                        color_code = color_codes[color_name]  # get the color code of the player

                        print(color_code + "*" + Style.RESET_ALL, end="")
            print()

    def print_player_turn_board(self, players: List[Player], player_play: int) -> None:
        """receive a list of players and the index of the player that play now,
         and print the board with the pieces with color for each player in the game between any turn.
         for the current player that play now, the pieces will be with the digit of the piece."""
        temp_board: List[List[Any]] = self.board
        # place in the temp board the players pieces
        for player_index in range(len(players)):
            player = players[player_index]
            for piece in player.pieces.values():
                temp_board[piece.x][piece.y] = player.color

        player_color = players[player_play].color  # get the color of the player that play now

        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col] == -1:  # if the place is not in the board
                    print(" ", end="")

                else:
                    if self.board[row][col] == -2:  # if the place is empty
                        print("*", end="")
                    else:  # if the place is a player piece
                        color_name = temp_board[row][col]  # get the color of the player
                        color_code = color_codes[color_name]  # get the color code of the player

                        if color_name == player_color:  # if the player that play now is the player of the piece
                            digit = players[player_play].get_digit((row, col))
                            print(color_code + str(digit) + Style.RESET_ALL, end="")
                        else:
                            print(color_code + "*" + Style.RESET_ALL, end="")
                            # for pieces that are not the player that play now.
            print()

    def print_possible_move_board(self, players: List[Player], player_play: Player,
                                  possible_moves: Dict[str, Coordinates]) -> None:
        """receive a list of players, the player that play now and the possible moves of the player,
        and print the board with the pieces with color for each player in the game between any turn.
        for the current player that play now, the pieces will be with the digit of the piece and the possible moves
        will be with the letter of the move in the same color of the player.
        """
        temp_board = self.board
        # place in the temp board the players pieces
        for player_index in range(len(players)):
            player = players[player_index]
            for piece in player.pieces.values():
                temp_board[piece.x][piece.y] = player.color

        # place in the temp board the possible moves of the player
        for key in possible_moves.keys():
            cord = possible_moves[key]
            temp_board[cord[0]][cord[1]] = key

        player_color = player_play.color  # get the color of the player that play now

        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col] == -1:  # if the place is not in the board
                    print(" ", end="")

                else:
                    if self.board[row][col] == -2:  # if the place is empty
                        print("*", end="")
                    else:
                        if 'a' <= temp_board[row][col] <= 'x':  # if the place is a possible move
                            print(Fore.MAGENTA + str(temp_board[row][col]) + Fore.RESET, end="")
                        else:
                            color_name = temp_board[row][col]
                            color_code = color_codes[color_name]
                            if color_name == player_color:
                                digit = player_play.get_digit((row, col))
                                print(color_code + str(digit) + Style.RESET_ALL, end="")
                            else:
                                print(color_code + "*" + Style.RESET_ALL, end="")
            print()

    def get_value(self, cord: Coordinates) -> int:
        """
        receive a cord and return the value of the place in the board.
        """
        return self.board[cord[0]][cord[1]]

    def clean_place(self, cord: Coordinates) -> None:
        """receive a cord and clean the place in the board."""
        self.board[cord[0]][cord[1]] = -2

    def set_value(self, cord: Coordinates, value: Any) -> None:
        """receive a cord and a value and set the value in the place in the board.
        """
        self.board[cord[0]][cord[1]] = value
