import os
import time

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

# asks for direction and returns a second coordinate for two size ships
def get_direction_for_size_two_ship(row, col, direction):
    counter = 0
    while True:
        string = "Please choose direction:"
        if not row == 0:
            string += "\n--> (u)p "
        if not row == SIZE - 1:
            string += "\n--> (d)own "
        if not col == 0:
            string += "\n--> (l)eft "
        if not col == SIZE - 1:
            string += "\n--> (r)ight "
        print(string)
        direction = input().lower()
        if (direction == "up" or direction == "u") and not row == 0:
            if not ships_too_close(BOARD, row - 1, col):
                return row - 1, col, "up"
        if (direction == "down" or direction == "d") and not row == SIZE - 1:
            if not ships_too_close(BOARD, row + 1, col):
                return row + 1, col, "down"
        if (direction == "right" or direction == "r") and not col == SIZE - 1:
            if not ships_too_close(BOARD, row, col + 1):
                return row, col + 1, "right"
        if (direction == "left" or direction == "l") and not col == 0:
            if not ships_too_close(BOARD, row, col - 1):
                return row, col - 1, "left"
        else:
            counter += 1
            if counter == 5:
                console_clear()
                counter = 0
                print_board()
            print("Incorrect direction. Try again!")

            continue

def ask_for_coordinates():
    counter = 0
    while True:
        user_move = input("Please give your coordinates: ")
        if validate_format(user_move):
            row = ord(user_move[0].lower()) - 97
            col = int(user_move[1]) - 1
            lenght_of_board = len(BOARD)
            if not row <= lenght_of_board and not col <= lenght_of_board:
                print("Invalid input")
                continue
        else:
            # counter += 1
            # if counter == 5:
            #     console_clear()
            #     counter = 0
            #     print_board()
            print("Wrong coordinates format")
            continue

        return row, col

# takes user input and checks its validity
def place_ship():
    while True:
        direction = None
        row, col = ask_for_coordinates()
        if SHIPS_TO_PLACE > 3 and not ships_too_close(BOARD, row, col):
            return get_direction_for_size_two_ship(row, col, direction)
        if ships_too_close(BOARD, row, col):
            print("Ships are too close!")
            continue
        else:
            return row, col, direction

# marks user's choice of placement of the ships and returns marked board
def mark():
    global BOARD
    row, col, direction = place_ship()
    if direction == "up":
        BOARD[row + 1][col] = SHIP_PLACED
    if direction == "down":
        BOARD[row - 1][col] = SHIP_PLACED
    if direction == "right":
        BOARD[row][col - 1] = SHIP_PLACED
    if direction == "left":
        BOARD[row][col + 1] = SHIP_PLACED
    else:
        BOARD[row][col] = SHIP_PLACED
    console_clear()
    # print(f"\n       Player {player}\n")
    print_board()


# prints board for each player in shooting phase
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

def play(empty_board, player_board, player):
    while True:
        print(f"Player {player + 1}")
        row, col = ask_for_coordinates()
        if player_board[row][col] == "M" or player_board[row][col] == "S" or player_board[row][col] == "H":
                print(f"Player {player + 1} you already tried this shot!\n")
                continue
        if player_board[row][col] == EMPTY_SPACE:
            empty_board[row][col] = "M"
            console_clear()
            print(f"Player {player + 1} has missed!\n")
        if player_board[row][col] == SHIP_PLACED:
            if ships_too_close(player_board, row, col):
                empty_board[row][col] = "H"
                player_board[row][col] = "H"
                console_clear()
                print(f"Player {player + 1} has hit a ship!\n")
            else:
                empty_board[row][col] = "S"
                player_board[row][col] = "S"
                console_clear()
                print(f"Player {player + 1} has sunk a ship!\n")
                if empty_board[row - 1][col] == "H" and not row == 0:
                    empty_board[row - 1][col] = "S"
                    player_board[row - 1][col] = "S"
                if empty_board[row][col - 1] == "H" and not col == 0:
                    empty_board[row][col - 1] = "S"
                    player_board[row][col - 1] = "S"
                if col + 1 < SIZE:
                    if empty_board[row][col + 1] == "H" and not col == 4:
                        empty_board[row][col + 1] = "S"
                        player_board[row][col + 1] = "S"
                if row + 1 < SIZE:
                    if empty_board[row + 1][col] == "H" and not row == 4:
                        empty_board[row + 1][col] = "S"
                        player_board[row + 1][col] = "S"
        if has_won(player_board):
            print(f"Player {player + 1} wins!")
            quit()
        break

def waiting_screen():
    console_clear()
    print("Next player's placement phase")
    time.sleep(2)
    console_clear()
    os.system('pause')
    console_clear()

def has_won(board):
    count = 0
    for i in board:
        for j in i:
            if j == SHIP_PLACED:
                count += 1
    if count == 0:
        return True
    else:
        return False



def placement_phase():
    global BOARD
    global SHIPS_TO_PLACE

    round = 0
    player = round % 2

    print_board()
    while SHIPS_TO_PLACE > 0:
        mark()
        SHIPS_TO_PLACE -= 1
    player_one_board = BOARD

    waiting_screen()
    BOARD = generate_board()
    SHIPS_TO_PLACE = 6

    print_board()
    while SHIPS_TO_PLACE > 0:
        mark()
        SHIPS_TO_PLACE -= 1
    player_two_board = BOARD

    console_clear()
    print("Let the game begin!")
    time.sleep(2)
    os.system('pause')
    console_clear()

    empty_board_one  = generate_board()
    empty_board_two = generate_board()

    round = 0
    while True:
        player = round % 2
        print_two_boards(empty_board_one, empty_board_two)
        if player == 0:
            play(empty_board_two, player_two_board, player)
        if player == 1:
            play(empty_board_one, player_one_board, player)
        round += 1

def main():
    placement_phase()


if __name__ == "__main__":
    main()
