from piece import Piece
from typing import Tuple, Optional, Dict

Coordinates = Tuple[int, int]


class Player:
    """
    Represents a player in the game of Chinese Checkers.
    Each player have a name, color, and pieces on the board.
    at first, when the player is created, the player has no color and no pieces.
    you can add color and pieces to the player by using the set_player function.

    Attributes:
    name (str): The name of the player.
    color (str): The color of the player's pieces.
    pieces (dict[int, Piece]): A dictionary of the player's pieces, indexed by the piece's digit.
    num_of_winning (int): The number of games won by the player.
    num_of_losses (int): The number of games lost by the player.

    Methods:
    __init__(name: str): Initializes a new Player object with the given name.
    __str__() -> str: Returns a string representation of the player.
    set_player(color, cords): Sets the player's color and pieces on the board.
    change_player_piece(digit, new_cord): Changes the location of a player's piece.
    get_coordinate_piece(digit: int) -> (int, int): Returns the coordinates of a player's piece.
    get_digit(coordinate: (int, int)) -> int: Returns the digit of a player's piece at the given coordinates.
    get_name() -> str: Returns the name of the player.
    add_winning(): Increments the number of games won by the player.
    add_losses(): Increments the number of games lost by the player.
    """

    def __init__(self, name: str, num_win=0, num_loses=0) -> None:
        self.name = name
        self.color = ''
        self.pieces: Dict[int, Piece] = {}
        self.num_of_winning = num_win
        self.num_of_losses = num_loses

    def set_player(self, color: str, cords: list[Coordinates]) -> None:
        """
        Sets the player's color and pieces on the board for the game.
        receive the color of the player and the cords of the pieces.
        """
        self.color = color  # set the color of the player
        index_piece = 0
        self.pieces = {}  # for the case that the player already played
        for cord in cords:
            self.pieces[index_piece] = Piece(cord, index_piece)
            # create a new piece with the cords and add it to the player's pieces
            index_piece += 1

    def __str__(self):
        return self.name

    def change_player_piece(self, digit: int, new_cord: Coordinates) -> None:
        """
        receive the digit of the piece and the new cord of the piece and change the location of the piece.
        """
        for piece in self.pieces.values():
            if piece.get_digit() == digit:
                piece.change_coordinate(new_cord)

    def get_coordinate_piece(self, digit: int) -> Coordinates:
        """
        receive the digit of the piece and return the cord of this piece.
        """
        return self.pieces[digit].get_coordinate()

    def get_digit(self, coordinate: Coordinates) -> Optional[int]:
        """
        receive the cord of one piece and return the digit of this piece only if it exists, if no return nothing.
        """
        for piece in self.pieces.values():
            if piece.get_coordinate() == coordinate:
                return piece.get_digit()
        return None

    def get_name(self) -> str:
        return self.name

    def add_winning(self) -> None:
        """increment the number of winning by 1."""
        self.num_of_winning += 1

    def add_losses(self) -> None:
        """increment the number of losses by 1."""
        self.num_of_losses += 1
