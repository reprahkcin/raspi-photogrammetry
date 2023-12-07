import tkinter as tk
from tkinter import ttk
import subprocess
from motor_controller import MotorController
from camera_controller import CameraController

class MotorControlApp:
    def __init__(self, master):
        self.master = master
        self.mc = MotorController('/dev/ttyACM0', 9600)  # Adjust as necessary

        # Initialize CameraController before create_widgets
        self.camera = CameraController()

        # Constants
        self.steps_per_revolution = 27118  # Motor 1
        self.steps_per_cm = 6625          # Motor 2

        self.master.title("Motor Control")
        self.create_widgets()


    def create_widgets(self):
        # Motor 1 Degree Dropdown and Direction
        tk.Label(self.master, text="Motor 1 (Degrees)").grid(row=0, column=0, columnspan=2)
        self.motor1_degree = tk.StringVar()
        motor1_options = ttk.Combobox(self.master, textvariable=self.motor1_degree,
                                      values=["1", "5", "10", "15", "30", "90"])
        motor1_options.grid(row=1, column=0, columnspan=2)
        motor1_options.current(0)  # Default selection
        self.motor1_direction = tk.StringVar(value="F")
        tk.Radiobutton(self.master, text="Forward", variable=self.motor1_direction, value="F").grid(row=2, column=0)
        tk.Radiobutton(self.master, text="Backward", variable=self.motor1_direction, value="B").grid(row=2, column=1)
        tk.Button(self.master, text="Rotate", command=lambda: self.move_motor('1', self.calculate_steps_motor1(), self.motor1_direction.get())).grid(row=3, column=0, columnspan=2)

        # Motor 2 Distance Dropdown and Direction
        tk.Label(self.master, text="Motor 2 (Distance)").grid(row=4, column=0, columnspan=2)
        self.motor2_distance = tk.StringVar()
        motor2_options = ttk.Combobox(self.master, textvariable=self.motor2_distance,
                                      values=["0.01", "0.05", "0.1", "0.5", "1"])
        motor2_options.grid(row=5, column=0, columnspan=2)
        motor2_options.current(0)  # Default selection
        self.motor2_direction = tk.StringVar(value="F")
        tk.Radiobutton(self.master, text="Forward", variable=self.motor2_direction, value="F").grid(row=6, column=0)
        tk.Radiobutton(self.master, text="Backward", variable=self.motor2_direction, value="B").grid(row=6, column=1)
        tk.Button(self.master, text="Move", command=lambda: self.move_motor('2', self.calculate_steps_motor2(), self.motor2_direction.get())).grid(row=7, column=0, columnspan=2)

        # Camera Control Buttons
        tk.Button(self.master, text="Start Camera Preview", command=self.camera.start_preview).grid(row=8, column=0)
        tk.Button(self.master, text="Stop Camera Preview", command=self.camera.stop_preview).grid(row=8, column=1)
        
    def calculate_steps_motor1(self):
        degrees = float(self.motor1_degree.get())
        steps = int((degrees / 360) * self.steps_per_revolution)
        return steps

    def calculate_steps_motor2(self):
        distance_cm = float(self.motor2_distance.get())
        steps = int(distance_cm * self.steps_per_cm)
        return steps

    def move_motor(self, motor, steps, direction):
        self.mc.move_motor(motor, steps, direction)

    def close(self):
        self.mc.close()
        
    def start_preview(self):
        # Start the libcamera-vid process for live preview
        self.preview_process = subprocess.Popen(["libcamera-vid", "-t", "0", "--display", "0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def stop_preview(self):
        # Terminate the preview process
        if self.preview_process:
                self.preview_process.terminate()


def main():
    root = tk.Tk()
    app = MotorControlApp(root)
    root.mainloop()
    app.close()

if __name__ == "__main__":
    main()
