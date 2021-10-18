import os

#global variables
SIZE = 5
EMPTY_SPACE = "O"
SHIP_PLACED = "X"

# clears the screen
def console_clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#function generates basic board
def generate_board():
    return [[EMPTY_SPACE] * SIZE for _ in range(SIZE)]

#prints 5x5 board without borders
def print_board(board):
    board = generate_board()
    row_letter_ascii = 97
    for i in range(SIZE):
        print(f"   {i + 1}", end="")

    for i in range(SIZE):
        print(f"\n{chr(row_letter_ascii + i).upper()} ", end="")

        for j in range(len(board[i])):
            print(f" {board[i][j]}", end=" ")
            if j != len(board[i]):
                print(" ", end="")
        if i != SIZE - 1:
            print("\n", end="")

print(print_board(SIZE))