from guizero import App, Text, TextBox, PushButton, Slider, Box
import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import os
import dslrCapture as dslr


camera = PiCamera()
camera.resolution = (4056, 3040)
#camera.resolution = (3040, 3040)
#camera.resolution = (1024,768)
#camera.awb_mode = 'fluorescent'
#camera.awb_gains = 2.1
#camera.brightness = 54
#camera.contrast = 44
#camera.iso = 400
#camera.shutter_speed = 1000

path = os.getcwd()
print ("The current working directory is %s" % path)

objectName = "shot"

#Turntable
enablePin = 5
dirPin = 13
stepPin = 6

#DSLR Slider (Nema 17)
dslrEnablePin = 20
dslrDirPin = 12
dslrStepPin = 16

#Stack Rig Motor
in1_2 = 17
in2_2 = 27
in3_2 = 22
in4_2 = 23

dslrSliderPosition = 0
sliderPosition = 0
turnTablePosition = 0

sleepTime = 0.002 #time in between motor steps
#sleepTimeRotate = 0.01
nemaSleepTime = 0.001 #time between steps (Nema 17)
shotPause = 2 #time between motor moves and shots - to settle camera
dslrShotPause = 5

shotNumber = 1 #counter for naming shots in stack sequentially
stackNumber = 1 # counter for folder naming in full routine

cyclesRotation = 8 #number of PWM cycles for the turntable in one motion segment
cyclesLinear = 10 #number of PWM cycles for the focus rack in one motion segment 
dslrCyclesLinear = 10 #number of PWN cycles for the focus rack in one motion segment (Nema 17)

numberShots = 10 #number of shots in each stack
numberStacks = 70 #number of stacks in the routine

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(in1_2, GPIO.OUT)
GPIO.setup(in2_2, GPIO.OUT)
GPIO.setup(in3_2, GPIO.OUT)
GPIO.setup(in4_2, GPIO.OUT)

