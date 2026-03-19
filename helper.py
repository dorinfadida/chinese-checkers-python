"""helper for chinese checkers"""

# empty board:
empty_board = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, -1, -2, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -2, -1, -2, -1, -2, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1],
               [-2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2],
               [-1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1],
               [-1, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -1],
               [-1, -1, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -1, -1],
               [-1, -1, -1, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -1, -1, -1],
               [-1, -1, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -1, -1],
               [-1, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -1],
               [-1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1],
               [-2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2, -1, -2],
               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -2, -1, -2, -1, -2, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, -1, -2, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

# the coordinate for each player for each game.
player1_coordinates = [(16, 12), (15, 11), (15, 13), (14, 10), (14, 12), (14, 14), (13, 9), (13, 11), (13, 13),
                       (13, 15)]
player2_coordinates = [(0, 12), (1, 11), (1, 13), (2, 10), (2, 12), (2, 14), (3, 9), (3, 11), (3, 13), (3, 15)]
player3_coordinates = [(4, 0), (4, 2), (4, 4), (4, 6), (5, 1), (5, 3), (5, 5), (6, 2), (6, 4), (7, 3)]
player4_coordinates = [(4, 18), (4, 20), (4, 22), (4, 24), (5, 19), (5, 21), (5, 23), (6, 20), (6, 22), (7, 21)]
player5_coordinates = [(12, 0), (12, 2), (12, 4), (12, 6), (11, 1), (11, 3), (11, 5), (10, 2), (10, 4), (9, 3)]
player6_coordinates = [(12, 18), (12, 20), (12, 22), (12, 24), (11, 19), (11, 21), (11, 23), (10, 20), (10, 22),
                       (9, 21)]

# dictionary of player location.
coordinates_map = {
    1: player1_coordinates,
    2: player2_coordinates,
    3: player3_coordinates,
    4: player4_coordinates,
    5: player5_coordinates,
    6: player6_coordinates,
}

# dictionary of player coordinates for each num of players in game.
players_in_game = {
    2: [player1_coordinates, player2_coordinates],
    3: [player1_coordinates, player3_coordinates, player4_coordinates],
    4: [player3_coordinates, player4_coordinates, player6_coordinates, player5_coordinates],
    6: [player1_coordinates, player5_coordinates, player3_coordinates, player2_coordinates, player4_coordinates,
        player6_coordinates]
}

# coordinates for winning for each player.
winning_coordinates = {
    2: [player2_coordinates, player1_coordinates],
    3: [player2_coordinates, player6_coordinates, player5_coordinates],
    4: [player6_coordinates, player5_coordinates, player3_coordinates, player4_coordinates],
    6: [player2_coordinates, player4_coordinates, player6_coordinates, player1_coordinates, player5_coordinates,
        player3_coordinates]}

"""for 2 players game: player1 and player2
for 3 players game: player1,player3 and player4
for 4 players game: player3,player4, player5, player6
for 6 players game: player1  -  player6"""

colors = ["RED", "BLUE", "YELLOW", "GREEN", "MAGENTA", "CYAN"]
color_codes = {"RED": "\033[91m", "BLUE": "\033[94m", "YELLOW": "\033[93m", "GREEN": "\033[92m", "MAGENTA": "\033[95m",
               "CYAN": "\033[96m"}


EMPTY = -2
OUTSIDE_GAME = -1

rules = """

Game Rules:
Gameplay: Chinese Checkers is a strategic board game for 2, 3, 4, or 6 players.\nThe goal of each player is to move all 
their game pieces to the opposite side of the star on the game board.

- Each player begins with 10 pieces at the start of the game.
- Players take turns in a round-robin fashion, moving one piece per turn. \nDuring a turn, the player selects a piece to
 move, and the board displays possible movement locations marked with letters a-z.\n The player must choose one of these
  letters for the move.
- Pieces can either move to an adjacent open spot in one of 6 directions or jump over other pieces.
- The winner is the first player to relocate all their pieces to the triangle directly opposite their starting position.
\n The game ends immediately, marking losses for the remaining players.

Menu Options:
1. Rules - Return to this screen to view the game rules.
2. Start New Game - Options include starting a new game against the computer,\n a local game with 2, 3, 4, or 6 players,
 or against 1, 2, 4, 5 computer players or smart computer against one computer.
3. All-Time Players - Displays all players who have ever played the game.
4. Winning Table - Shows a table of all-time winners.
5. Load Game - Load from a log file or a game that was either finished or paused.
6. Exit - Exit the game.

Additional Note:
- If you are in the middle of a game and wish to return to the main menu,\n you can do so by typing "EXIT".

"""
