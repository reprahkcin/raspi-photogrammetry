from guizero import App, Text, TextBox, PushButton, Slider, Box
import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import os #for file management, creating directories, etc.
import dslrCapture as dslr #gphoto2 module capture script


camera = PiCamera() #Make sure camera is enabled in preferences
camera.resolution = (4056, 3040)

#Uncomment to try out some of these settings, but ultimately automatic settings worked out better. 
#camera.resolution = (3040, 3040)
#camera.resolution = (1024,768)
#camera.awb_mode = 'fluorescent'
#camera.awb_gains = 2.1
#camera.brightness = 54
#camera.contrast = 44
#camera.iso = 400
#camera.shutter_speed = 1000

#grabs current path of the script
path = os.getcwd()
print ("The current working directory is %s" % path)

#default name of project
objectName = "shot"

#Turntable GPIO pins
enablePin = 5
dirPin = 13
stepPin = 6

#DSLR Slider (Nema 17) GPIO pins
dslrEnablePin = 20
dslrDirPin = 12
dslrStepPin = 16

forwardPin = 16
reversePin = 20

#Stack Rig Motor GPIO pins
in1_2 = 17
in2_2 = 27
in3_2 = 22
in4_2 = 23

#Light Control Pin (High to turn on)
lightPin = 21
lightsOn = False

#Global variables to keep track of positions
dslrSliderPosition = 0
sliderPosition = 0
turnTablePosition = 0

#Sleep and pauses
sleepTime = 0.002 #time in between motor steps PiCam stepper
nemaSleepTime = 0.001 #time between steps (Nema 17) turntable stepper (half-step microstepping)
nema2SleepTime = 0.0001 #DSLR stepper (40:1) reduction on the motor, half-step microstepping on the driver
shotPause = 2 #time between motor moves and shots - to settle camera
dslrShotPause = 5 #significantly longer to allow for file transfer, also, things are heavier and take more time to settle down

#Global counters -- apply to both PiCam and DSLR routines
shotNumber = 1 #counter for naming shots in stack sequentially
stackNumber = 1 # counter for folder naming in full routine
 
#Default Step Cycles and values
cyclesRotation = 8 #default number of PWM cycles for the turntable in one motion segment (change these with respective sliders)
cyclesLinear = 10 #default number of PWM cycles for the focus rack in one motion segment 
dslrCyclesLinear = 3 #default number of PWN cycles for the focus rack in one motion segment (Nema 17)

numberShots = 1 #default number of shots in each stack
numberStacks = 72 #default number of stacks in the routine

#GPIO setup
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

#PiCam stepper pin init
GPIO.setup(in1_2, GPIO.OUT)
GPIO.setup(in2_2, GPIO.OUT)
GPIO.setup(in3_2, GPIO.OUT)
GPIO.setup(in4_2, GPIO.OUT)

