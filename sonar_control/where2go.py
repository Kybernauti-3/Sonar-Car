import random

previous_move = None

def car_position(map):
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == "S":
                return i, j
    return 5, 5

def GenerateMove(map):
    global previous_move
    row, col = car_position(map)
    possible_moves = []

    if map[row-1][col] == 0 and previous_move != "Move down":
        possible_moves.append("Move up")
    if map[row+1][col] == 0 and previous_move != "Move up":
        possible_moves.append("Move down")
    if map[row][col-1] == 0 and previous_move != "Move right":
        possible_moves.append("Move left")
    if map[row][col+1] == 0 and previous_move != "Move left":
        possible_moves.append("Move right")

    if not possible_moves:
        return "No free path available"

    # Choose a random move from the possible moves
    move = random.choice(possible_moves)
    previous_move = move

    return move

"""map = grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 'S', 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
"""