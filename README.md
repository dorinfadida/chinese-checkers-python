# Chinese Checkers Game 🎮

A terminal-based Chinese Checkers game written in Python, designed using Object-Oriented Programming (OOP) principles.

The project includes multiple game modes, persistent player statistics, and a game replay/load system.

This project was developed as part of an introductory programming course during my first year of Computer Science studies.

## 🚀 Features

### 🧠 Smart Computer Opponent
- Includes a rule-based (heuristic) computer player
- Chooses moves based on:
  - advancing toward the winning area
  - preferring more central board positions

---

### 👥 Multiple Game Modes
- Supports 2, 3, 4, or 6 players
- Can be played against:
  - friends (local multiplayer)
  - a basic computer opponent (random moves)
  - a smart computer opponent (heuristic-based)

---

### 💾 Persistent Player Statistics
- Stores all-time player data in JSON
- Tracks wins and losses across games
- Automatically loads and saves player data

---

### 🏆 Winning Table
- Displays players who have won games
- Shows cumulative performance over time

---

### 🎨 Colored Terminal Board
- Uses `colorama` for colored output
- Improves readability of the board in the terminal

---

### 🔁 Game Logging and Replay
- Saves game activity into log files
- Supports:
  - replaying completed games
  - continuing unfinished games from saved logs

---

### 🔍 Type Checking
- Uses type hints and `mypy`

---

## 🏗️ Project Structure

main.py                # Entry point and menu system  
game.py                # Core game logic  
board.py               # Board representation  
player.py              # Player model  
piece.py               # Piece model  
helper.py              # Constants and utilities  
load_game.py           # Load & replay games  
chinese_checkers.py    # Application controller  
requirements.txt       # Dependencies  

---

## ⚙️ Installation

pip install -r requirements.txt

---

## ▶️ Run the Game

python main.py

---

## 💡 Technical Highlights

- Object-Oriented design (`Game`, `Board`, `Player`, `Piece`)
- Non-trivial move generation logic (including jumps)
- Recursive logic for chained moves
- JSON-based persistence for player statistics
- Log parsing and replay system
- Clear separation between components

---

## 🔮 Future Improvements

- Refine the object-oriented design to improve modularity and maintainability
- Strengthen the separation between game logic, user interaction, and data persistence
- Improve the heuristic used by the computer player
- Add unit tests for core game mechanics and move validation

---

## 👩‍💻 Author

**Dorin Fadida**  
Computer Science Student  
Hebrew University of Jerusalem