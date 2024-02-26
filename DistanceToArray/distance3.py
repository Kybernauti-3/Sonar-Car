def generate_initial_array(length):
    return [1] * length

def update_array_with_input(array, input_string, length):
    direction = input_string[0]  # Extracting direction: 'L' for left or 'R' for right
    distance_str = input_string[1:].strip()  # Extracting distance string and removing leading/trailing spaces
    distance = int(distance_str)  # Converting distance string to integer
    
    # Divide distance by 10 to get the number of elements to update
    num_elements = distance // 10
    
    # Update array based on direction and distance
    if direction == 'L':
        for i in range(min(num_elements, len(array))):  # Ensure we don't go out of array bounds,
            array[i] = 0
    elif direction == 'R':
        for i in range(length // 2, min(length // 2 + num_elements, length)):  # Ensure we don't go out of array bounds
            array[i] = 0
    
    # Insert 'S' back into the array
    middle_index = length // 2
    array[middle_index] = 'S'
    
    return array

# Generate initial array
length = 11  # Specify the length of the initial array
array = generate_initial_array(length)

while True:
    input_string = input("Enter direction and distance in centimeters (e.g., 'L28' or 'R14'), or 'done' to exit: ")
    if input_string.lower() == 'done':
        break
    
    # Update array with input
    array = update_array_with_input(array, input_string, length)
    
    print("Updated array:", array)
