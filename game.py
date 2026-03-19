import random
import logging
from datetime import datetime
from board import *
from piece import *
from helper import *
from typing import Optional, Dict, Callable


class ExitGameException(Exception):
    """Exception for exit the game."""
    pass


class Game:
    """A class represent one game - Chinese Checkers.
    this class include the board of the game, the players, the current turn player, and the winner of the game.
    and have option for play a friendly play or against the computer/smart computer.

    Attributes:
    board (Board): The board of the game.
    players (list[Player]): A list of players in the game.
    current_turn_p (int): The number of the player that play now. before the game start it 0. and after the game start
    it starts from 1.
    winner (Player): The player that wins the game.

    Methods:
    - pre_game(against) -> Optional[Player]: organize the game board and start the game.
    - reset_current_turn_p() -> None: reset the current turn player to 1 to start a new round of the game.
    - add_current_turn_p() -> None: increment the current turn player by 1.
    - local_game() -> Optional[Player]: a friendly game rounds that return the winner of the game.
    - game_with_computer(computer_turn: Callable) -> Optional[Player]:
      start a game with one local player against computer.
    - local_turn() -> bool: the turn of the local player.
    - choose_piece_turn() -> Piece: ask the local player to choose a piece to move and return the piece.
    - coordinate_in_board(coordinate: Coordinates) -> bool: check if the move is valid.
    three functions for the algorithm of the possible moves:
    1. first_check(coordinate: Coordinates) -> list[Coordinates]: the first check for the possible moves of the piece.
    2. check_jump(coordinate: Coordinates) -> list[Coordinates]: check if the coordinate is empty and if it is,
      save this coordinate.
    3. check_diagonal_empty(coordinate: Coordinates, coords_list=None, visited=None) -> list[Coordinates]:
      check if there is more jumps do to.
    - dict_possible_moves(current_piece: Piece) -> Dict[str, Coordinates]:
      return a possible move dict to the piece receive order by letters.
    - choose_move_turn(possible_moves_dict: Dict[str, Coordinates], num_piece: int) -> None:
      ask the local player to choose a letter to move the piece.
    - smart_turn() -> None: the turn of the smart computer.
    - computer_turn() -> None: the computer turn.
    - move_piece(possible_moves: Dict[str, Coordinates], piece: int, new_cord: Coordinates, prev_cord: Coordinates)
      -> None: move piece for the computer.
    - move_piece_load(cur_player: int, piece: int, new_cord: Coordinates) -> None: move piece for the loading game.
    - is_winner(potential_winner: Player) -> bool: check if the player is the winner.
    - is_game_finished() -> bool: check if the game is finished.
    """

    def __init__(self, players: list):
        self.board = Board()  # create an empty board.
        self.players = players  # a list of players to start on this game.
        self.current_turn_p = 0
        self.winner = None

    def pre_game(self, against) -> Optional[Player]:
        """
        this method organize the game board - by giving every player a color and coords for any piece.
        at the end current_turn_p ready to play.
        this method also create a log file for the game.
        and at the end return the winner of the game.
        """
        # create a log file for the game
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'game_{timestamp}.log'
        logging.basicConfig(filename=filename, level=logging.INFO,
                            format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        str_players = "Players:\n"
        num_players = len(self.players)
        relevant_cord = players_in_game[num_players]  # from helper
        for player_index in range(num_players):  # for any player:
            player = self.players[player_index]
            player.set_player(colors[player_index], relevant_cord[player_index])  # set player
            str_players += f"player_num: {player_index + 1} player_name: {player.name} player_color: {player.color}\n"
            # string for logging file

        self.current_turn_p = 1  # ready to start the game.

        log_game_event(f"num players: {len(self.players)}", player=str_players)  # log the players

        winner = None
        if against == "computer":
            log_game_event("Game against Computer")
            winner = self.game_with_computer(self.computer_turn)
        elif against == "friends":
            log_game_event("Game against Friends")
            winner = self.local_game()
        elif against == "smart":
            log_game_event("Game against Smart Computer")
            winner = self.game_with_computer(self.smart_turn)

        return winner

    def reset_current_turn_p(self) -> None:
        """this function reset the current turn player to 1 to start a new round of the game."""
        self.current_turn_p = 1

    def add_current_turn_p(self) -> None:
        """this function increment the current turn player by 1."""
        self.current_turn_p += 1

    def local_game(self) -> Optional[Player]:
        """a friendly game rounds that return the winner of the game."""
        while not self.is_game_finished():
            for num_turn in range(len(self.players)):  # the game routine until someone wins
                if self.local_turn():  # for the local players
                    break
        if self.winner:
            print(f"The winner of the game is {self.winner}!")  # print the winner
            log_game_event("Winner", player=self.winner)
            self.winner.add_winning()  # add the winning to the winner
            for player in self.players:
                if player != self.winner:
                    player.add_losses()  # add the losses to the other players
            self.board.print_board(self.players)
        return self.winner

    def game_with_computer(self, computer_turn: Callable) -> Optional[Player]:
        """
        this function start a game with one local player against computer.
        there is two option: against regular computer or against smart computer.
        receive the function of the computer turn according the type of the game.
        return the winner of the game.
        """
        while not self.is_game_finished():  # the game routine until someone wins
            for num_turn in range(len(self.players)):
                if num_turn == 0:  # for the local player
                    if self.local_turn():  # local choose a piece and move it
                        break
                else:  # for the computer players
                    computer_turn()  # smart or regular computer
                    if self.is_winner(self.players[num_turn]):
                        self.winner = self.players[num_turn]
                        break
                    else:
                        self.add_current_turn_p()
        if self.winner:
            print(f"The winner of the game is {self.winner}!")
            log_game_event("Winner", player=self.winner)
            if self.winner == self.players[0]:
                self.winner.add_winning()  # add the winning to the winner only if it local player
                self.board.print_board(self.players)
                return self.winner
            else:
                self.players[0].add_losses()  # add the losses to the local player
        return self.winner

    def local_turn(self) -> bool:
        """
        this function represent the turn of the local player.
        the player choose a piece to move and move it.
        return True if the game is finished - there is a winner.
        return False if the game is not finished.
        """
        flag = False  # if the game is finished - True
        if self.current_turn_p == len(self.players) + 1:
            self.reset_current_turn_p()
        self.board.print_player_turn_board(self.players, self.current_turn_p - 1)
        piece_play = self.choose_piece_turn()
        dict_moves = self.dict_possible_moves(piece_play)
        while dict_moves == {}:  # if there is no possible moves for the piece
            print("There is no possible moves for this piece.")
            piece_play = self.choose_piece_turn()
            dict_moves = self.dict_possible_moves(piece_play)
        self.board.print_possible_move_board(self.players, self.players[self.current_turn_p - 1],
                                             dict_moves)
        self.choose_move_turn(dict_moves, piece_play.get_digit())
        if self.is_winner(self.players[self.current_turn_p - 1]):
            self.winner = self.players[self.current_turn_p - 1]
            flag = True
        else:
            self.add_current_turn_p()
        return flag

    def choose_piece_turn(self):
        """this function ask the local player to choose a piece to move and return the piece."""
        current_piece = None
        while True:
            try:
                piece = input(f"{self.players[self.current_turn_p - 1].name}, choose a piece to move")
                if piece.upper() == "EXIT":
                    close_log_file()
                    raise ExitGameException
                piece = int(piece)
            except ValueError:
                print("Please enter a number")
                continue
            if piece in self.players[self.current_turn_p - 1].pieces.keys():
                current_piece = self.players[self.current_turn_p - 1].pieces[piece]
                break
            else:
                print("The piece you chose is not in the game, please choose a piece from the game.")
        return current_piece

    def smart_turn(self):
        """
        the turn of the smart computer.
        the smart computer choose the best piece to move and move it.
        the best piece is direct for the winning place.
        """
        numbers_pieces = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        piece_play = random.choice(numbers_pieces)
        dict_moves = self.dict_possible_moves(self.players[self.current_turn_p - 1].pieces[piece_play])
        while dict_moves == {}:  # if there is no possible moves for the piece
            numbers_pieces.remove(piece_play)  # remove the piece from the list
            piece_play = random.choice(numbers_pieces)
            dict_moves = self.dict_possible_moves(self.players[self.current_turn_p - 1].pieces[piece_play])
        list_moves = list(dict_moves.values())  # list of the possible moves - tuples
        list_moves.sort(key=lambda t: (-t[0], abs(t[1] - 12)))  # choose the best move
        # x value should be the biggest and the y value should be the closest to the middle
        new_cord = list_moves[0]
        prev_cord = self.players[self.current_turn_p - 1].get_coordinate_piece(piece_play)
        self.move_piece(dict_moves, piece_play, new_cord, prev_cord)

    def computer_turn(self) -> None:
        """
        the computer turn.
        the computer choose a random piece to move and move it.
        """
        numbers_pieces = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        piece_play = random.choice(numbers_pieces)
        dict_moves = self.dict_possible_moves(self.players[self.current_turn_p - 1].pieces[piece_play])
        while dict_moves == {}:  # if there is no possible moves for the piece
            numbers_pieces.remove(piece_play)  # remove the piece from the list
            piece_play = random.choice(numbers_pieces)
            dict_moves = self.dict_possible_moves(self.players[self.current_turn_p - 1].pieces[piece_play])
        list_moves = list(dict_moves.keys())
        move = random.choice(list_moves)
        new_cord = dict_moves[move]
        prev_cord = self.players[self.current_turn_p - 1].get_coordinate_piece(piece_play)
        self.move_piece(dict_moves, piece_play, new_cord, prev_cord)

    def coordinate_in_board(self, coordinate: Coordinates) -> bool:
        """this function check if the move is valid.
        receive coordinate and check if the place is in the board.
        True - if the move is valid.
        False - if the move is not valid."""
        x, y = coordinate
        if x < 0 or x > self.board.rows - 1 or y < 0 or y >= self.board.columns:
            return False
        return True

    def first_check(self, coordinate: Coordinates) -> list[Coordinates]:
        """this is the first check for the possible moves of the piece.
        the function receive a coordinate of a piece and check the possible move according to the rules.
        this function check if the 6 directions in this game is empty if it is, save this coordinate
        else continue to check the diagonal direction for legal jump.
        return a list of the possible moves for the piece in the board.
        """
        x, y = coordinate
        possible_moves_step = []

        # define the six directions of movement
        directions = [
            (-1, -1),  # Diagonal up-left
            (-1, 1),  # Diagonal up-right
            (0, 2),  # Right
            (1, 1),  # Diagonal down-right
            (1, -1),  # Diagonal down-left
            (0, -2),  # Left
        ]

        for dx, dy in directions:  # create a coordinate for each direction
            adj_cord = (x + dx, y + dy)
            jump_cord = (x + 2 * dx, y + 2 * dy)

            if self.coordinate_in_board(adj_cord) and self.board.get_value(adj_cord) == -2:
                # if the adjacent space is empty, add it as a possible move
                possible_moves_step.append(adj_cord)
            elif self.coordinate_in_board(adj_cord) and self.board.get_value(adj_cord) not in [-1, -2]:
                # if there's a piece in the adjacent space, check for a legal jump
                if self.coordinate_in_board(jump_cord) and self.board.get_value(jump_cord) == -2:
                    jump_moves = self.check_jump(jump_cord)  # check for legal jumps
                    possible_moves_step = possible_moves_step + jump_moves  # add the legal jumps to the possible moves

        return possible_moves_step

    def check_jump(self, coordinate: Coordinates) -> list[Coordinates]:
        """this function check if the coordinate is empty and if it is, save this coordinate,
        else continue to check the diagonal direction for legal jump"""
        possible_move = []
        x, y = coordinate
        if self.coordinate_in_board((x, y)) and self.board.get_value((x, y)) == -2:  # if the place is empty
            possible_move.append((x, y))  # add the coordinate to the possible moves
            diagonal_moves = self.check_diagonal_empty((x, y))  # check for legal jumps
            possible_move = possible_move + diagonal_moves
        return possible_move

    def check_diagonal_empty(self, coordinate: Coordinates, coords_list=None, visited=None) -> list[Coordinates]:
        """
        this function is the helper for the check_jump function.
        its check if there is more jumps do to and if it is - add it to coord list that
        represent the previous list of possible moves.
        visited is a set that contain the cords that already checked.
        """
        if coords_list is None:
            coords_list = []
        if visited is None:
            visited = set()

        x, y = coordinate
        # add current coordinate to visited set
        visited.add((x, y))

        directions = [(-2, -2), (-2, 2), (2, 2), (2, -2), (0, 4), (0, -4)]
        # define the six directions of movement(jumps)
        for dx, dy in directions:
            next_cord = (x + dx, y + dy)
            prev_cord = (x + dx // 2, (y + dy // 2))
            if next_cord not in visited:
                if self.coordinate_in_board(prev_cord) and self.board.get_value(prev_cord) not in [-1, -2]:
                    # if there is a piece in prev
                    if self.coordinate_in_board(next_cord) and self.board.get_value(next_cord) == -2:
                        # if the jump cord are empty -> possible moves
                        coords_list.append(next_cord)
                        self.check_diagonal_empty(next_cord, coords_list, visited)

        return coords_list

    def dict_possible_moves(self, current_piece: Piece) -> Dict[str, Coordinates]:
        """
        this function return a possible move dict to the piece receive order by letters.
        """
        possible_moves = self.first_check(current_piece.get_coordinate())
        possible_moves_dict = {}
        for i, value in enumerate(possible_moves, start=ord('a')):
            possible_moves_dict[chr(i)] = value
        return possible_moves_dict

    def choose_move_turn(self, possible_moves_dict: Dict[str, Coordinates], num_piece: int) -> None:
        """this function ask the local player to choose a letter to move the piece and move the piece to this place.
        receive the possible moves of the piece and the number of the piece that the player wants to move,
        if the input is not in the possible moves, the function ask the player to choose again.
        else, move the piece to the new coordinate"""
        x = True
        while x:
            place_letter = input("Please choose a place to move the piece")
            if place_letter.upper() == "EXIT":
                close_log_file()
                raise ExitGameException
            if place_letter in possible_moves_dict.keys():
                self.board.clean_place(self.players[self.current_turn_p - 1].pieces[num_piece].get_coordinate())
                # remove the piece from the board
                for letter in possible_moves_dict.keys():
                    self.board.clean_place(possible_moves_dict[letter])  # remove the letter places from the board
                self.players[self.current_turn_p - 1].pieces[num_piece].change_coordinate(
                    possible_moves_dict[place_letter])  # change the coordinate of the piece to the new place
                log_game_event("Move", player=self.current_turn_p, piece=num_piece,
                               coordinates=possible_moves_dict[place_letter])
                x = False
            else:
                print(
                    "The letter you chose is not in the possible moves, please choose a letter"
                    " from the possible moves.")

    def move_piece(self, possible_moves: Dict[str, Coordinates], piece: int, new_cord: Coordinates,
                   prev_cord: Coordinates) -> None:
        """this function - move piece for the computer.
        this function move the piece to the new coordinate and remove the piece from the previous coordinate.
        receive the possible moves of the piece, the piece that the computer wants to move,
         the new coordinate of the piece that the computer chose,
        and the previous coordinate of the piece.
        """
        self.board.clean_place(prev_cord)
        # remove the piece from the board
        for letter in possible_moves.keys():
            self.board.clean_place(possible_moves[letter])  # remove the letter places from the board
        self.players[self.current_turn_p - 1].pieces[piece].change_coordinate(new_cord)
        log_game_event("Move", player=self.current_turn_p, piece=piece, coordinates=new_cord)
        #  logging.info(f"Player {self.players[self.current_turn_p - 1].name} moved piece {piece} to {new_cord}.")

        # change the coordinate of the piece to the new place

    def move_piece_load(self, cur_player: int, piece: int, new_cord: Coordinates) -> None:
        """this function - move piece for the loading game.
        move it by changing the coordinate of the piece and remove the piece from the previous coordinate.
        without print the board
        """
        self.current_turn_p = cur_player
        prev_cord = self.players[self.current_turn_p - 1].get_coordinate_piece(piece)
        self.board.clean_place(prev_cord)
        self.players[self.current_turn_p - 1].pieces[piece].change_coordinate(new_cord)

    def is_winner(self, potential_winner: Player) -> bool:
        """receive a potential player and check if he is the winner - True if it is False if no"""
        for player in self.players:
            if player == potential_winner:
                for piece in player.pieces.values():
                    if piece.get_coordinate() not in winning_coordinates[len(self.players)][self.current_turn_p - 1]:
                        return False
                return True
        return False

    def is_game_finished(self) -> bool:
        """this function check if the game is finished.
        return True if the game is finished.
        return False if the game is not finished."""
        if self.winner is not None:
            return True
        return False


def close_log_file():
    """
    this function close the log file of the game.
    """
    logging.shutdown()
    handlers = logging.root.handlers[:]
    for handler in handlers:
        handler.close()
        logging.root.removeHandler(handler)


def log_game_event(event, player=None, piece=None, coordinates=None):
    """this function add a log to the game log file with the event, player, piece and coordinates."""
    # build the custom message format
    parts = [event, f"Player: {player}" if player else "",
             f"Piece: {piece}" if piece in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] else "",
             f"Coordinates: {coordinates}" if coordinates else ""]
    message = " | ".join(part for part in parts if part)  # join the parts with a separator
    logging.info(message)
