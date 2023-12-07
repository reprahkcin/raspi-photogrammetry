from guizero import App, Text, TextBox, PushButton, Slider, Box
import time
import subprocess
import os  # for file management, creating directories, etc.
from motor_controller import MotorController
from camera_controller import CameraController

# Initialize the motor controller and camera controller
mc = MotorController('/dev/ttyACM0', 9600)
camera = CameraController()
preview_process = None  # To keep track of the preview subprocess

# grabs current path of the script
path = os.getcwd()
print("The current working directory is %s" % path)

# default name of project
object_name = "shot"

# Global variables to keep track of positions
slider_position = 0
turntable_position = 0

# Sleep and pauses
shot_pause = 2  # time between motor moves and shots - to settle camera

# Global counters -- apply to both PiCam and DSLR routines
shot_number = 1  # counter for naming shots in stack sequentially
stack_number = 1  # counter for folder naming in full routine

# Constants
steps_per_revolution = 27118  # Motor 1
steps_per_cm = 6625          # Motor 2


def calculate_steps_motor1(degrees):
    steps = int((degrees / 360) * steps_per_revolution)
    return steps


def calculate_steps_motor2(distance_cm):
    steps = int(distance_cm * steps_per_cm)
    return steps


def move_motor(motor, steps, direction):
    mc.move_motor(motor, steps, direction)


def calculate_steps_rotation(degrees):
    steps = int((degrees / 360) * steps_per_revolution)
    return steps


def calculate_steps_linear(distance_cm):
    steps = int(distance_cm * steps_per_cm)
    return steps


def forward(steps):
    # Example values - you should adjust these based on your application's logic
    motor_id = '2'  # Motor 2 is the camera slider
    direction = 'F'  # Forward direction

    mc.move_motor(motor_id, steps, direction)


def backward(steps):
    # Example values - you should adjust these based on your application's logic
    motor_id = '2'  # Motor 2 is the camera slider
    direction = 'B'  # Forward direction

    mc.move_motor(motor_id, steps, direction)


def clockwise(steps):
    # Example values - you should adjust these based on your application's logic
    motor_id = '1'  # Motor 1 is the turntable
    direction = 'F'  # Forward direction

    mc.move_motor(motor_id, steps, direction)


def counter_clockwise(steps):
    # Example values - you should adjust these based on your application's logic
    motor_id = '1'  # Motor 1 is the turntable
    direction = 'B'  # Forward direction

    mc.move_motor(motor_id, steps, direction)


def close(self):
    self.mc.close()


