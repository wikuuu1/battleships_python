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
        return True
    else:
        return False

    # second_index = int(user_move[1:])
    # print(second_index)

# checks if ships aren't too close
def proximity_of_ships(row, col):
    if BOARD[row - 1][col] == SHIP_PLACED and not row == 0:
        return True
    if BOARD[row][col - 1] == SHIP_PLACED and not col == 0:
        return True
    if col + 1 < SIZE:
        if BOARD[row][col + 1] == SHIP_PLACED and not col == 4:
            return True
    if row + 1 < SIZE:
        if BOARD[row + 1][col] == SHIP_PLACED and not row == 4:
            return True
    return False

def get_direction_for_size_two_ship(row, col, direction):
    while True:
        direction = input("Please choose direction(up/down/left/right): ")
        if direction == "up" and not row == 0:
            if not proximity_of_ships(row - 1, col):
                return row - 1, col, direction
        if direction == "down" and not row == 4:
            if not proximity_of_ships(row + 1, col):
                return row + 1, col, direction
        if direction == "right" and not col == 4:
            if not proximity_of_ships(row, col + 1):
                return row, col + 1, direction
        if direction == "left" and not col == 0:
            if not proximity_of_ships(row, col - 1):
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
            if SHIPS_TO_PLACE > 3 and not proximity_of_ships(row, col):
                return get_direction_for_size_two_ship(row, col, direction)
            if proximity_of_ships(row, col):
                print("Ships are too close!")
                continue
            else:
                return row, col, direction
        else:
            print("")

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



def main():
    print_board()
    global SHIPS_TO_PLACE
    while SHIPS_TO_PLACE > 0:
        mark()
        SHIPS_TO_PLACE -= 1
        print(SHIPS_TO_PLACE)

if __name__ == "__main__":
    main()

