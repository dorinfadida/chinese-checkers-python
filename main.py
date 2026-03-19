from game import *
from helper import *
from chinese_checkers import App
import load_game
import argparse


def choose_players_to_play() -> int:
    """the function ask the user how many players are playing and return the number of players."""
    while True:
        num_plays = input("How many num_players are playing? (2,3,4,6)")
        if num_plays in ["2", "3", "4", "6"]:
            break
        else:
            print("The number of players should be 2,3,4 or 6")
    return int(num_plays)


def computers_players() -> int:
    """the function ask the user how many computers he wants to play against and return the number of computers."""
    while True:
        num_computers = input("How many computers you want to play against? (1,2,3,5)")
        if num_computers in ["1", "2", "3", "5"]:
            return int(num_computers)
        else:
            print("The number of players should be 1,2,3 or 5")


def against_who() -> str:
    """the function ask the user if he wants to play against the computer or against other players."""
    while True:
        game_type = input(
            "Do you want to play against a standard computer, a smart computer, or with friends? ("
            "computer/smart/friends)").lower()
        if game_type == "computer":
            print("The computer is not ready yet.")
            return game_type
        elif game_type == "friends":
            print("Let's get the players name!")
            return game_type
        elif game_type == "smart":
            print("The smart computer is not ready yet.")
            return game_type
        else:
            print("Please enter computer or players or smart")


def single_player(num_plays: int, all_players: dict[str, Player]) -> list[Player]:
    """the function add the player to the current game - for the case of playing against the computer (
    one_local_player).
    nam_play : the number of players in the game.
    all_players : the all-time players in the app."""
    game_players_dict = {}
    if all_players == {}:  # if no one ever played the game
        name = input("What is your player name?")
        flag = False
        while not flag:
            if not name.strip():  # if the name is empty
                print("Name cannot be empty")
                name = input("What is your player name?")
            if not name.isascii():  # if the name is not in ascii
                print("Name can include only english, digits and sign.")
                name = input("What is your player name?")
            else:
                flag = True
        game_players_dict[name] = Player(name)  # create a new player and add it to the game
        all_players[name] = game_players_dict[name]  # add the player to the all-time players
        print(f"{name} added successfully to the app and this game!")
    else:  # if there are already players in the app
        name = input("What is your player name?")
        if name in all_players.keys():
            # if the player is already in the app
            print("hello again!")
            game_players_dict[name] = all_players[name]
            print(f"{name} added successfully the game!")
        elif name not in all_players.keys():
            game_players_dict[name] = Player(name)  # create a new player and add it to the game
            all_players[name] = game_players_dict[name]  # add the player to the all-time players
            print(f"{name} added successfully to the app and this game!")
            print("Let's start the game!")
    for i in range(num_plays):  # add the computers to the game
        name_c = "computer"
        game_players_dict[str(i + 1)] = Player(name_c + str(i + 1))
    return list(game_players_dict.values())  # return the list of the players in the game


def local_p_in_game(num_players: int, all_players: dict[str, Player]) -> list[Player]:
    """the function add the players to the current game - for the case of playing against other players.(local)
    num_players : the number of players in the game.
    all_players : the all-time players in the app."""
    game_players_dict = {}
    for player_index in range(num_players):
        while True:  # until a valid name is provided and processed.
            name = input(f"Player {player_index + 1}: What is the player name? ").strip()
            if not name:  # check if the name is empty
                print("Name cannot be empty.")
                continue
            if not name.isascii():  # check if the name is not in ASCII
                print("Name can include only English, digits, and signs.")
                continue
            if name in game_players_dict:
                print("Player already signed to the current game.")
                continue
            # check if the player is already in the app
            if name in all_players:
                print("Hello again!")
                player = all_players[name]  # get the existing player object
            else:
                # if it's a new player, create a new Player instance
                player = Player(name)
                all_players[name] = player  # add the player to the all-time players
            # add the player to the current game's dictionary
            game_players_dict[name] = player
            print(f"{name} added successfully to this game!")
            break  # Exit the loop since a valid name was processed

    return list(game_players_dict.values())  # return the list of the players in the game


