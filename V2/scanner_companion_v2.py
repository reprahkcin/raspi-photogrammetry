from guizero import App, Text, TextBox, PushButton, Slider, Box
import RPi.GPIO as GPIO
import time
import os #for file management, creating directories, etc.


#grabs current path of the script
path = os.getcwd()
print ("The current working directory is %s" % path)

#default name of project
objectName = "shot"


#Global variables to keep track of positions
sliderPosition = 0
turnTablePosition = 0

#Sleep and pauses
shotPause = 2 #time between motor moves and shots - to settle camera


#Global counters -- apply to both PiCam and DSLR routines
shotNumber = 1 #counter for naming shots in stack sequentially
stackNumber = 1 # counter for folder naming in full routine
 
#Default Step Cycles and values
cyclesRotation = 8 #default number of PWM cycles for the turntable in one motion segment (change these with respective sliders)
cyclesLinear = 10 #default number of PWM cycles for the focus rack in one motion segment 
dslrCyclesLinear = 3 #default number of PWN cycles for the focus rack in one motion segment (Nema 17)

numberShots = 1 #default number of shots in each stack
numberStacks = 72 #default number of stacks in the routine



def camPreviewWindowed(): #If the preview causes display issues, you can increase GPU memory or use a smaller PiCam Resolution
    print("camera.start_preview(fullscreen=False, window=(50,150,1024,576))")
    
def camStopPreview():
    print("camera.stop_preview")


   


#Interface Functions
def zeroSlider(): #Sets the current PiCam slider position as 'home'
    global sliderPosition
    sliderPosition = 0
    print("The current position of the PiCam is now the home position")
    
def dslrZeroSlider(): #Sets the current DSLR slider position as 'home'
    global dslrSliderPosition
    dslrSliderPosition = 0
    print("The current position of the DSLR is now the home position")
    
def resetShotNumber(): #Not used in UI -- used inside routine
    global shotNumber
    shotNumber = 1
    print("Shot count is reset to 1")
    


#UI Slider functions
def changeCyclesRotation(slider_value):
    global cyclesRotation
    print("Your turntable will rotate in " + str(cyclesRotation/ 9.4) + " degree increments")
    cyclesRotation = int(slider_value) * 9.4 # This value maps the turntable steps to = degrees
    
    
def changeCyclesLinear(slider_value):
    global cyclesLinear
    cyclesLinear = int(slider_value)
    print("Your camera will move in " + str(cyclesLinear) + " step increments")
    
def changeDslrCyclesLinear(slider_value):
    global dslrCyclesLinear
    dslrCyclesLinear = int(slider_value)
    print("Your camera will move in " + str(dslrCyclesLinear) + " step increments")

def changeNumberShots(slider_value):
    global numberShots
    numberShots = int(slider_value)
    print("You will shoot " + str(numberShots) + "shots in each stack")

def changeNumberStacks(slider_value):
    global numberStacks
    numberStacks = int(slider_value)
    print("You will shoot " + str(numberStacks) + " stacks")
    
    
app = App(title="3D Scanner Companion", height="1000", width="550")


welcome_message = Text(app, text="Enter the name of your project:" )
objectName = TextBox(app, width=50)
PushButton(app, command=toggleLights, text="Toggle Lights")
spacer = Text(app, text="")
#label = Text(app, text="AWB Gains")
#Slider(app, command=changeAWBGains, start=0, end=80, width=300)
previewBox = Box(app, layout="grid")
label = Text(previewBox, text="Brightness", width=10, grid=[0,2])
Slider(previewBox, command=changeBrightness, start=0, end=100, width=400, grid=[1,2])
label = Text(previewBox, text="Contrast", width=10, grid=[0,1])
Slider(previewBox, command=changeContrast, start=-100, end=100, width=400, grid=[1,1])
spacer = Text(app, text="")
previewButtonBox = Box(app, layout="grid")
PushButton(previewButtonBox, command=camPreviewWindowed, text="Start PiCam Preview", grid=[0,0])
PushButton(previewButtonBox, command=stopPreview, text="Stop PiCam Preview", grid=[1,0])

spacer = Text(app, text="")

Slider(app, command=changeCyclesLinear, start=0, end=1000, width=400)
spacer = Text(app, text="PiCam Movement Distance (in motor steps)")

sliderBox = Box(app, layout="grid")
PushButton(sliderBox, command=forward, text="PiCam Forward", grid=[1,0])
PushButton(sliderBox, command=reverse, text="PiCam Reverse", grid=[0,0])

piCamHomeBox = Box(app, layout="grid")
PushButton(piCamHomeBox, command=zeroSlider, text="Zero PiCam Slider", grid=[0,0])
PushButton(piCamHomeBox, command=goHome, text="Go Home", grid=[1,0])

piCamActionBox = Box(app, layout="grid")
PushButton(piCamActionBox, command=shoot, text="PiCam Shot", grid=[0,0])
PushButton(piCamActionBox, command=runStackRoutine, text="PiCam Stack", grid=[1,0])
PushButton(piCamActionBox, command=runFullRoutine, text="PiCam Full Routine", grid=[2,0])
          

spacer = Text(app, text="")
Slider(app, command=changeDslrCyclesLinear, start=0, end=100, width=400)
spacer = Text(app, text="DSLR Movement Distance (in motor steps, 1:40)")
dslrSliderBox = Box(app, layout="grid")
PushButton(dslrSliderBox, command=dslrForward, text="DSLR Forward", grid=[1,0])
PushButton(dslrSliderBox, command=dslrReverse, text="DSLR Reverse", grid=[0,0])


spacer = Text(app, text="")

Slider(app, command=changeNumberShots, start=0, end=150, width=400)
spacer = Text(app, text="# of Shots in Stack")

Slider(app, command=changeNumberStacks, start=0, end=360, width=400)
spacer = Text(app, text="Number of Stacks in Routine")
spacer = Text(app, text="#Stacks * #Degrees = 360")


Slider(app, command=changeCyclesRotation, start=0, end=360, width=400)
spacer = Text(app, text="Rotational Degrees Between Stacks")
turntableBox = Box(app, layout="grid")
PushButton(turntableBox, command=clockwise, text="Turntable CW", grid=[1,0])
PushButton(turntableBox, command=counterClockwise, text="Turntable CCW", grid=[0,0])



app.display()
