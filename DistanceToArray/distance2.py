def generate_array(input_string):
    arrays = []  # List to store arrays for each input
    
    # Split input by space to handle multiple inputs
    inputs = input_string.split()
    
    for inp in inputs:
        direction = inp[0]  # Extracting direction: 'L' for left or 'R' for right
        distance_str = inp[1:]  # Extracting distance string
        distance = int(distance_str)  # Converting distance string to integer
        
        # Divide distance by 10 to get the number of elements in the array
        num_elements = distance // 10
        
        # Create an array with 'num_elements' zeros
        array = [0] * num_elements
        
        # Set the last element to 1 if there's a remainder
        if distance % 10 != 0:
            array.append(1)
        
        # If direction is 'L' and there are more than one element in the array, rotate the array
        if direction == 'L' and len(array) > 1:
            array = array[-1:] + array[:-1]
        
        arrays.append(array)  # Append the generated array
    
    # Insert 'S' in the middle
    middle_index = len(arrays) // 2
    arrays.insert(middle_index, ['S'])
    
    # Combine arrays into one
    combined_array = []
    for arr in arrays:
        combined_array.extend(arr)
    
    return combined_array

while True:
    input_string = input("Enter direction and distance in centimeters separated by space (e.g., 'L51 R24'): ")
    output_array = generate_array(input_string)
    print("Output array:", output_array)