def print_list_players(players: list[Player]) -> None:
    """this function print the list of the players in the game."""
    print("The players in the game are:")
    index_player = 1
    for player in players:
        print(f"Player{index_player} is " + player.name)
        index_player += 1


def show_welcome_message() -> None:
    """
    the main menu options of the game.
    """
    print("Select an option:")
    print("1. Rules")
    print("2. Start New Game")
    print("3. All-Time Players")
    print("4. Winning Table")
    print("5. Load Game")
    print("6. Exit")


def show_rules() -> None:
    """
    1 - the rules of the game.
    """
    print(rules)


def start_new_game() -> None:
    """
    2 - the function start a new game - according to the user choice..
    """
    against = against_who()  # ask the user against who he wants to play
    # according to the user choice, the function will add the players to the game
    if against == "friends":
        num_players = choose_players_to_play()
        players_cur_game = local_p_in_game(num_players, ChineseCheckers.all_time_players)
        print_list_players(players_cur_game)
        print("Let's start the game!")
        ChineseCheckers.start_new_game(players_cur_game, against)
    elif against == "computer":
        players_cur_game = single_player(computers_players(), ChineseCheckers.all_time_players)
        print("Let's start the game!")
        ChineseCheckers.start_new_game(players_cur_game, against)
    elif against == "smart":
        players_cur_game = single_player(1, ChineseCheckers.all_time_players)
        print("Let's start the game!")
        ChineseCheckers.start_new_game(players_cur_game, against)


def show_all_time_players(dict_players: dict[str, Player]) -> None:
    """
    3 - the function print the all-time players in the app.
    dict_players : the all-time players in the app.
    """
    print("All-Time Players:")
    if dict_players == {}:
        print("No players in the app yet.")
    else:
        for name, player in dict_players.items():
            print(f"Player_name: {name} | Wins: {player.num_of_winning} | Losses: {player.num_of_losses}")


def show_winning_table(ChineseCheckersApp: App) -> None:
    """
    4 - the function print the winning table of the players.
    ChineseCheckersApp : the app object.
    """
    print("Winning Table:")
    if not ChineseCheckersApp.winners:
        print("No winners yet.")
    else:
        for player in ChineseCheckersApp.winners:
            print(f"Player: {player.name} | Wins: {player.num_of_winning} | Losses: {player.num_of_losses}")


def load_file_game() -> None:
    """
    5 - the function load a saved game.
    there is a few options to load a game:
    1. load a game that already finished and then the user will see the course of the game.
    2. load a game that is not finished yet and then the user will continue the game.
    3. something went wrong and the game is not loaded -> back to main menu.
    """
    file_name = input("Enter the name of the file to load: ")
    print("Loading a saved game...")
    load_game.load_game(file_name)


def main_menu(ChineseCheckersApp) -> None:
    """
    the main menu of the game - start the app.
    """

    while True:
        show_welcome_message()
        choice = input("Enter your choice (1-6): ")

        try:
            if choice == '1':
                show_rules()
            elif choice == '2':
                start_new_game()
            elif choice == '3':
                show_all_time_players(ChineseCheckersApp.all_time_players)
            elif choice == '4':
                show_winning_table(ChineseCheckersApp)
            elif choice == '5':
                load_file_game()
            elif choice == '6':
                print("Thank you for playing. Goodbye!")
                ChineseCheckersApp.save_all_time_players()  # save the all-time players to a json file
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except ExitGameException:  # if the user wants to exit the game
            print("Returning to main menu...")
            continue

        input("Press Enter to continue...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This is a Chinese Checkers game. You can play against the computer or with friends. You can also "
                    "load a saved game.")
    args = parser.parse_args()
    ChineseCheckers = App()
    print("WELCOME TO THE CHINESE CHECKERS GAME!")
    main_menu(ChineseCheckers)
