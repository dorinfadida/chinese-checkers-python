from game import *
from typing import List, Dict
import json


class App:
    """
    This class is the main class of the game. It is responsible for starting a new game, saving the winners and
    loading the all-time players.

    Attributes:
    winners: a list of the winners of the game
    all_time_players: a dictionary of all the players that played the game

    Methods:
    start_new_game: starts a new game
    set_winners: sets the winners of the game
    load_all_time_players: loads the all-time players
    save_all_time_players: saves the all-time players

    """

    def __init__(self) -> None:
        self.winners: List[Player] = []
        self.all_time_players: Dict[str, Player] = {}
        self.load_all_time_players()
        self.set_winners()

    def start_new_game(self, players: list[Player], type_of_game: str) -> None:
        """
        This method starts a new game.
        :param players: a list of players
        :param type_of_game: the type of the game
        """
        winner = None
        new_game = Game(players)  # create a new game
        if type_of_game == "friends":  # if the game is against friends
            winner = new_game.pre_game(type_of_game)
        elif type_of_game == "computer":  # if the game is against the computer
            winner = new_game.pre_game(type_of_game)  # if the game is against the computer
        elif type_of_game == "smart":  # if the game is a loaded game
            winner = new_game.pre_game(type_of_game)
        if winner is not None and winner != "EXIT":
            # if there is a winner and it is the computer or exit the game
            if winner not in self.winners:
                self.winners.append(winner)

    def set_winners(self) -> None:
        """
        This method sets the winners of the game when the object is created.
        the winners take from the all_time_players dictionary.
        """
        if self.all_time_players == {}:
            self.winners = []
        else:
            for player in self.all_time_players.values():
                if player.num_of_winning > 0:
                    self.winners.append(player)

    def load_all_time_players(self) -> None:
        """
        This method loads the all-time players from a file.
        and creates a dictionary of all the players that played the game.
        """
        try:
            with open('all_time_players.json', 'r') as file:
                dict_players = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.all_time_players = {}
            return
        for name, player in dict_players.items():
            try:
                name = str(name)
                wins = int(player[0])
                losses = int(player[1])
                if wins < 0 or losses < 0:
                    raise ValueError("Negative wins or losses not allowed.")
            except (ValueError, KeyError):
                print("File is not match the required file.")
                continue  # Skip this player and continue with the next

            self.all_time_players[name] = Player(name, player[0], player[1])

    def save_all_time_players(self) -> None:
        """
        This method saves the all-time players to a file.
        """
        dict_players = {}
        for name, player in self.all_time_players.items():
            dict_players[name] = [player.num_of_winning, player.num_of_losses]
        with open('all_time_players.json', 'w') as file:
            json.dump(dict_players, file)
