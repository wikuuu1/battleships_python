import os

#global variables
SIZE = 5
EMPTY_SPACE = "O"
SHIP_PLACED = "X"
SHIPS_TO_PLACE = 6

# clears the screen
def console_clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#function generates basic board
def generate_board():
    return [[EMPTY_SPACE] * SIZE for _ in range(SIZE)]

BOARD = generate_board()


#prints 5x5 board without borders
def print_board():
    row_letter_ascii = 97
    for i in range(SIZE):
        print(f"   {i + 1}", end="")

    for i in range(SIZE):
        print(f"\n{chr(row_letter_ascii + i).upper()} ", end="")

        for j in range(len(BOARD[i])):
            print(f" {BOARD[i][j]}", end=" ")
            if j != len(BOARD[i]):
                print(" ", end="")
        if i != SIZE - 1:
            print("\n", end="")
    print("\n")


# validates user's input's format
def validate_format(user_input):
    # Change to range(2,4) for custom board size
    if len(user_input) in range(2,3) and user_input[1].isdigit() and user_input[0].isalpha():
        if (ord(user_input[0].lower()) - 97) <= len(BOARD) - 1:
            if int(user_input[1]) <= len(BOARD):
                return True
    else:
        return False

    # second_index = int(user_move[1:])
    # print(second_index)

# checks if ships aren't too close
def ships_too_close(board, row, col):
    if board[row - 1][col] == SHIP_PLACED and not row == 0:
        return True
    if board[row][col - 1] == SHIP_PLACED and not col == 0:
        return True
    if col + 1 < SIZE:
        if board[row][col + 1] == SHIP_PLACED and not col == 4:
            return True
    if row + 1 < SIZE:
        if board[row + 1][col] == SHIP_PLACED and not row == 4:
            return True
    return False

def get_direction_for_size_two_ship(row, col, direction):
    while True:
        direction = input("Please choose direction(up/down/left/right): ")
        if direction == "up" and not row == 0:
            if not ships_too_close(BOARD, row - 1, col):
                return row - 1, col, direction
        if direction == "down" and not row == 4:
            if not ships_too_close(BOARD, row + 1, col):
                return row + 1, col, direction
        if direction == "right" and not col == 4:
            if not ships_too_close(BOARD, row, col + 1):
                return row, col + 1, direction
        if direction == "left" and not col == 0:
            if not ships_too_close(BOARD, row, col - 1):
                return row, col - 1, direction
        else:
            print("INVALID INPUT")
            continue

# takes user input and checks its validity
def get_move():

    while True:
        direction = None
        user_move = input("Please give your coordinates: ")
        if validate_format(user_move):
            row = ord(user_move[0].lower()) - 97
            col = int(user_move[1]) - 1
            lenght_of_board = len(BOARD)
            if not row <= lenght_of_board and not col <= lenght_of_board:
                print("Invalid input")
                continue
            if SHIPS_TO_PLACE > 3 and not ships_too_close(BOARD, row, col):
                return get_direction_for_size_two_ship(row, col, direction)
            if ships_too_close(BOARD, row, col):
                print("Ships are too close!")
                continue
            else:
                return row, col, direction
        else:
            print("Wrong coordinates format")

# marks user's choice of placement of the ships and returns marked board
def mark():
    global BOARD
    row, col, direction = get_move()
    if direction == None:
        BOARD[row][col] = SHIP_PLACED
    if direction == "up":
        BOARD[row][col] = SHIP_PLACED
        BOARD[row + 1][col] = SHIP_PLACED
    if direction == "down":
        BOARD[row][col] = SHIP_PLACED
        BOARD[row - 1][col] = SHIP_PLACED
    if direction == "right":
        BOARD[row][col] = SHIP_PLACED
        BOARD[row][col - 1] = SHIP_PLACED
    if direction == "left":
        BOARD[row][col] = SHIP_PLACED
        BOARD[row][col + 1] = SHIP_PLACED
    print_board()

