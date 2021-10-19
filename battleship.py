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
def print_board():
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

print_board()

# def validate_format(user_input): # --> True / False
#     # Change to range(2,4) for custom board size
#     if len(user_input) in range(2,3) and user_input[1].isdigit() and user_input[0].isalpha():
#         return True
#     else:
#         return False

#     # second_index = int(user_move[1:])
#     # print(second_index)



# def get_move(board):
#     while True:
#         user_move = input("Please give your coordinates: ")
#         if validate_format(user_move):
#             row = ord(user_move[0].lower()) - 97
#             col = int(user_move[1])
#             lenght_of_board = len(board)
#             if not row <= lenght_of_board and not col <= lenght_of_board:
#                 print("Invalid input")
#                 continue
#             else:
#                 return print(board[row][col])
#         else:
#             print("")




# get_move([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])


