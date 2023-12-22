import asyncio
import math
import threading
# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program

class servo:
    """
    A class that represents a servo motor.
    """
    MIN_VALUE = 2
    SCALE = 10

    pin: int
    servo: GPIO.PWM
    range_of_motion: int = 180
    current_angle: float = 0

    is_initialized: bool = False

    def __init__(self, pin, range_of_motion=180):
        """
        Initializes the servo object.

        Args:
            pin (int): The GPIO pin number to which the servo is connected.
            range_of_motion (int, optional): The range of motion of the servo in degrees. Defaults to 180.
        """
        self.pin = pin
        self.range_of_motion = range_of_motion
        GPIO.setup(self.pin, GPIO.OUT)
        self.servo = GPIO.PWM(self.pin, 50)
        self.servo.start(0)
        self.is_initialized = True

    def move(self, angle):
        """
        Moves the servo to the specified angle.

        Args:
            angle (float): The angle to which the servo should be moved.
        """
        if(self.is_initialized == False):
            raise Exception("servo not initialized")

        #self.move_servo(self.servo, angle)
        thread = threading.Thread(target=self.move_servo, args=(self.servo, angle)).start()

    def move_servo(self, servo, angle):
        """
        Moves the servo to the specified angle.

        Args:
            servo (GPIO.PWM): The PWM object representing the servo.
            angle (float): The angle to which the servo should be moved.
        """
        angle = min(angle, 179)
        angle = max(angle, 0)

        if(angle == self.current_angle):
            return
        
        z = abs(angle - self.current_angle) / self.range_of_motion
        z = max(z, 0.1)

        print("Moving servo to angle " + str(angle) + " with z = " + str(z))

        angle = angle / self.range_of_motion * self.SCALE + self.MIN_VALUE

        servo.ChangeDutyCycle(angle)
        sleep(z)
        servo.ChangeDutyCycle(0)

        self.current_angle = angle

class servo_controller:
    """
    A class that controls the servos connected to a Raspberry Pi using GPIO pins.
    """

    DEFAULT_RIGHT_ARM_PIN = 16
    DEFAULT_LEFT_ARM_PIN = 22
    DEFAULT_HEAD_PIN = 18
    SERVO_RANGE_OF_MOTION = 180

    right_arm: servo
    left_arm: servo
    head: servo

    is_initialized: bool = False

    def __init__(self, right_arm_pin=DEFAULT_RIGHT_ARM_PIN, left_arm_pin=DEFAULT_LEFT_ARM_PIN, head_pin=DEFAULT_HEAD_PIN):
        """
        Initializes the servo controller object.

        Args:
            right_arm_pin (int, optional): The GPIO pin number to which the right arm servo is connected. Defaults to 16.
            left_arm_pin (int, optional): The GPIO pin number to which the left arm servo is connected. Defaults to 18.
            head_pin (int, optional): The GPIO pin number to which the head servo is connected. Defaults to 22.
        """
        GPIO.setmode(GPIO.BOARD)

        self.right_arm = servo(right_arm_pin, self.SERVO_RANGE_OF_MOTION)
        self.left_arm = servo(left_arm_pin, self.SERVO_RANGE_OF_MOTION)
        self.head = servo(head_pin, self.SERVO_RANGE_OF_MOTION)

        self.is_initialized = True

    def move_right_arm(self, angle):
        """
        Moves the right arm servo to the specified angle.

        Args:
            angle (float): The angle to which the right arm servo should be moved.
        """
        self.right_arm.move(angle)
    
    def move_left_arm(self, angle):
        """
        Moves the left arm servo to the specified angle.

        Args:
            angle (float): The angle to which the left arm servo should be moved.
        """
        self.left_arm.move(self.SERVO_RANGE_OF_MOTION-angle)
    
    def move_head(self, angle):
        """
        Moves the head servo to the specified angle.

        Args:
            angle (float): The angle to which the head servo should be moved.
        """
        self.head.move(angle)

def test():
    sc = servo_controller()
    sc.move_right_arm(90)
    sc.move_left_arm(90)
    sc.move_head(90)
    sleep(1)
    sc.move_right_arm(0)
    sc.move_left_arm(0)
    sc.move_head(0)
    sleep(1)
    sc.move_right_arm(180)
    sc.move_left_arm(180)
    sc.move_head(180)
    sleep(1)
    sc.move_right_arm(90)
    sc.move_left_arm(90)
    sc.move_head(90)

if __name__ == '__main__':
    test()