def print_two_boards(empty_board_one, empty_board_two):

    print("Player 1                  Player 2\n")
    print("   ", end="")
    for i in range(SIZE):
        print(str(i + 1) + "   ", end="")
    print("      ", end="")
    for i in range(SIZE):
        print(str(i + 1) + "   ", end="")
    print()

    for i in range(SIZE):
        print(chr(97 + i ).upper() + "  ", end="")
        for j in range(SIZE):
            print(empty_board_one[i][j] + "   " , end="")
        print("   ", end="")
        print(chr(97 + i).upper() + "  ", end="")
        for j in range(SIZE):
            print(empty_board_two[i][j] + "   " , end="")
        print()
        print()

def play(empty_board_one, empty_board_two, player_one_board, player_two_board):
    while True:
        print_two_boards(empty_board_one, empty_board_two)
        user_input = input("Please give your coordinates: ")
        if validate_format(user_input):
            row = ord(user_input [0].lower()) - 97
            col = int(user_input [1]) - 1
            lenght_of_board = len(BOARD)
            if not row <= lenght_of_board and not col <= lenght_of_board:
                print("Invalid input")
                continue
        if player_two_board[row][col] == EMPTY_SPACE:
            empty_board_two[row][col] = "M"
        if player_two_board[row][col] == SHIP_PLACED:
            if ships_too_close(player_two_board, row, col):
                empty_board_two[row][col] = "H"
                player_two_board[row][col] = "H"
            else:
                empty_board_two[row][col] = "S"
                if empty_board_two[row - 1][col] == "H" and not row == 0:
                    empty_board_two[row - 1][col] = "S"
                if empty_board_two[row][col - 1] == "H" and not col == 0:
                    empty_board_two[row][col - 1] = "S"
                if col + 1 < SIZE:
                    if empty_board_two[row][col + 1] == "H" and not col == 4:
                        empty_board_two[row][col + 1] = "S"
                if row + 1 < SIZE:
                    if empty_board_two[row + 1][col] == "H" and not row == 4:
                        empty_board_two[row + 1][col] = "S"

        print_two_boards(empty_board_one, empty_board_two)

        user_input = input("Please give your coordinates: ")
        if validate_format(user_input):
            row = ord(user_input [0].lower()) - 97
            col = int(user_input [1]) - 1
            lenght_of_board = len(BOARD)
            if not row <= lenght_of_board and not col <= lenght_of_board:
                print("Invalid input")
                continue
        if player_one_board[row][col] == EMPTY_SPACE:
            empty_board_one[row][col] = "M"
        if player_one_board[row][col] == SHIP_PLACED:
            if ships_too_close(player_one_board, row, col):
                empty_board_one[row][col] = "H"
                player_one_board[row][col] = "H"
            else:
                empty_board_one[row][col] = "S"
                if empty_board_one[row - 1][col] == "H" and not row == 0:
                    empty_board_one[row - 1][col] = "S"
                if empty_board_one[row][col - 1] == "H" and not col == 0:
                    empty_board_one[row][col - 1] = "S"
                if col + 1 < SIZE:
                    if empty_board_one[row][col + 1] == "H" and not col == 4:
                        empty_board_one[row][col + 1] = "S"
                if row + 1 < SIZE:
                    if empty_board_one[row + 1][col] == "H" and not row == 4:
                        empty_board_one[row + 1][col] = "S"

        print_two_boards(empty_board_one, empty_board_two)

def place_ships():
    global BOARD
    global SHIPS_TO_PLACE
    print_board()
    while SHIPS_TO_PLACE > 0:
        mark()
        SHIPS_TO_PLACE -= 1
        print(SHIPS_TO_PLACE)

    player_one_board = BOARD
    BOARD = generate_board()
    SHIPS_TO_PLACE = 6
    print_board()

    while SHIPS_TO_PLACE > 0:
        mark()
        SHIPS_TO_PLACE -= 1
        print(SHIPS_TO_PLACE)
    player_two_board = BOARD

    empty_board_one  = generate_board()
    empty_board_two = generate_board()

    play(empty_board_one, empty_board_two, player_one_board, player_two_board)

def main():
    place_ships()


if __name__ == "__main__":
    main()
