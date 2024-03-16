import tkinter as tk
import paho.mqtt.client as mqtt

# MQTT Broker Configuration
broker_address = "broker.emqx.io"
broker_port = 1883
topic = "key_pressed"

# Callback function for MQTT connection
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
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

# GUI Setup
root = tk.Tk()
root.title("Wireless MQTT controller")

# Function to disconnect MQTT client when closing the GUI
def on_closing():
    client.disconnect()
    root.destroy()

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
button_w.grid(row=0, column=1)
button_a = tk.Button(root, text="A", command=lambda: send_key("A"), **button_style)
button_a.grid(row=1, column=0)
button_s = tk.Button(root, text="S", command=lambda: send_key("S"), **button_style)
button_s.grid(row=1, column=1)
button_d = tk.Button(root, text="D", command=lambda: send_key("D"), **button_style)
button_d.grid(row=1, column=2)

# Bind key press events to individual buttons
root.bind("<KeyPress-w>", lambda event: on_key_press(event, button_w))
root.bind("<KeyPress-a>", lambda event: on_key_press(event, button_a))
root.bind("<KeyPress-s>", lambda event: on_key_press(event, button_s))
root.bind("<KeyPress-d>", lambda event: on_key_press(event, button_d))

root.protocol("WM_DELETE_WINDOW", on_closing)  # Bind closing event to on_closing function

root.mainloop()
