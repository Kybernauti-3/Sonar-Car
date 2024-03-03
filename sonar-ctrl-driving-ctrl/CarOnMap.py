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

def move_car(room_grid, direction):
    if direction == 'W':
        move_up(room_grid)
    elif direction == 'S':
        move_down(room_grid)
    elif direction == 'A':
        move_left(room_grid)
    elif direction == 'D':
        move_right(room_grid)
    else:
        print("Invalid direction. Please enter W, S, A, or D.")

while True:
    direction = input("Enter direction (W, S, A, D to move the car, or 'Q' to quit): ").upper()
    if direction == 'Q':
        print("Exiting...")
        break
    move_car(room_grid, direction)
    print_map()