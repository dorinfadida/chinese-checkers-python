from typing import Tuple

Coordinates = Tuple[int, int]


class Piece:

    """
    Represents a single piece in the game of Chinese Checkers.
    Each piece is identified by a digit and has a specific board location.

    Attributes:
    digit (int): The number ("name") of this piece.
    coordinate (tuple[int, int]): The (x, y) board location of the piece.
    x (int): The x-coordinate of the piece's location, for quick access.
    y (int): The y-coordinate of the piece's location, for quick access.


    Methods:
    __init__(coordinate: Coordinates, digit: int): Initializes a new Piece object with the given coordinates and digit.
    __str__() -> str: Returns a string representation of the piece.
    get_coordinate() -> Coordinates: Returns the current board location of the piece as a tuple.
    get_digit() -> int: return the digit(int) of the piece
    change_coordinate(new_coordinate: Coordinates): updates the piece's location to the new specified coordinates.
    """

    def __init__(self, coordinate: Coordinates, digit: int) -> None:
        try:
            digit = int(digit)
            self.__digit = digit
        except ValueError:
            print("Invalid digit input. Setting digit to 0.")
            self.__digit = 0  # set to default value for invalid inputs
        else:
            self.__digit = digit
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.coordinate = coordinate

    def get_coordinate(self) -> Coordinates:
        """return the current board location (x, y) of the piece."""
        return self.coordinate

    def get_digit(self) -> int:
        """return the digit(int) of the piece."""
        return self.__digit

    def __str__(self) -> str:
        return f"Piece {self.__digit} is in {self.coordinate}"

    def change_coordinate(self, new_coordinate: Coordinates) -> None:
        """updates the piece's location to the new specified (x, y) coordinates."""
        self.x = new_coordinate[0]
        self.y = new_coordinate[1]
        self.coordinate = new_coordinate
