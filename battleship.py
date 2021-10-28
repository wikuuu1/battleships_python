import os
import time
import random

class bcolors:
# DARK COLORS
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m' # BROWN
    BLUE = '\033[34m'
    MAGNETA = '\033[35m' # RED-ISH PURPLE
    CYAN = '\033[36m' # TEAL (TURKUSOWY)
    WHITE = '\033[37m' # GRAY
# BRIGHT COLORS
    BBLACK = '\033[90m' # DARKER GRAY
    BRED = '\033[91m' # SALMON COLOR
    BGREEN = '\033[92m'
    BYELLOW = '\033[93m' # NORMAL YELLOW
    BBLUE = '\033[94m' # BLUE-ISH PURPLE
    BMAGNETA = '\033[95m'
    BCYAN = '\033[96m'
    BWHITE = '\033[97m' # WHITE
# STYLES
    ENDC = '\033[0m' # FINISHES COLOR CODING
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#global variables
SIZE = 5
LIMIT = SIZE * SIZE
EMPTY_SPACE = f"{bcolors.BLUE}~{bcolors.ENDC}"
SHIP_PLACED = "X"
SHIPS_TO_PLACE = 6
INFO = ""
AI = False

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
    if board[row - 1][col] == SHIP_PLACED and not row == 0:
        return True
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
            print("\nIncorrect direction. Try again!\n")
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
                print("\nInvalid input\n")
                continue
        else:
            # counter += 1
            # if counter == 5:
            #     console_clear()
            #     counter = 0
            #     print_board()
            print("\nWrong coordinates format\n")
            continue

        return row, col

# takes user input and checks its validity
def place_ship():
    while True:
        direction = None
        row, col, direction = ai_place_ship()   # zmiana row, col = ask_for_coordinates()
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


# prints board for each player in shooting phase
def print_two_boards(empty_board_one, empty_board_two):
    spaces = (SIZE - 5) * "    "
    print(f"{bcolors.GREEN}Your board{bcolors.ENDC} {spaces}               {bcolors.RED}Enemy's board{bcolors.ENDC}\n")
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
    global INFO
    while True:
        print(f"Player {player + 1} turn!\n")
        if player == 0:
            row, col = ask_for_coordinates()
        if player == 1 and AI == True:
            row, col = AI_move(empty_board)
        if player == 1 and AI == False:
            row, col = ask_for_coordinates()
        if empty_board[row][col] == f"{bcolors.RED}M{bcolors.ENDC}" or empty_board[row][col] == f"{bcolors.CYAN}S{bcolors.ENDC}" or empty_board[row][col] == f"{bcolors.GREEN}H{bcolors.ENDC}":
            print(f"\nYou have already tried this shot!\n")
            continue
        if player_board[row][col] == EMPTY_SPACE:
            empty_board[row][col] = f"{bcolors.RED}M{bcolors.ENDC}"
            player_board[row][col] = f"{bcolors.RED}M{bcolors.ENDC}"
            INFO = f"{bcolors.RED}\nPlayer {player + 1} has missed! ({str(chr(row + 65)) + str((col + 1))})\n{bcolors.ENDC}"
            print(f"{bcolors.RED}\nYou have missed!\n{bcolors.ENDC}")
        if player_board[row][col] == SHIP_PLACED:
            if ships_too_close(player_board, row, col):
                empty_board[row][col] = f"{bcolors.GREEN}H{bcolors.ENDC}"
                player_board[row][col] = f"{bcolors.GREEN}H{bcolors.ENDC}"
                INFO = (f"{bcolors.GREEN}\nPlayer {player + 1} has hit a ship! ({str(chr(row + 65)) + str((col + 1))})\n{bcolors.ENDC}")
                print((f"{bcolors.GREEN}\nYou have hit a ship!\n{bcolors.ENDC}"))
            else:
                empty_board[row][col] = f"{bcolors.CYAN}S{bcolors.ENDC}"
                player_board[row][col] = f"{bcolors.CYAN}S{bcolors.ENDC}"
                INFO = (f"{bcolors.CYAN}\nPlayer {player + 1} has sunk a ship! ({str(chr(row + 65)) + str((col + 1))})\n{bcolors.ENDC}")
                print((f"{bcolors.CYAN}\nYou have sunk a ship!\n{bcolors.ENDC}"))
                if empty_board[row - 1][col] == f"{bcolors.GREEN}H{bcolors.ENDC}" and not row == 0:
                    empty_board[row - 1][col] = f"{bcolors.CYAN}S{bcolors.ENDC}"
                    player_board[row - 1][col] = f"{bcolors.CYAN}S{bcolors.ENDC}"
                if empty_board[row][col - 1] == f"{bcolors.GREEN}H{bcolors.ENDC}" and not col == 0:
                    empty_board[row][col - 1] = f"{bcolors.CYAN}S{bcolors.ENDC}"
                    player_board[row][col - 1] = f"{bcolors.CYAN}S{bcolors.ENDC}"
                if col + 1 < SIZE:
                    if empty_board[row][col + 1] == f"{bcolors.GREEN}H{bcolors.ENDC}" and not col == SIZE - 1:
                        empty_board[row][col + 1] = f"{bcolors.CYAN}S{bcolors.ENDC}"
                        player_board[row][col + 1] = f"{bcolors.CYAN}S{bcolors.ENDC}"
                if row + 1 < SIZE:
                    if empty_board[row + 1][col] == f"{bcolors.GREEN}H{bcolors.ENDC}" and not row == SIZE - 1:
                        empty_board[row + 1][col] = f"{bcolors.CYAN}S{bcolors.ENDC}"
                        player_board[row + 1][col] = f"{bcolors.CYAN}S{bcolors.ENDC}"
        if has_won(player_board):
            console_clear()
            print(f"Player {player + 1} wins!\n")
            play_again()
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


