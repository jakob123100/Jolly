import asyncio
import math
import threading
# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep, time   # Imports sleep (aka wait or pause) into the program
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

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
    movement_time: float = 10

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
        angle = min(angle, self.range_of_motion - 1)
        angle = max(angle, 0)

        if(angle == self.current_angle):
            return
        
        time_to_move = abs(angle - self.current_angle) / self.range_of_motion * self.movement_time + 0.1
        time_to_move = max(time_to_move, 0.1)

        print("Moving servo to angle " + str(angle) + " with z = " + str(time_to_move))

        angle = angle / self.range_of_motion * self.SCALE + self.MIN_VALUE

        for i in range(0, 10):
            servo.ChangeDutyCycle(angle)
            sleep(0.1)
            servo.ChangeDutyCycle(0)
            sleep(0.1)

        servo.ChangeDutyCycle(angle)
        sleep(time_to_move)
        servo.ChangeDutyCycle(0)

        self.current_angle = angle

class servo_controller:
    """
    A class that controls the servos connected to a Raspberry Pi using GPIO pins.
    """

    DEFAULT_RIGHT_ARM_PIN = 23
    DEFAULT_LEFT_ARM_PIN = 25
    DEFAULT_HEAD_PIN = 24
    SERVO_RANGE_OF_MOTION = 180

    right_arm: Servo
    left_arm: Servo
    head: Servo

    right_arm_angle: float = 0
    left_arm_angle: float = 0
    head_angle: float = 0

    is_initialized: bool = False

    def __init__(self, right_arm_pin=DEFAULT_RIGHT_ARM_PIN, left_arm_pin=DEFAULT_LEFT_ARM_PIN, head_pin=DEFAULT_HEAD_PIN):
        """
        Initializes the servo controller object.

        Args:
            right_arm_pin (int, optional): The GPIO pin number to which the right arm servo is connected. Defaults to 16.
            left_arm_pin (int, optional): The GPIO pin number to which the left arm servo is connected. Defaults to 18.
            head_pin (int, optional): The GPIO pin number to which the head servo is connected. Defaults to 22.
        """
        GPIO.setmode(GPIO.BCM)

        #self.right_arm = servo(right_arm_pin, self.SERVO_RANGE_OF_MOTION)
        #self.left_arm = servo(left_arm_pin, self.SERVO_RANGE_OF_MOTION)
        #self.head = servo(head_pin, self.SERVO_RANGE_OF_MOTION)
        
        factory = PiGPIOFactory()
        self.right_arm = Servo(right_arm_pin, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
        self.left_arm = Servo(left_arm_pin, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
        self.head = Servo(head_pin, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

        self.is_initialized = True
    
    def __move_servo(self, servo, angle):
        servo.value = angle/90 - 1
    
    def __smooth_move_over_time(self, servo, angle, duration):
        current_angle = servo.value
        angle_delta = angle/90 - (current_angle + 1)

        start_time = time()
        elapsed_time = 0
        
        # use sine function to make the movement smoother
        while elapsed_time < duration:
            elapsed_time = time() - start_time
            next_value = current_angle + \
                (math.sin(-math.pi/2 + elapsed_time / duration * math.pi) + 1) / 2 * angle_delta
            next_value = min(next_value, 1)
            next_value = max(next_value, -1)
            servo.value = next_value

        servo.value = angle/90 - 1

    def move_right_arm(self, angle, duration = 0):
        if duration > 0:
            self.__smooth_move_over_time(self.right_arm, angle, duration)
        else:
            self.__move_servo(self.right_arm, angle)

        self.right_arm_angle = angle
    
    def move_left_arm(self, angle, duration = 0):
        if duration > 0:
            self.__smooth_move_over_time(self.left_arm, 180 - angle, duration)
        else:
            self.__move_servo(self.left_arm, 180 -  angle)

        self.left_arm_angle = angle
    
    def move_head(self, angle, duration = 0):
        if duration > 0:
            self.__smooth_move_over_time(self.head, angle, duration)
        else:
            self.__move_servo(self.head, angle)

        self.head_angle = angle

def test():
    sc = servo_controller()
    sc.move_right_arm(0)
    sc.move_left_arm(0)
    sc.move_head(0)
    sleep(1)
    #sc.move_right_arm(90, 2)
    #sc.move_left_arm(90, 2)
    #sc.move_head(90, 2)
    #sleep(1)
    sc.move_right_arm(0, 2)
    sc.move_left_arm(0, 2)
    sc.move_head(0, 2)
    sleep(2)
    sc.move_right_arm(180, 2)
    sc.move_left_arm(180, 2)
    sc.move_head(180, 2)
    sleep(1)
    sc.move_right_arm(90, 2)
    sc.move_left_arm(90, 2)
    sc.move_head(90, 2)

if __name__ == '__main__':
    test()