#Turntable pin init
GPIO.setup(enablePin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(stepPin, GPIO.OUT)

#DSLR slider pin init
#GPIO.setup(dslrEnablePin, GPIO.OUT)
#GPIO.setup(dslrDirPin, GPIO.OUT)
#GPIO.setup(dslrStepPin, GPIO.OUT)
GPIO.setup(reversePin, GPIO.OUT)
GPIO.setup(forwardPin, GPIO.OUT)
GPIO.output(reversePin, GPIO.LOW)
GPIO.output(forwardPin, GPIO.LOW)

#Lights Relay
GPIO.setup(lightPin, GPIO.OUT)

#Turntable Motion
def clockwise():
    global cyclesRotation
    segment = cyclesRotation
    print("Clockwise: " + str(segment/9.4) + " degrees")
    while (segment > 0):
        GPIO.output(enablePin, GPIO.LOW)
        GPIO.output(dirPin, GPIO.LOW)
        GPIO.output(stepPin, GPIO.HIGH)
        time.sleep(nemaSleepTime)
        GPIO.output(stepPin, GPIO.LOW)
        time.sleep(nemaSleepTime)
        segment -= 1
    disableMotors()
        
def counterClockwise():
    global cyclesRotation
    segment = cyclesRotation
    print("Counter-Clockwise: " + str(segment/9.4) + " degrees")
    while (segment > 0):
        GPIO.output(enablePin, GPIO.LOW)
        GPIO.output(dirPin, GPIO.HIGH)
        GPIO.output(stepPin, GPIO.HIGH)
        time.sleep(nemaSleepTime)
        GPIO.output(stepPin, GPIO.LOW)
        time.sleep(nemaSleepTime)
        segment -= 1
    disableMotors()

#DSLR Slider
def dslrForwardPWM():
    GPIO.output(dslrEnablePin, GPIO.LOW)
    GPIO.output(dslrDirPin, GPIO.HIGH)
    global dslrCyclesLinear
    segment = dslrCyclesLinear/10
    p = GPIO.PWM(dslrStepPin, 3000)
    p.start(50)
    time.sleep(segment)
    p.stop()
    disableMotors()


def dslrForward():
    global dslrCyclesLinear
    global dslrSliderPosition
    print("Current Position: " + str(dslrSliderPosition))
    dslrSliderPosition += dslrCyclesLinear
    segment = dslrCyclesLinear
    print("Slider Position: " + str(dslrSliderPosition))
    print("Moving Forward by: " + str(segment))
    while (segment > 0):
        GPIO.output(forwardPin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(forwardPin, GPIO.LOW)
        segment -= 1
        
def dslrReverse():
    global dslrCyclesLinear
    global dslrSliderPosition
    dslrSliderPosition -= dslrCyclesLinear
    segment = dslrCyclesLinear
    print("Slider Position: " + str(dslrSliderPosition))
    print("Moving in Reverse by: " + str(segment))
    while (segment > 0):
        GPIO.output(reversePin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(reversePin, GPIO.LOW)
        segment -= 1
    
# def dslrForward():
#     global dslrCyclesLinear
#     global dslrSliderPosition
#     dslrSliderPosition += dslrCyclesLinear
#     segment = dslrCyclesLinear
#     print("Slider Position: " + str(dslrSliderPosition))
#     print("Moving Forward by: " + str(segment))
#     while (segment > 0):
#         GPIO.output(dslrEnablePin, GPIO.LOW)
#         GPIO.output(dslrDirPin, GPIO.HIGH)
#         GPIO.output(dslrStepPin, GPIO.HIGH)
#         time.sleep(nema2SleepTime)
#         GPIO.output(dslrStepPin, GPIO.LOW)
#         time.sleep(nema2SleepTime)
#         segment -= 1
#     disableMotors()
#         
# def dslrReverse():
#     global dslrCyclesLinear
#     global dslrSliderPosition
#     dslrSliderPosition -= dslrCyclesLinear
#     segment = dslrCyclesLinear
#     print("Slider Position: " + str(dslrSliderPosition))
#     print("Moving in Reverse by: " + str(segment))
#     while (segment > 0):
#         GPIO.output(dslrEnablePin, GPIO.LOW)
#         GPIO.output(dslrDirPin, GPIO.LOW)
#         GPIO.output(dslrStepPin, GPIO.HIGH)
#         time.sleep(nema2SleepTime)
#         GPIO.output(dslrStepPin, GPIO.LOW)
#         time.sleep(nema2SleepTime)
#         segment -= 1
#     disableMotors()

#Raspberry Pi HQ Camera Slider
def forward():
    global cyclesLinear
    print("Your camera is moving forward in " + str(cyclesLinear) + " step increments")
    global sliderPosition
    sliderPosition += cyclesLinear
    segment = cyclesLinear
    print("Slider Position: " + str(sliderPosition))
    while (segment > 0):
        GPIO.output(in1_2, GPIO.HIGH)
        GPIO.output(in2_2, GPIO.LOW)
        GPIO.output(in3_2, GPIO.LOW)
        GPIO.output(in4_2, GPIO.LOW)
        time.sleep(sleepTime)
        GPIO.output(in1_2, GPIO.LOW)
        GPIO.output(in2_2, GPIO.HIGH)
        GPIO.output(in3_2, GPIO.LOW)
        GPIO.output(in4_2, GPIO.LOW)
        time.sleep(sleepTime)
        GPIO.output(in1_2, GPIO.LOW)
        GPIO.output(in2_2, GPIO.LOW)
        GPIO.output(in3_2, GPIO.HIGH)
        GPIO.output(in4_2, GPIO.LOW)
        time.sleep(sleepTime)
        GPIO.output(in1_2, GPIO.LOW)
        GPIO.output(in2_2, GPIO.LOW)
        GPIO.output(in3_2, GPIO.LOW)
        GPIO.output(in4_2, GPIO.HIGH)
        time.sleep(sleepTime)
        segment -= 1
    disableMotors()
    
def reverse():
    global cyclesLinear
    print("Your camera is moving in reverse in " + str(cyclesLinear) + " step increments")
    global sliderPosition
    sliderPosition -= cyclesLinear
    print("Slider Position: " + str(sliderPosition))
    segment = cyclesLinear
    while (segment > 0):
        GPIO.output(in1_2, GPIO.LOW)
        GPIO.output(in2_2, GPIO.LOW)
        GPIO.output(in3_2, GPIO.LOW)
        GPIO.output(in4_2, GPIO.HIGH)
        time.sleep(sleepTime)
        GPIO.output(in1_2, GPIO.LOW)
        GPIO.output(in2_2, GPIO.LOW)
        GPIO.output(in3_2, GPIO.HIGH)
        GPIO.output(in4_2, GPIO.LOW)
        time.sleep(sleepTime)
        GPIO.output(in1_2, GPIO.LOW)
        GPIO.output(in2_2, GPIO.HIGH)
        GPIO.output(in3_2, GPIO.LOW)
        GPIO.output(in4_2, GPIO.LOW)
        time.sleep(sleepTime)
        GPIO.output(in1_2, GPIO.HIGH)
        GPIO.output(in2_2, GPIO.LOW)
        GPIO.output(in3_2, GPIO.LOW)
        GPIO.output(in4_2, GPIO.LOW)
        time.sleep(sleepTime)
        segment -= 1
    disableMotors()


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
    
def disableMotors(): #Turns off the current to motors while they are not moving, decreases holding power, but keeps everything cool. *you should actually run this at boot, with the accompanying script
    GPIO.output(in1_2, GPIO.LOW)
    GPIO.output(in2_2, GPIO.LOW)
    GPIO.output(in3_2, GPIO.LOW)
    GPIO.output(in4_2, GPIO.LOW)
    GPIO.output(enablePin, GPIO.HIGH)
    #GPIO.output(dslrEnablePin, GPIO.HIGH)
    print("Motors are disabled")


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

#Main Functions

def shoot(): #PiCam - capture single photo
    global path
    global shotNumber
    print("PiCam shot #" + str(shotNumber))
    if (shotNumber < 10):
        camera.capture(path + "/0" + str(shotNumber) + ".jpg")
    else:
        camera.capture(path + "/" + str(shotNumber) + ".jpg")
    shotNumber += 1
    
def dslrTrigger(): #DSLR - triggers capture of single photo *calls out to gphoto2 script
    global path
    global shotNumber
    print("DSLR shot #" + str(shotNumber))
    if (shotNumber < 10):
        dslr.take_picture(path + "/0" + str(shotNumber) + ".jpg")
    else:
        dslr.take_picture(path + "/" + str(shotNumber) + ".jpg")
    shotNumber += 1
    
    
def goHome(): #PiCam slider moves back to 0
    global sliderPosition
    global cyclesLinear
    temp = cyclesLinear
    cyclesLinear = sliderPosition
    reverse()
    cyclesLinear = temp
    print("PiCam is moved back to HOME")
    
def dslrGoHome(): #DSLR slider moves back to 0
    global dslrSliderPosition
    global dslrCyclesLinear
    temp = dslrCyclesLinear
    dslrCyclesLinear = dslrSliderPosition
    dslrReverse()
    dslrCyclesLinear = temp
    print("DSLR is moved back to HOME")
    


def runStackRoutine(): #With current settings, 
    
    global objectName
    global stackNumber
    global path
    newPath = objectName.value + "_" + str(stackNumber)
    os.mkdir(newPath)
    path = newPath
    
    global numberShots
    for x in range(0,numberShots):
        shoot()
        time.sleep(shotPause)
        forward()
        time.sleep(shotPause)
    print("PiCam done with stack #" + str(stackNumber))
    stackNumber += 1
    resetShotNumber()
    
    
def dslrStack():
    
    global objectName
    global stackNumber
    global path
    newPath = objectName.value + "_" + str(stackNumber)
    os.mkdir(newPath)
    path = newPath
    #os.mkdir('/home/pi/Desktop/DSLR-photos/' + path)
    
    global numberShots
    for x in range(0,numberShots):
        dslrTrigger()
        time.sleep(dslrShotPause)
        dslrForward()
        time.sleep(dslrShotPause)
    print("DSLR done with stack #" + str(stackNumber))
    stackNumber += 1
    resetShotNumber()
    
def runFullRoutine():
    zeroSlider()
    global camera
    global numberStacks
    global numberShots
    print("PiCam Full Routine Started!")
    print(str(numberStacks)+" stacks of " + str(numberShots) + " shots")
    for x in range(0,numberStacks):
        runStackRoutine()
        clockwise()
        goHome()
        
def dslrRunFullRoutine():
    dslrZeroSlider()
    global numberStacks
    global numberShots
    print("DSLR Full Routine Started!")
    print(str(numberStacks)+" stacks of " + str(numberShots) + " shots")
    for x in range(0,numberStacks):
        dslrStack()
        clockwise()
        dslrGoHome()

        
    
    
def camPreviewWindowed(): #If the preview causes display issues, you can increase GPU memory or use a smaller PiCam Resolution
    camera.start_preview(fullscreen=False, window=(50,150,1024,576))
    
def camStopPreview():
    camera.stop_preview
    
def changeAWBGains(slider_value):
    global camera
    camera.awb_gains = float(slider_value)/10
    print("AWB Gains = " + str(slider_value))
    
def changeBrightness(slider_value):
    global camera
    camera.brightness = int(slider_value)
    print("Brightness = " + str(slider_value))
    
def changeContrast(slider_value):
    global camera
    camera.contrast = int(slider_value)
    print("Contrast = " + str(slider_value))

def toggleLights():
    global lightsOn
    if lightsOn:
        GPIO.output(lightPin, GPIO.LOW)
        lightsOn = False
    else:
        GPIO.output(lightPin, GPIO.HIGH)
        lightsOn = True

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
PushButton(previewButtonBox, command=camera.stop_preview, text="Stop PiCam Preview", grid=[1,0])

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

dslrHomeBox = Box(app, layout="grid")
PushButton(dslrHomeBox, command=dslrZeroSlider, text="Zero DSLR Slider", grid=[0,0])
PushButton(dslrHomeBox, command=dslrGoHome, text="Go Home", grid=[1,0])

dslrActionBox = Box(app, layout="grid")
PushButton(dslrActionBox, command=dslrTrigger, text="DSLR Shot", grid=[0,0])
PushButton(dslrActionBox, command=dslrStack, text="DSLR Stack", grid= [1,0])
PushButton(dslrActionBox, command=dslrRunFullRoutine, text="DSLR Full Routine", grid= [2,0])

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