import random

WINNING_LINES = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],   # 3 rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],   # 3 columns
    [0, 4, 8], [2, 4, 6],              # 2 diagonals
]

def create_board():
    """Return a new empty board (9 spaces)."""
    return [" "] * 9


def show_board(board):
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()

def get_move(board, player_name, mark):
    while True:
        text = input(f"{player_name} ({mark}), choose a cell (1-9): ").strip()
 
        # Check 1: empty input
        if text == "":
            print("You didn't type anything. Please enter a number from 1 to 9.")
            continue
 
        # Check 2: not a number (try/except catches the error)
        try:
            number = int(text)
        except ValueError:
            print("That is not a number. Please enter a number from 1 to 9.")
            continue
 
        # Check 3: number out of range
        if number < 1 or number > 9:
            print("That number is out of range. Please choose from 1 to 9.")
            continue
 
        # Check 4: cell already taken
        index = number - 1
        if board[index] != " ":
            print("That cell is already taken. Choose another one.")
            continue
 
        return index
 
 
def computer_move(board):
    """The computer picks a random empty cell. Returns the board index (0-8)."""
    empty_cells = []
    for i in range(9):
        if board[i] == " ":
            empty_cells.append(i)
    return random.choice(empty_cells)
 
 
def check_winner(board, mark):
    """Return True if this mark has completed a row, column or diagonal."""
    for line in WINNING_LINES:
        if board[line[0]] == mark and board[line[1]] == mark and board[line[2]] == mark:
            return True
    return False
 
 
def is_draw(board):
    """Return True if every cell is filled (no empty spaces left)."""
    return " " not in board
 
 
def choose_mode():
    """Ask if the game is 2-player or vs the computer. Returns 1 or 2."""
    print("\n1. Two players")
    print("2. Play against the Computer")
    while True:
        text = input("Choose a mode (1 or 2): ").strip()
        if text == "1" or text == "2":
            return int(text)
        print("Please type 1 or 2.")
 
 
def play_game(scores, names):
    """
    Play one full game. Updates the scores dictionary.
    names = [name of the X player, name of the O player]
    """
    board = create_board()
    marks = ["X", "O"]
    turn = 0                     
 
    print("\nCell numbers:")
    show_board(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
 
    while True:
        name = names[turn]
        mark = marks[turn]
        print(f"--- It is {name}'s turn ({mark}) ---")
        show_board(board)
 
        if name == "Computer":
            index = computer_move(board)
            print(f"Computer chooses cell {index + 1}.")
        else:
            index = get_move(board, name, mark)
        board[index] = mark
 
        if check_winner(board, mark):
            show_board(board)
            print(f"*** {name} ({mark}) wins! Congratulations! ***")
            scores[name] += 1
            return
 
        if is_draw(board):
            show_board(board)
            print("*** It's a draw! ***")
            scores["Draws"] += 1
            return
 
        turn = 1 - turn           
 
 
def ask_play_again():
    while True:
        answer = input("Play again? (yes/no): ").strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("Please type yes or no.")
 
 
def show_scores(scores, names):
    print("\n----- SCORE -----")
    print(f"{names[0]} (X): {scores[names[0]]}")
    print(f"{names[1]} (O): {scores[names[1]]}")
    print(f"Draws: {scores['Draws']}")
    print("-----------------")
 
 
def main():
    print("=" * 30)
    print("      TIC-TAC-TOE")
    print("=" * 30)
 
    mode = choose_mode()
    if mode == 1:
        names = ["Player 1", "Player 2"]
    else:
        names = ["Player 1", "Computer"]
 
    scores = {names[0]: 0, names[1]: 0, "Draws": 0}
 
    while True:
        play_game(scores, names)
        show_scores(scores, names)
        if not ask_play_again():
            print("\nThanks for playing! Goodbye!")
            break
 
 
main()
 