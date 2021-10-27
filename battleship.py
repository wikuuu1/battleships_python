import os
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#global variables
SIZE = 7
LIMIT = None
EMPTY_SPACE = f"{bcolors.OKBLUE}~{bcolors.ENDC}"
SHIP_PLACED = "X"
SHIPS_TO_PLACE = 6

# clears the screen
def console_clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#function generates basic board
def generate_board():
    global SIZE
    return [[EMPTY_SPACE] * SIZE for _ in range(SIZE)]

BOARD = generate_board()

#prints 5x5 board without borders
def print_board():
    global SIZE
    global BOARD
    for i in range(SIZE):
        print(f"   {i + 1}", end="")

    for i in range(SIZE):
        print(f"\n{chr(97 + i).upper()} ", end="")

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
    if SIZE < 10:
        if len(user_input) in range(2,3) and user_input[1].isdigit() and user_input[0].isalpha():
            if (ord(user_input[0].lower()) - 97) <= len(BOARD) - 1:
                if int(user_input[1]) <= len(BOARD):
                    return True
    else:
        if len(user_input) in range(2,4) and user_input[1].isdigit() and user_input[0].isalpha():
            second_index = int(user_input[1:])
            if (ord(user_input[0].lower()) - 97) <= len(BOARD) - 1:
                if second_index <= len(BOARD):
                    return True
    return False


# checks if ships aren't too close
def ships_too_close(board, row, col):
    # if board[row - 1][col] == SHIP_PLACED and not row == 0:
    #     return True
    if board[row][col - 1] == SHIP_PLACED and not col == 0:
        return True
    if col + 1 < SIZE:
        if board[row][col + 1] == SHIP_PLACED and not col == SIZE - 1:
            return True
    if row + 1 < SIZE:
        if board[row + 1][col] == SHIP_PLACED and not row == SIZE - 1:
            return True
    return False

# asks for direction and returns a second coordinate for two size ships
def get_direction_for_size_two_ship(row, col, direction):
    counter = 0
    while True:
        string = "Please choose direction:"
        if not row == 0:
            string += "\n» (u)p "
        if not row == SIZE - 1:
            string += "\n» (d)own "
        if not col == 0:
            string += "\n» (l)eft "
        if not col == SIZE - 1:
            string += "\n» (r)ight "
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
    # counter = 0
    while True:
        user_move = input("Please give your coordinates: ")
        if validate_format(user_move):
            row = ord(user_move[0].lower()) - 97
            if SIZE < 10:
                col = int(user_move[1]) - 1
            else:
                col = int(user_move[1:]) - 1

            length_of_board = len(BOARD)
            if not row <= length_of_board and not col <= length_of_board:
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
        if BOARD[row][col] == SHIP_PLACED:
            print("This place is taken already!")
            continue
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
        print("left")
    BOARD[row][col] = SHIP_PLACED
    console_clear()
    # print(f"\n       Player {player}\n")
    # print_board()


# prints board for each player in shooting phase
def print_two_boards(empty_board_one, empty_board_two):
    spaces = (SIZE - 5) * "    "
    print(f"{bcolors.OKGREEN}Your board{bcolors.ENDC} {spaces}               {bcolors.FAIL}Enemy's board{bcolors.ENDC}\n")
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
        if SIZE < 10:
            print("   ", end="")
        if SIZE == 10:
            print("    ", end="")
        print(chr(97 + i).upper() + "  ", end="")
        for j in range(SIZE):
            print(empty_board_two[i][j] + "   " , end="")
        print()
        print()


