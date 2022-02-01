# Basic Motor module just ot see if its working or not 


import RPi.GPIO as GPIO
from time import sleep 
# Using the common header naming 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Motor():
    def __init__(self, EnaA, EnaB, In1A, In2A, In1B, In2B):
        self.EnaA = EnaA
        self.EnaB = EnaB
        self.In1A = In1A
        self.In2A = In2A
        self.In1B = In1B
        self.In2B = In2B
        # setting up the pins to output pins 
        
        GPIO.setup(self.EnaA, GPIO.OUT)
        GPIO.setup(self.In1A, GPIO.OUT)
        GPIO.setup(self.In2A, GPIO.OUT)
        GPIO.setup(self.EnaB, GPIO.OUT)
        GPIO.setup(self.In1B, GPIO.OUT)
        GPIO.setup(self.In2B, GPIO.OUT)
        # Setting up the PWM pin this is used for providing the power to the motor 
        
        self.pwmA = GPIO.PWM(self.EnaA, 100)
        self.pwmA.start(0)
        self.pwmB = GPIO.PWM(self.EnaB, 100)
        self.pwmB.start(0)

    def move(self, t = 0, turn = 0, speed = 0.5):
        speed *= 100
        turn *= 100
        leftSpeed = speed - turn
        rightSpeed = speed + turn
        if leftSpeed > 100: 
            leftSpeed = 100
        elif leftSpeed < -100:
            leftSpeed = -100
        if rightSpeed > 100: 
            rightSpeed = 100
        elif rightSpeed < -100:
            rightSpeed = -100 
            
        
        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))
        
        if leftSpeed > 0:    
            GPIO.output(self.In1A, GPIO.LOW)
            GPIO.output(self.In2A, GPIO.HIGH)
        # Indicating it is in reverse 
        else:
            GPIO.output(self.In1A, GPIO.HIGH)
            GPIO.output(self.In2A, GPIO.LOW) 
            
        if rightSpeed > 0:
            GPIO.output(self.In1B, GPIO.LOW)
            GPIO.output(self.In2B, GPIO.HIGH)
        # Indicating it is in reverse         
        else:
            GPIO.output(self.In1B, GPIO.HIGH)
            GPIO.output(self.In2B, GPIO.LOW)
        sleep(t)
    
    def stop(self, t = 0):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        sleep(t)

       
# The naming conventions are as per Board scheme 







