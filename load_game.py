import helper
from player import Player
import re
from game import Game
from typing import Tuple, Optional, Any, List, Dict


def find_winner_name(file_name: str) -> Tuple[Optional[bool], Optional[str]]:
    """check if the file game that want to be load is end or in the middle of the game.
    if the game is end, return True and the winner name.
    if the game is in the middle, return False and None.
    if the file is not a game file, return None and None."""
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()  # Read all lines into a list
    except FileNotFoundError:
        print("File not found.")
        return None, None
    if not lines:  # Check if the list is empty
        return None, None
    last_line = lines[-1]  # Get the last line
    winner_search = re.search(r'Winner \| Player: (\w+)', last_line)
    if winner_search:
        return True, winner_search.group(1)
    else:
        return False, None


def load_players(name_file: str) -> Tuple[Optional[Any], int, Optional[List[Dict]]]:
    """Load the players from the file and return them as a list of dictionaries.
    Each dictionary contains the player's number, name, and color.
    If the file is not found, return None.
    If the file is not a game file, return None.
    If the game is against the computer or friends,
    return the game opponent and the number of players and list of players.
    """
    try:
        with open(name_file, 'r', encoding='utf-8') as file:
            contents = file.read()
    except FileNotFoundError:
        print("File not found.")
        return 0, 0, None
    else:
        sentence_count = contents.count('\n')
        if sentence_count < 4:
            print("this file is not a game file")
            return 0, 0, None

    # extract the game opponent
    game_against_search = re.search(r'Game against (\w+)', contents)
    if game_against_search:
        game_against = game_against_search.group(1)
        # Check if the opponent is either "Computer" or "Friends"
        if game_against not in ["Computer", "Friends", "Smart"]:
            return 0, 0, None
    else:
        game_against = 0

    # Extract the number of players
    num_players_search = re.search(r'num players: (\d+)', contents)
    num_players = int(num_players_search.group(1)) if num_players_search else 0
    # if no match found, return 0

    # Extract player information
    player_info_pattern = re.compile(r'player_num: (\d+) player_name: (\w+) player_color: (\w+)')
    players_info = player_info_pattern.findall(contents)  # if no match found, return an empty list

    # Format player information into a list of dictionaries
    players = [{'player_num': int(num), 'player_name': name, 'player_color': color} for num, name, color in
               players_info]

    return game_against, num_players, players


def pre_game_load(num_players: int, players_file: List[Any]) -> Optional[List[Player]]:
    """Load the players on game and return them as a list of players.
    If the game is against the computer or friends, return the list of players.
    otherwise return None."""

    players_cur_game = []
    cur_game_cords = helper.players_in_game[num_players]
    for play in players_file:
        players_cur_game.append(Player(play['player_name']))
        players_cur_game[-1].set_player(play['player_color'], cur_game_cords[play['player_num'] - 1])
    return players_cur_game


def load_moves(file_name: str, num_players: int) -> Optional[List]:
    """load the moves from the file and return them as a list of moves.
    file name: the name of the file.
    num_players: the number of players in the game."""
    move_pattern = re.compile(r'Move \| Player: (\d+) \| Piece: (\d+) \| Coordinates: \((\d+), (\d+)\)')
    moves = []
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                match = move_pattern.search(line)
                if match:
                    player = match.group(1)
                    if int(player) > num_players:
                        print("Invalid player number.")
                        return None
                    piece = match.group(2)
                    coordinates = (int(match.group(3)), int(match.group(4)))
                    moves.append({'player': player, 'piece': piece, 'coordinates': coordinates})
    except FileNotFoundError:
        print("File not found.")
        return None
    return moves


def watch_game(players, moves) -> None:
    """Watch a game that was loaded from a file - print the board after each move.
    this for a game that was finished."""
    game = Game(players)
    game.board.print_board(players)  # print the board on start
    for move in moves:
        num_player = int(move['player'])
        player = players[int(move['player']) - 1]
        piece = int(move['piece'])
        coordinates = move['coordinates']
        game.move_piece_load(num_player, piece, coordinates)
        print(f"Player: {player.get_name()} | Piece: {piece} | Coordinates: {coordinates}")
        game.board.print_board(players)  # print the board after each move


def continue_game(game_against: Any, players: List[Player], moves: List) -> None:
    """
    Continue a game that was loaded from a file.
    """
    game = Game(players)  # Create a new game
    for move in moves:
        num_player = int(move['player'])
        piece = int(move['piece'])
        coordinates = move['coordinates']
        game.move_piece_load(num_player, piece, coordinates)
    game.add_current_turn_p()
    # now after loading - continue to play
    if game_against == "Computer":
        game.game_with_computer(game.computer_turn)
    elif game_against == "Friends":
        game.local_game()
    elif game_against == "Smart":
        game.game_with_computer(game.smart_turn)
    game.board.print_board(players)  # print the board after each move


def load_game(file_name: str) -> None:
    """Load a game from a file.
    If the game is finished, print every move of the game and print the winner.
    If the game is not finished, continue the game from the last move.
    If the file is not found, print an error message.
    If the file is not a game file, print an error message.
    """
    game_against, num_players, players = load_players(file_name)
    if game_against == 0 or num_players == 0 or not players:
        print("this file is not a game file")
        return
    is_winner, winner = find_winner_name(file_name)
    if is_winner:
        # a finished game - now we need to load the game
        players_type = pre_game_load(num_players, players)
        moves = load_moves(file_name, num_players)
        watch_game(players_type, moves)
        print("The Winner was: ", winner)
    elif is_winner is False:
        players_type = pre_game_load(num_players, players)
        moves = load_moves(file_name, num_players)
        if players_type is not None and moves is not None:
            continue_game(game_against, players_type, moves)
    else:
        print("this file is not a game file")