def sunk_ships_close(row, col, board):
    if board[row - 1][col] == f"{bcolors.CYAN}S{bcolors.ENDC}" and not row == 0:
        return True
    if board[row][col - 1] == f"{bcolors.CYAN}S{bcolors.ENDC}" and not col == 0:
        return True
    if col + 1 < SIZE:
        if board[row][col + 1] == f"{bcolors.CYAN}S{bcolors.ENDC}" and not col == SIZE - 1:
            return True
    if row + 1 < SIZE:
        if board[row + 1][col] == f"{bcolors.CYAN}S{bcolors.ENDC}" and not row == SIZE - 1:
            return True
    return False

def AI_move(empty_board): # zmiana
    while True:
            for index1, row in enumerate(empty_board):
                for index2, i in enumerate(row):
                    if i == f"{bcolors.GREEN}H{bcolors.ENDC}":
                        row, col = index1, index2
                        if empty_board[row - 1][col] == EMPTY_SPACE and not row == 0:
                            return row - 1, col
                        if empty_board[row][col - 1] == EMPTY_SPACE and not col == 0:
                            return row, col - 1
                        if col + 1 < SIZE:
                            if empty_board[row][col + 1] == EMPTY_SPACE and not col == SIZE - 1:
                                return row, col + 1
                        if row + 1 < SIZE:
                            if empty_board[row + 1][col] == EMPTY_SPACE and not row == SIZE - 1:
                                return row + 1, col

            potencial_row = []
            for index, row in enumerate(empty_board):
                if row.count(EMPTY_SPACE):
                    potencial_row.append(index)
            # print(potencial_row)
            first_index = random.choice(potencial_row)
            # print(first_index)

            potencial_move = []
            for index, row in enumerate(empty_board[first_index]):
                if row == EMPTY_SPACE:
                    potencial_move.append(index)
            # print(potencial_move)
            second_index = random.choice(potencial_move)
            # print(second_index)
            if empty_board[first_index][second_index] and sunk_ships_close(first_index, second_index, empty_board):
                continue
            else:
                return first_index, second_index

def ai_place_ship(): # zmiana
    while True:
        if SHIPS_TO_PLACE > 3:
            potencial_place = []
            for index, row in enumerate(BOARD):
                if row.count(EMPTY_SPACE) > 1:
                    potencial_place.append(index)

            first_index = random.choice(potencial_place)

            potencial_move = []
            for index, row in enumerate(BOARD[first_index]):
                if row == EMPTY_SPACE:
                    potencial_move.append(index)

            second_index = random.choice(potencial_move)
            directions = ["up", "down", "right", "left"]
            direct = random.choices(directions)
            print(first_index, second_index, direct)
            if "up" in direct and not ships_too_close(BOARD, first_index, second_index) and not ships_too_close(BOARD, first_index - 1, second_index):
                return first_index, second_index, direct
            if "down" in direct and not ships_too_close(BOARD, first_index, second_index) and not ships_too_close(BOARD, first_index + 1, second_index):
                return first_index, second_index, direct
            if "right" in direct and not ships_too_close(BOARD, first_index, second_index) and not ships_too_close(BOARD, first_index, second_index + 1):
                return first_index, second_index, direct
            if "left" in direct and not ships_too_close(BOARD, first_index, second_index) and not ships_too_close(BOARD, first_index, second_index - 1):
                return first_index, second_index, direct
            else:
                continue
        else:
            potencial_place = []
            for index, row in enumerate(BOARD):
                if row.count(EMPTY_SPACE) > 1:
                    potencial_place.append(index)

            first_index = random.choice(potencial_place)

            potencial_move = []
            for index, row in enumerate(BOARD[first_index]):
                if row == EMPTY_SPACE:
                    potencial_move.append(index)

            second_index = random.choice(potencial_move)
            if ships_too_close(BOARD, first_index, second_index):
                continue

