
import math
# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BOARD) # Sets the pin numbering system to use the physical layout

z=16
GPIO.setup(z,GPIO.OUT)   # Sets up pin z to an output (instead of an input)
ra = GPIO.PWM(z, 50)    # Sets up pin z as a PWM pin
ra.start(0)             # Starts running PWM on the pin and sets it to 0

z=18
GPIO.setup(z,GPIO.OUT)   # Sets up pin z to an output (instead of an input)
ha = GPIO.PWM(z, 50)      # Sets up pin z as a PWM pin
ha.start(0)               # Starts running PWM on the pin and sets it to 0

z=22
GPIO.setup(z,GPIO.OUT)   # Sets up pin z to an output (instead of an input)
la = GPIO.PWM(z, 50)    # Sets up pin z as a PWM pin
la.start(0)             # Starts running PWM on the pin and sets it to 0




# Move the servo back and forth
'''
p.ChangeDutyCycle(3)     # Changes the pulse width to 3 (so moves the servo)
sleep(1)                 # Wait 1 second
p.ChangeDutyCycle(10)    # Changes the pulse width to 12 (so moves the servo)
sleep(1)
'''

ra_y=0
la_y=0
ha_y=0

def right_arm(x,y):
    x=2+x*10
    if x != y:
        z=abs(x-y)/10
        if z<0.1:
            z=0.1
        print ("x,y,z",x,y,z)
        ra.ChangeDutyCycle(x)
        sleep(z)
        ra.ChangeDutyCycle(0)
        y=x
    return y

def left_arm(x,y):
    x=1-x
    x=2+x*10
    if x != y:
        z=abs(x-y)/10
        if z<0.1:
            z=0.1
        print ("x,y,z",x,y,z)
        la.ChangeDutyCycle(x)
        sleep(z)
        la.ChangeDutyCycle(0)
        y=x
    return y


def head(x,y):
    x=1-x
    x=2+x*10
    if x != y:
        z=abs(x-y)/10
        if z<0.1:
            z=0.1
        print ("x,y,z",x,y,z)
        ha.ChangeDutyCycle(x)
        sleep(z)
        ha.ChangeDutyCycle(0)
        y=x
    return y


i=0.0
while i<=1:
    x=i
    ra_y=right_arm(x,ra_y)
    la_y=left_arm(x,la_y)
    ha_y=head(x,ha_y)
    
    i=i+0.1
    sleep(0.5)



x=0.0
while True:
    x = float(input("right arm:")) /10
    ra_y=right_arm(x,ra_y)
    
    x = float(input("left arm:")) /10
    la_y=left_arm(x,la_y)
    
    x = float(input("head:")) /10
    ha_y=head(x,ha_y)


# Clean up everything
ra.stop()                 # At the end of the program, stop the PWM
la.stop()                 # At the end of the program, stop the PWM
ha.stop()                 # At the end of the program, stop the PWM
GPIO.cleanup()           # Resets the GPIO pins back to defaults
