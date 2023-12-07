import serial
import time

# Initialize serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace '/dev/ttyUSB0' with your specific port
time.sleep(2)  # Wait for the serial connection to initialize

# Send a command to move the steppers forward
ser.write(b'F')
time.sleep(2)  # Wait for the action to complete

# Send a command to move the steppers backward
ser.write(b'B')
time.sleep(2)  # Wait for the action to complete

# Close the serial connection
ser.close()