def play_again():
    print("""Would you like to play again?"

    1. Yes

    2. No
    """)
    while True:
        again = input().strip()
        if again == "":
            continue
        if again == "1":
            main()
        if again == "2":
            print("\nFarewell Dear Pirate! Arr!\n")
            quit()
        else:
            print("\nInvalid input! Try again!\n")
            continue

def welcome_screen():
    pass

def custom_board():
    global SIZE
    global BOARD
    while True:
        custom_size = input("Choose the board size in range 5-10: ").strip()
        if custom_size == "":
            print("\nInvalid input! Must be between 5-10!\n")
            continue
        if int(custom_size) in range(5, 11):
            SIZE = int(custom_size)
            BOARD = generate_board()
            break
        else:
            print("\nInvalid input! Must be between 5-10!\n")
            continue

def turn_limit():
    global LIMIT
    while True:
        custom_limit = input("Choose the number of rounds between 5-50: ").strip()
        if custom_limit == "":
            print("\nInvalid input! Must be between 5-50!\n")
            continue
        if int(custom_limit) in range(5, 51):
            LIMIT = int(custom_limit)
            break
        else:
            print("\nInvalid input! Must be between 5-50!\n")
            continue



def main():
    global BOARD
    global SHIPS_TO_PLACE
    global LIMIT
    SIZE = 5

    LIMIT = SIZE * SIZE
    SHIPS_TO_PLACE = 6



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
        waiting_screen(f"{INFO}\nPlayer {player + 1}, it's your turn to shot!\n")
        if player == 0:
            print_two_boards(player_one_board, empty_board_two)
            if LIMIT > 0:
                print(f"Turns left: {LIMIT}\n")
            play(empty_board_two, player_two_board, player)
        if player == 1:
            print_two_boards(player_two_board, empty_board_one)
            if LIMIT > 0:
                print(f"Turns left: {LIMIT}\n")
            play(empty_board_one, player_one_board, player)
        round += 1
        if round % 2 == 0:
            LIMIT -= 1
        os.system('pause')
        if LIMIT == 0:
            console_clear()
            print("No more turns, it's a draw.\n")
            play_again()

def menu():
    global AI
    global BOARD
    while True:
        console_clear()
        print("""MAIN MENU

    1. Play battleships

    2. Options

    3. Credits

    4. Quit
    """)
        user_input = input().strip()
        if user_input == "":
            continue
        if user_input == "1":
            while True:
                console_clear()
                print("""MENU

        1. Play against a friend

        2. Play against the computer
        """)
                user_choice = input().strip()
                if user_choice == "1":
                    main()
                if user_choice == "2":
                    AI = True
                    main()
                else:
                    print("\nInvalid option.\n")
                    time.sleep(2)
                    continue
        if user_input == "2":
            while True:
                console_clear()
                print("""MENU

    1. Set turn limit

    2. Set board size

    3. Return to main menu
    """)
                options = input().strip()
                if options == "":
                    continue
                if options == "1":
                    console_clear()
                    turn_limit()
                    continue
                if options == "2":
                    console_clear()
                    custom_board()
                    continue
                if options == "3":
                    menu()
                else:
                    print("\nInvalid option.\n")
                    time.sleep(2)
                    continue
        if user_input == "3":
            console_clear()
            print("The Gods of the game:")
            os.system("pause")
            continue
        if user_input == "4":
            console_clear()
            print("\nThanks for playing. See you soon!\n")
            quit()
        else:
            print("\nInvalid option.\n")
            time.sleep(2)
            continue

if __name__ == "__main__":
    menu()


#ships to place
#ai
#ascii