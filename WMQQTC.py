import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import numpy as np

# MQTT Broker Configuration
broker_address = "broker.emqx.io"
broker_port = 1883
topic = "key_pressed"

# Callback function for MQTT connection
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

# MQTT client setup
client = mqtt.Client(protocol=mqtt.MQTTv311)  # Specify MQTT protocol version
client.on_connect = on_connect
client.connect(broker_address, broker_port, 60)

# Function to send respective key when button pressed
def send_key(key):
    client.publish(topic, key)

# Function to change button color when pressed
def change_button_color(button):
    button.config(bg="gray", fg="black")  # Change button color when pressed

# Function to reset button color
def reset_button_color(button):
    button.config(bg="#4CAF50", fg="white")  # Reset button color

# Function to handle key events
def on_key_press(event, button):
    key = event.keysym.upper()
    if key in ("W", "A", "S", "D"):
        send_key(key)
        change_button_color(button)
        root.after(200, lambda: reset_button_color(button))  # Reset button color after a short delay

def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    if message.startswith("[["):
        plot_map_from_message(message)

def plot_map_from_message(message):
    try:
        # Parse the map data from the message
        mapa = eval(message)
        mapa = np.array(mapa)

        def find_biggest_number(map_array):
            # Convert the map array to integers (assuming it contains numbers as strings)
            xx = map_array.copy()
            xx[xx == 'S'] = 0
            map_array = xx.astype(int)
            # Find the maximum value in the array
            max_value = np.max(map_array) + 1
            return max_value

        # Replace 'S' with a blue point marker
        x = find_biggest_number(mapa)
        mapa[mapa == 'S'] = x

        # Convert the array to integers
        mapa = mapa.astype(int)

        # Create a plot
        plt.figure(figsize=(8, 8))

        # Display the map
        plt.imshow(mapa, cmap='binary', interpolation='nearest')

        # Plot the blue square marker
        blue_point_indices = np.where(mapa == x)
        plt.scatter(blue_point_indices[1], blue_point_indices[0], s=100, c='blue', marker='s')  # 's' for square marker

        # Add a colorbar to show the legend
        #cbar = plt.colorbar(ticks=[0, 1])
        #cbar.ax.set_yticklabels(['Free', 'Obstacle'])

        # Add grid lines to visually separate each cell
        plt.grid(True, color='black', linewidth=0.5)

        # Add title and labels
        plt.title('Map')
        plt.xlabel('X')
        plt.ylabel('Y')

        # Show plot
        plt.show()

    except Exception as e:
        print("Error plotting map:", e)


# Function to handle plotting
def plot_map():
    map_input = entry_map.get()  # Get the text from the entry field
    
    # Check if the input is empty
    if not map_input:
        return
    
    # Parse the input string to create a 2D list
    try:
        mapa = eval(map_input)
    except Exception as e:
        print("Error parsing map input:", e)
        return

    # Convert the 2D list to a numpy array
    mapa = np.array(mapa)
    
    def find_biggest_number(map_array):
        # Convert the map array to integers (assuming it contains numbers as strings)
        xx = map_array.copy()
        xx[xx == 'S'] = 0
        map_array = xx.astype(int)
        # Find the maximum value in the array
        max_value = np.max(map_array)+1
        return max_value

    # Replace 'S' with a blue point marker
    x = find_biggest_number(mapa)
    mapa[mapa == 'S'] = x
    
    # Convert the array to integers
    mapa = mapa.astype(int)

    # Create a plot
    plt.figure(figsize=(8, 8))

    # Display the map
    plt.imshow(mapa, cmap='binary', interpolation='nearest')
    
    # Plot the blue square marker
    blue_point_indices = np.where(mapa == x)
    plt.scatter(blue_point_indices[1], blue_point_indices[0], s=100, c='blue', marker='s')  # 's' for square marker

    # Add a colorbar to show the legend
    #cbar = plt.colorbar(ticks=[0, 1])
    #cbar.ax.set_yticklabels(['Free', 'Obstacle'])

    # Add grid lines to visually separate each cell
    plt.grid(True, color='black', linewidth=0.5)

    # Add title and labels
    plt.title('Map')
    plt.xlabel('X')
    plt.ylabel('Y')

    # Show plot
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("Wireless Controller with Plotter")

# Configure button style
button_style = {
    "font": ("Helvetica", 20),  # Set font size and family
    "width": 6,  # Set button width
    "height": 3,  # Set button height
    "bg": "#4CAF50",  # Set background color
    "fg": "white",  # Set text color
    "borderwidth": 0,  # Set border width
}

# Buttons for W, A, S, D
button_w = tk.Button(root, text="W", command=lambda: send_key("W"), **button_style)
button_w.grid(row=0, column=1, padx=5, pady=5)
button_a = tk.Button(root, text="A", command=lambda: send_key("A"), **button_style)
button_a.grid(row=1, column=0, padx=5, pady=5)
button_s = tk.Button(root, text="S", command=lambda: send_key("S"), **button_style)
button_s.grid(row=1, column=1, padx=5, pady=5)
button_d = tk.Button(root, text="D", command=lambda: send_key("D"), **button_style)
button_d.grid(row=1, column=2, padx=5, pady=5)

# Bind key press events to individual buttons
root.bind("<KeyPress-w>", lambda event: on_key_press(event, button_w))
root.bind("<KeyPress-a>", lambda event: on_key_press(event, button_a))
root.bind("<KeyPress-s>", lambda event: on_key_press(event, button_s))
root.bind("<KeyPress-d>", lambda event: on_key_press(event, button_d))

# Input field for map data
entry_map = ttk.Entry(root, width=30)
entry_map.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

# Button to display plot
btn_plot = ttk.Button(root, text="Plot Map", command=plot_map)
btn_plot.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
