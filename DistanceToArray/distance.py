def generate_array(input_string):
    direction = input_string[0]  # Extracting direction: 'L' for left or 'R' for right
    distance_str = input_string[1:]  # Extracting distance string
    distance = int(distance_str)  # Converting distance string to integer
    
    # Divide distance by 10 to get the number of elements in the array
    num_elements = distance // 10
    
    # Create an array with 'num_elements' zeros
    array = [0] * num_elements
    
    # Set the last element to 1 if there's a remainder
    if distance % 10 != 0:
        array.append(1)
    
    # Insert 'S' at appropriate index based on direction
    if direction == 'L':
        array = [1] + [0] * (num_elements) + ['S']  # Insert 'S' at the end for left side
    elif direction == 'R':
        array = ['S'] + array  # Insert 'S' at the beginning for right side
    
    return array

while True:
    input_string = input("Enter direction (L/R) followed by distance in centimeters (e.g., L51 or R54): ")
    output_array = generate_array(input_string)
    print("Output array:", output_array)