def start_preview():
    global preview_process
    # Start the libcamera-vid process for live preview
    preview_process = subprocess.Popen(
        ["libcamera-vid", "-t", "0", "--display", "0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def stop_preview():
    global preview_process
    # Terminate the preview process
    if preview_process:
        preview_process.terminate()


def change_steps_rotation(slider_value):
    global steps_rotation
    steps_rotation = int(slider_value)
    print("Steps Rotation: " + str(steps_rotation))


def change_steps_linear(slider_value):
    global steps_linear
    steps_linear = int(slider_value)
    print("Steps Linear: " + str(steps_linear))


def zero_slider():
    global slider_position
    slider_position = 0
    print("The current position of the PiCam is now the home position")


def go_home():
    global slider_position
    slider_position = 0
    print("The current position of the PiCam is now the home position")
    move_motor('2', slider_position, 'B')


def shoot():
    global shot_number
    global stack_number
    global object_name
    global slider_position
    global turntable_position
    global shot_pause

    # Take a picture using libcamera-still
    image_filename = f"{object_name}_{shot_number}.jpg"
    # TODO: Add code to take a picture using libcamera-still

    print("Capturing image...", image_filename)


def run_stack_routine():
    global shot_number
    global stack_number
    global object_name
    global slider_position
    global turntable_position
    global shot_pause
    global number_shots

    # Create a folder for the current stack
    stack_folder = f"{object_name}_stack_{stack_number}"
    os.mkdir(stack_folder)

    # Take a picture using libcamera-still placed in the stack folder
    image_filename = f"{object_name}_{shot_number}.jpg"
    # TODO: Add code to take a picture using libcamera-still

    print("Running stack routine...")


def run_full_routine():
    global shot_number
    global stack_number
    global object_name
    global slider_position
    global turntable_position
    global shot_pause
    global number_shots
    global number_stacks

    # Create a folder for the current collection of stacks
    collection_folder = f"{object_name}_collection"
    os.mkdir(collection_folder)

    # Create a folder for the current stack in the collection folder
    stack_folder = f"{collection_folder}/{object_name}_stack_{stack_number}"
    os.mkdir(stack_folder)

    # Take a picture using libcamera-still placed in the stack folder
    image_filename = f"{object_name}_{shot_number}.jpg"
    # TODO: Add code to take a picture using libcamera-still

    print("Running full routine...")


# Default Step Cycles and values
# default number of PWM cycles for the turntable in one motion segment (change these with respective sliders)
steps_rotation = 8
steps_linear = 10  # default number of PWM cycles for the focus rack in one motion segment


def change_number_shots(slider_value):
    global numberShots
    numberShots = int(slider_value)
    print("Number of Shots in Stack: " + str(numberShots))


def change_number_stacks(slider_value):
    global numberStacks
    numberStacks = int(slider_value)
    print("Number of Stacks in Routine: " + str(numberStacks))


numberShots = 1  # default number of shots in each stack
numberStacks = 72  # default number of stacks in the routine

app = App(title="3D Scanner Companion", height="1000", width="550")


welcome_message = Text(app, text="Enter the name of your project:")
object_name = TextBox(app, width=50)
spacer = Text(app, text="")

previewBox = Box(app, layout="grid")

previewButtonBox = Box(app, layout="grid")
PushButton(previewButtonBox, command=start_preview,
           text="Start PiCam Preview", grid=[0, 0])
PushButton(previewButtonBox, command=stop_preview,
           text="Stop PiCam Preview", grid=[1, 0])

spacer = Text(app, text="")

Slider(app, command=change_steps_linear, start=0, end=1000, width=400)
spacer = Text(app, text="PiCam Movement Distance (in motor steps)")

sliderBox = Box(app, layout="grid")
PushButton(sliderBox, command=lambda: forward(steps_linear),
           text="PiCam Forward", grid=[1, 0])
PushButton(sliderBox, command=lambda: backward(steps_linear),
           text="PiCam Reverse", grid=[0, 0])

piCamHomeBox = Box(app, layout="grid")
PushButton(piCamHomeBox, command=zero_slider,
           text="Zero PiCam Slider", grid=[0, 0])
PushButton(piCamHomeBox, command=go_home, text="Go Home", grid=[1, 0])

piCamActionBox = Box(app, layout="grid")
PushButton(piCamActionBox, command=shoot, text="PiCam Shot", grid=[0, 0])
PushButton(piCamActionBox, command=run_stack_routine,
           text="PiCam Stack", grid=[1, 0])
PushButton(piCamActionBox, command=run_full_routine,
           text="PiCam Full Routine", grid=[2, 0])

spacer = Text(app, text="")

Slider(app, command=change_number_shots, start=0, end=150, width=400)
spacer = Text(app, text="# of Shots in Stack")

Slider(app, command=change_number_stacks, start=0, end=360, width=400)
spacer = Text(app, text="Number of Stacks in Routine")
spacer = Text(app, text="#Stacks * #Degrees = 360")


Slider(app, command=change_steps_rotation, start=0, end=360, width=400)
spacer = Text(app, text="Rotational Degrees Between Stacks")
turntableBox = Box(app, layout="grid")
PushButton(turntableBox, command=lambda: clockwise(
    steps_rotation), text="Turntable CW", grid=[1, 0])
PushButton(turntableBox, command=lambda: counter_clockwise(
    steps_rotation), text="Turntable CCW", grid=[0, 0])

app.display()
