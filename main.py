from motor import Motor
from Image_Processing.video import get_curve
import Image_Processing.webcam as webcam
import cv2
import time

motor = Motor(32, 33, 11, 13, 15, 16) #Rpi pin defining arguments

def main():
    
    img = webcam.getImg(display=True)
    curve_val = get_curve(img, display=1)
    
    sen = 1.7 #sensitivity, controls the turning radius 
    max_val = 0.25 #keeps the curve value in limit
    v = 0.47 #turn
    
    if curve_val > max_val:
        curve_val = max_val #limitation
    
    if curve_val < -max_val:
        curve_val = -max_val #limitation
    
    if curve_val>0:
        #sen = 1.7
        if curve_val<=0.02:
            curve_val = 0 #for stability 
            v=0.47 #forward
            print("Adj-Fwd") #adjusted forward movement
        elif curve_val >= 0.2:
            curve_val = 0.17
            
            #time.sleep(1.5)
            #motor.stop(3)
            print("Max - left") #max pixels on the left
    elif curve_val == 0:
        v= 0.45
        print("fwd")
    else:
        if curve_val>-0.01: #0.02 for right
            curve_val = 0 #for stability 
            v=0.47 #forward
            print("Adj-Fwd")
        elif curve_val >= -0.01: #0.02 for right
            curve_val = -0.17
            #time.sleep(1)
            #motor.stop(1)
            print("Max - right") #max pixels on the right
    
    motor.move(0.1, -curve_val*sen, v)
    cv2.waitKey(1)
    

#driver code
if __name__ == "__main__":
    while True:
        main()
        