def play(empty_board, player_board, player):
    while True:
        print(f"Player {player + 1} turn!\n")
        row, col = ask_for_coordinates()
        if empty_board[row][col] == f"{bcolors.FAIL}M{bcolors.ENDC}" or empty_board[row][col] == f"{bcolors.OKCYAN}S{bcolors.ENDC}" or empty_board[row][col] == f"{bcolors.OKGREEN}H{bcolors.ENDC}":
            print(f"\nYou have already tried this shot!\n")
            continue
        if player_board[row][col] == EMPTY_SPACE:
            empty_board[row][col] = f"{bcolors.FAIL}M{bcolors.ENDC}"
            player_board[row][col] = f"{bcolors.FAIL}M{bcolors.ENDC}"
            # console_clear()
            print(f"{bcolors.FAIL}\nYou have missed!\n{bcolors.ENDC}")
        if player_board[row][col] == SHIP_PLACED:
            if ships_too_close(player_board, row, col):
                empty_board[row][col] = f"{bcolors.OKGREEN}H{bcolors.ENDC}"
                player_board[row][col] = f"{bcolors.OKGREEN}H{bcolors.ENDC}"
                # console_clear()
                print(f"{bcolors.OKGREEN}\nYou have hit a ship!\n{bcolors.ENDC}")
            else:
                empty_board[row][col] = f"{bcolors.OKCYAN}S{bcolors.ENDC}"
                player_board[row][col] = f"{bcolors.OKCYAN}S{bcolors.ENDC}"
                # console_clear()
                print(f"{bcolors.OKCYAN}\nYou have sunk a ship!\n{bcolors.ENDC}")
                if empty_board[row - 1][col] == "H" and not row == 0:
                    empty_board[row - 1][col] = f"{bcolors.OKCYAN}S{bcolors.ENDC}"
                    player_board[row - 1][col] = f"{bcolors.OKCYAN}S{bcolors.ENDC}"
                if empty_board[row][col - 1] == "H" and not col == 0:
                    empty_board[row][col - 1] = f"{bcolors.OKCYAN}S{bcolors.ENDC}"
                    player_board[row][col - 1] = f"{bcolors.OKCYAN}S{bcolors.ENDC}"
                if col + 1 < SIZE:
                    if empty_board[row][col + 1] == "H" and not col == SIZE - 1:
                        empty_board[row][col + 1] = f"{bcolors.OKCYAN}S{bcolors.ENDC}"
                        player_board[row][col + 1] = f"{bcolors.OKCYAN}S{bcolors.ENDC}"
                if row + 1 < SIZE:
                    if empty_board[row + 1][col] == "H" and not row == SIZE - 1:
                        empty_board[row + 1][col] = f"{bcolors.OKCYAN}S{bcolors.ENDC}"
                        player_board[row + 1][col] = f"{bcolors.OKCYAN}S{bcolors.ENDC}"
        if has_won(player_board):
            print(f"Player {player + 1} wins!")
            quit()
        break

def waiting_screen(message):
    console_clear()
    print(message)
    time.sleep(2)
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

def placement_phase(player):
    global SHIPS_TO_PLACE
    waiting_screen(f"Player {player + 1}, it's your turn to place the ships!\n")

    print("Place your ships! (for example C4)\n")

    print_board()
    print(f"Ships to place: {SHIPS_TO_PLACE}\n")
    while SHIPS_TO_PLACE > 0:

        mark()
        SHIPS_TO_PLACE -= 1
        print("Place your ships!\n")

        print_board()
        print(f"Ships to place: {SHIPS_TO_PLACE}\n")
    return BOARD

def menu():
    while True:
        print(SIZE)
        print("1. Play battleships.")
        print("2. Options.")
        print("3. Credits.")
        print("4. Quit.")
        user_input = int(input())
        if user_input == 1:
            break
        if user_input == 2:
            while True:
                print(SIZE)
                print("1. Set turn limit.")
                print("2. Set board size.")
                print("3. Back.")
                options = int(input())
                if options == 1:
                    turn_limit()
                    continue
                if options == 2:
                    custom_board()
                    continue
                if options == 3:
                    break
                else:
                    print("Invalid option.")
                    continue
        if user_input == 3:
            console_clear()
            print("The Gods of the game:")
            os.system("pause")
            continue
        if user_input == 4:
            print("Thanks for playing. See you soon!")
            quit()

    # wybor size (uzaleznic ilosc statkow od size)
    # limit tur
    # ascii
    # quit
    # play again

def welcome_screen():
    pass

def custom_board():
    global SIZE
    global BOARD
    while True:
        custom_size = int(input("Choose the board size in range 5 to 10: "))
        if custom_size in range(5, 11):
            SIZE = custom_size
            BOARD = generate_board()
            print(SIZE)
            break
        else:
            print("Invalid input! Must be between 5-10!")
            continue

def turn_limit():
    global LIMIT
    while True:
        question = input("Would you like to play with turn limit?(YES/NO)").lower()
        if question == "yes" or question == "y":
            while True:
                custom_limit = int(input("How many rounds would you like to play(5-50)"))
                if custom_limit in range(5, 51):
                    LIMIT = custom_limit
                else:
                    print("Invalid input! (must be between 5-50)")
                    continue
        if question == "no" or question == "n":
            return False
        else:
            print("Invalid input! Yes or No!")
            continue



def main():
    menu()
    global BOARD
    global SHIPS_TO_PLACE


    round = 0
    player = round % 2

    console_clear()
    player_one_board = placement_phase(player)

    BOARD = generate_board()
    SHIPS_TO_PLACE = 6
    player += 1

    player_two_board = placement_phase(player)

    console_clear()
    print("Let the game begin!\n")
    time.sleep(2)
    os.system('pause')
    console_clear()

    empty_board_one  = generate_board()
    empty_board_two = generate_board()

    round = 0
    while True:
        player = round % 2
        waiting_screen(f"Player {player + 1}, it's your turn to shot!\n")
        if player == 0:
            print_two_boards(player_one_board, empty_board_two)
            play(empty_board_two, player_two_board, player)
        if player == 1:
            print_two_boards(player_two_board, empty_board_one)
            play(empty_board_one, player_one_board, player)
        round += 1
        os.system('pause')


if __name__ == "__main__":
    main()