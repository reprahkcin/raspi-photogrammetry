import serial
import time

class MotorController:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.ser = serial.Serial(port, baudrate)
        time.sleep(2)  # Wait for serial connection to initialize

    def move_motor(self, motor, steps, direction):
        command = f"{motor}{steps}{direction}"
        self.ser.write(command.encode())

    def close(self):
        self.ser.close()