GPIO.setup(enablePin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(stepPin, GPIO.OUT)

GPIO.setup(dslrEnablePin, GPIO.OUT)
GPIO.setup(dslrDirPin, GPIO.OUT)
GPIO.setup(dslrStepPin, GPIO.OUT)

#Turntable Motion
def clockwise():
    global cyclesRotation
    segment = cyclesRotation
    print(segment)
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
    print(segment)
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
def dslrForward():
    global dslrCyclesLinear
    segment = dslrCyclesLinear
    print(segment)
    while (segment > 0):
        GPIO.output(dslrEnablePin, GPIO.LOW)
        GPIO.output(dslrDirPin, GPIO.HIGH)
        GPIO.output(dslrStepPin, GPIO.HIGH)
        time.sleep(nemaSleepTime)
        GPIO.output(dslrStepPin, GPIO.LOW)
        time.sleep(nemaSleepTime)
        segment -= 1
    disableMotors()
        
def dslrReverse():
    global dslrCyclesLinear
    segment = dslrCyclesLinear
    print(segment)
    while (segment > 0):
        GPIO.output(dslrEnablePin, GPIO.LOW)
        GPIO.output(dslrDirPin, GPIO.LOW)
        GPIO.output(dslrStepPin, GPIO.HIGH)
        time.sleep(nemaSleepTime)
        GPIO.output(dslrStepPin, GPIO.LOW)
        time.sleep(nemaSleepTime)
        segment -= 1
    disableMotors()

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
def zeroSlider():
    global sliderPosition
    sliderPosition = 0

def resetShotNumber():
    global shotNumber
    shotNumber = 1
    
def disableMotors():
    GPIO.output(in1_2, GPIO.LOW)
    GPIO.output(in2_2, GPIO.LOW)
    GPIO.output(in3_2, GPIO.LOW)
    GPIO.output(in4_2, GPIO.LOW)
    GPIO.output(enablePin, GPIO.HIGH)
    GPIO.output(dslrEnablePin, GPIO.HIGH)



def changeCyclesRotation(slider_value):
    global cyclesRotation
    cyclesRotation = int(slider_value)*9.4
    print("Your turntable will rotate in " + str(cyclesRotation/9.4) + " degree increments")
    
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


def shoot():
    global path
    global shotNumber
    print(shotNumber)
    if (shotNumber < 10):
        camera.capture(path + "/" + str(shotNumber) + ".jpg")
    else:
        camera.capture(path + "/" + str(shotNumber) + ".jpg")
    shotNumber += 1
    
def dslrTrigger():
    global shotNumber
    global objectName
    print(shotNumber)
    if (shotNumber < 10):
        dslr.take_picture(objectName.value + "/" + str(shotNumber) + ".jpg")
    else:
        dslr.take_picture(objectName.value + "/" + str(shotNumber) + ".jpg")
    shotNumber += 1
    
    
def goHome():
    global sliderPosition
    global cyclesLinear
    temp = cyclesLinear
    cyclesLinear = sliderPosition
    reverse()
    cyclesLinear = temp
    
def dslrGoHome():
    global dslrSliderPosition
    global dslrCyclesLinear
    temp = dslrCyclesLinear
    dslrCyclesLinear = dslrSliderPosition
    dslrReverse()
    dslrCyclesLinear = temp

def runStackRoutine():
    global camera
    camera.stop_preview
    camera.resolution = (4056,3040)
    global objectName
    global stackNumber
    path = objectName.value + "_" + str(stackNumber)
    os.mkdir(path)
    
    global numberShots
    for x in range(0,numberShots):
        shoot()
        time.sleep(shotPause)
        forward()
        time.sleep(shotPause)
    stackNumber += 1
    resetShotNumber()
    camera.resolution = (2592, 1944)
    
def dslrStack():
    global objectName
    global stackNumber
    path = objectName.value + "_" + str(stackNumber)
    #os.mkdir('/home/pi/Desktop/DSLR-photos/' + path)
    
    global numberShots
    for x in range(0,numberShots):
        dslrTrigger()
        time.sleep(dslrShotPause)
        dslrForward()
        time.sleep(dslrShotPause)
    stackNumber += 1
    resetShotNumber()
    
def runFullRoutine():
    global camera
    camera.resolution = (4056,3040)
    global numberStacks
    
    for x in range(0,numberStacks):
        runStackRoutine()
        clockwise()
        goHome()
    camera.resolution = (2592, 1944)
    
def camPreviewWindowed():
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
    
app = App(title="3D Scanner Companion", height="1000", width="400")


welcome_message = Text(app, text="Enter the name of your project:" )
objectName = TextBox(app, width=30)
spacer = Text(app, text="")
label = Text(app, text="AWB Gains")
Slider(app, command=changeAWBGains, start=0, end=80, width=300)
label = Text(app, text="Brightness")
Slider(app, command=changeBrightness, start=0, end=100, width=300)
label = Text(app, text="Contrast")
Slider(app, command=changeContrast, start=-100, end=100, width=300)
previewBox = Box(app, layout="grid")
PushButton(previewBox, command=camPreviewWindowed, text="Start Preview", grid=[0,0])
PushButton(previewBox, command=camera.stop_preview, text="Stop Preview", grid=[1,0])

spacer = Text(app, text="")


sliderBox = Box(app, layout="grid")
PushButton(sliderBox, command=forward, text="Camera Push", grid=[1,0])
PushButton(sliderBox, command=reverse, text="Camera Pull", grid=[0,0])

Slider(app, command=changeCyclesLinear, start=0, end=1000, width=300)
spacer = Text(app, text="Distance Between Shots in Stack")
Slider(app, command=changeNumberShots, start=0, end=150, width=300)
spacer = Text(app, text="# of Shots in Stack")
spacer = Text(app, text="")



actionBox = Box(app, layout="grid")
PushButton(actionBox, command=shoot, text="Take Shot", grid=[0,0])
PushButton(actionBox, command=zeroSlider, text="Zero Slider", grid=[1,0])
PushButton(actionBox, command=goHome, text="Go Home", grid=[2,0])
PushButton(actionBox, command=runStackRoutine, text="Shoot Stack", grid=[3,0])
          

spacer = Text(app, text="")

turntableBox = Box(app, layout="grid")
PushButton(turntableBox, command=clockwise, text="Turntable CW", grid=[1,0])
PushButton(turntableBox, command=counterClockwise, text="Turntable CCW", grid=[0,0])
Slider(app, command=changeCyclesRotation, start=0, end=360, width=300)
spacer = Text(app, text="Rotational Degrees Between Stacks")
Slider(app, command=changeNumberStacks, start=0, end=100, width=300)
spacer = Text(app, text="Number of Stacks in Routine")
spacer = Text(app, text="")

dslrSliderBox = Box(app, layout="grid")
PushButton(dslrSliderBox, command=dslrForward, text="DSLR Forward", grid=[1,0])
PushButton(dslrSliderBox, command=dslrReverse, text="DSLR Reverse", grid=[0,0])
PushButton(dslrSliderBox, command=dslrTrigger, text="Take DSLR photo", grid=[2,0])
Slider(app, command=changeDslrCyclesLinear, start=0, end=10000, width=300)
spacer = Text(app, text="Distance Between DSLR Positions")

PushButton(app, command=runFullRoutine, text="Run Full Routine")
PushButton(app, command=dslrStack, text="Run DSLR Stack")

app.display()