import serial
import time

# Configuration
port = '/dev/ttyACM0'  # Change this to the path of your Arduino serial port
baud = 9600
motor = 2
direction = 'left'
steps = 2000

# Open a serial connection to the Arduino
ser = serial.Serial(port, baud, timeout=1)

# Define the command format to send to the Arduino
command = f"motor={motor} direction={direction} steps={steps}"

# Send the command to the Arduino
ser.write(command.encode())

# Wait for the response from the Arduino
response = ser.readline().decode().strip()
print(response)

# Close the serial connection
ser.close()
