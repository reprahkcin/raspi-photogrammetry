import RPi.GPIO as GPIO

dslrEnablePin = 20
enablePin = 5

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(enablePin, GPIO.OUT)
GPIO.setup(dslrEnablePin, GPIO.OUT)


GPIO.output(enablePin, GPIO.HIGH)
GPIO.output(dslrEnablePin, GPIO.HIGH)