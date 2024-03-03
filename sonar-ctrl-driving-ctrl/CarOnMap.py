# Function to create an empty grid representation of a room
def create_empty_room(length, width):
    room_grid = [[0] * width for _ in range(length)]
    for i in range(length):
        room_grid[i][0] = 1  # First column is considered as wall
        room_grid[i][-1] = 1  # Last column is considered as wall
    for j in range(width):
        room_grid[0][j] = 1  # First row is considered as wall
        room_grid[-1][j] = 1  # Last row is considered as wall
    return room_grid

def print_map():
    print("Printing map")
    for row in room_grid:
        print(' '.join(map(str, row)))

# Function to add obstacles to the room grid
def add_obstacle(room_grid, x, y):
    if 0 < x < len(room_grid) - 1 and 0 < y < len(room_grid[0]) - 1:  # Ensure coordinates are within bounds and not blocking walls
        room_grid[x][y] = 1

def spawn_car(room_grid, x, y):
    if 0 < x < len(room_grid) - 1 and 0 < y < len(room_grid[0]) - 1:  # Ensure coordinates are within bounds and not blocking walls
        room_grid[x][y] = "S"
        return x, y
    else:
        raise ValueError("Invalid car position. Coordinates must be within the room bounds.")

# Room dimensions (length and width in meters)
room_length = 10
room_width = 10

# Create an empty room
room_grid = create_empty_room(room_length, room_width)

# Add obstacles to the room grid
obstacles = [(2, 2), (4, 5), (5, 7)]
for obstacle in obstacles:
    add_obstacle(room_grid, *obstacle)

# Spawn a car in the room
spawn_car(room_grid, 5, 5)

# Print the room grid
print(f"Room Dimensions: {room_length} x {room_width}")
for row in room_grid:
    print(' '.join(map(str, row)))

# Function to move the car up in the room grid
def move_up(room_grid):
    for i in range(len(room_grid)):
        for j in range(len(room_grid[0])):
            if room_grid[i][j] == "S":
                if i > 1 and room_grid[i - 1][j] != 1:  # Check if moving up is valid
                    room_grid[i][j] = 0  # Clear the current position
                    room_grid[i - 1][j] = "S"  # Move the car up
                return

# Function to move the car down in the room grid
def move_down(room_grid):
    for i in range(len(room_grid) - 1, -1, -1):
        for j in range(len(room_grid[0])):
            if room_grid[i][j] == "S":
                if i < len(room_grid) - 2 and room_grid[i + 1][j] != 1:  # Check if moving down is valid
                    room_grid[i][j] = 0  # Clear the current position
                    room_grid[i + 1][j] = "S"  # Move the car down
                return

# Function to move the car left in the room grid
def move_left(room_grid):
    for i in range(len(room_grid)):
        for j in range(len(room_grid[0])):
            if room_grid[i][j] == "S":
                if j > 1 and room_grid[i][j - 1] != 1:  # Check if moving left is valid
                    room_grid[i][j] = 0  # Clear the current position
                    room_grid[i][j - 1] = "S"  # Move the car left
                return

# Function to move the car right in the room grid
def move_right(room_grid):
    for i in range(len(room_grid)):
        for j in range(len(room_grid[0]) - 1, -1, -1):
            if room_grid[i][j] == "S":
                if j < len(room_grid[0]) - 2 and room_grid[i][j + 1] != 1:  # Check if moving right is valid
                    room_grid[i][j] = 0  # Clear the current position
                    room_grid[i][j + 1] = "S"  # Move the car right
                return

def can_move_up(room_grid):
    for i in range(len(room_grid)):
        for j in range(len(room_grid[0])):
            if room_grid[i][j] == "S":
                if i > 1 and room_grid[i - 1][j] != 1:  # Check if moving up is valid
                    return True
                else:
                    return False
    return False

def can_move_down(room_grid):
    for i in range(len(room_grid) - 1, -1, -1):
        for j in range(len(room_grid[0])):
            if room_grid[i][j] == "S":
                if i < len(room_grid) - 2 and room_grid[i + 1][j] != 1:  # Check if moving down is valid
                    return True
                else:
                    return False
    return False

def can_move_left(room_grid):
    for i in range(len(room_grid)):
        for j in range(len(room_grid[0])):
            if room_grid[i][j] == "S":
                if j > 1 and room_grid[i][j - 1] != 1:  # Check if moving left is valid
                    return True
                else:
                    return False
    return False

def can_move_right(room_grid):
    for i in range(len(room_grid)):
        for j in range(len(room_grid[0]) - 1, -1, -1):
            if room_grid[i][j] == "S":
                if j < len(room_grid[0]) - 2 and room_grid[i][j + 1] != 1:  # Check if moving right is valid
                    return True
                else:
                    return False
    return False

def move_car(room_grid, direction):
    x, y = None, None  # Initialize coordinates
    moved = False  # Flag to indicate if the car moved successfully
    if direction == 'W':
        if can_move_up(room_grid):
            move_up(room_grid)
            moved = True
        else:
            print("Cannot move up. Obstacle in the way.")
    elif direction == 'S':
        if can_move_down(room_grid):
            move_down(room_grid)
            moved = True
        else:
            print("Cannot move down. Obstacle in the way.")
    elif direction == 'A':
        if can_move_left(room_grid):
            move_left(room_grid)
            moved = True
        else:
            print("Cannot move left. Obstacle in the way.")
    elif direction == 'D':
        if can_move_right(room_grid):
            move_right(room_grid)
            moved = True
        else:
            print("Cannot move right. Obstacle in the way.")
    elif direction == 'P':
        # Print the coordinates of the car
        for i in range(len(room_grid)):
            for j in range(len(room_grid[0])):
                if room_grid[i][j] == "S":
                    x, y = i, j
                    break
        if x is not None and y is not None:
            print(f"Current position of the car: ({x}, {y})")
        else:
            print("Car not found in the room.")
    else:
        print("Invalid direction. Please enter W, S, A, D, or P.")

    if moved:
        # Find the coordinates of the car after moving
        for i in range(len(room_grid)):
            for j in range(len(room_grid[0])):
                if room_grid[i][j] == "S":
                    x, y = i, j
                    break

        # Print the map if the car moved successfully
        print_map()
        # Print the coordinates
        if x is not None and y is not None:
            print(f"Car moved to position: ({x}, {y})")
        else:
            print("Car not found in the room.")


while True:
    direction = input("Enter direction (W, S, A, D to move the car, P to print car position, or 'Q' to quit): ").upper()
    if direction == 'Q':
        print("Exiting...")
        break
    move_car(room_grid, direction)