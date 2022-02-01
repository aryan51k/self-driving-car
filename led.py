import Keyboard_controller as kc
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)

while True: # Run forever
    if kc.getKey('a'):
        GPIO.output(8, GPIO.HIGH)
    elif kc.getKey('b'):
        GPIO.output(8, GPIO.LOW)
