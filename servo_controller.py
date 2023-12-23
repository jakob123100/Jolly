import asyncio
import math
# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep, time   # Imports sleep (aka wait or pause) into the program
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from multiprocessing import Process


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

    __left_arm_process: Process = None
    __right_arm_process: Process = None
    __head_process: Process = None

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
            sleep(0.01)

        servo.value = angle/90 - 1

    def move_right_arm(self, angle, duration = 0):
        if duration > 0:
            self.__right_arm_process = Process(target=self.__smooth_move_over_time, args=(self.right_arm, angle, duration))
            self.__right_arm_process.start()
        else:
            self.__move_servo(self.right_arm, angle)

        self.right_arm_angle = angle
    
    def move_left_arm(self, angle, duration = 0):
        if duration > 0:
            self.__left_arm_process = Process(target=self.__smooth_move_over_time, args=(self.left_arm, 180 - angle, duration))
            self.__left_arm_process.start()
        else:
            self.__move_servo(self.left_arm, 180 -  angle)

        self.left_arm_angle = angle
    
    def move_head(self, angle, duration = 0):
        if duration > 0:
            self.__head_process = Process(target=self.__smooth_move_over_time, args=(self.head, angle, duration))
            self.__head_process.start()
        else:
            self.__move_servo(self.head, angle)

        self.head_angle = angle
    
    def wait_until_done(self):
        if self.__left_arm_process != None:
            self.__left_arm_process.join()
        if self.__right_arm_process != None:
            self.__right_arm_process.join()
        if self.__head_process != None:
            self.__head_process.join()
        
        sleep(0.1)

        self.__left_arm_process = None
        self.__right_arm_process = None
        self.__head_process = None

def test():
    sc = servo_controller()
    sc.move_right_arm(0)
    #sc.move_left_arm(0)
    #sc.move_head(0)

    sc.wait_until_done()

    sc.move_right_arm(180, 2)
    #sc.move_left_arm(180, 2)
    #sc.move_head(180, 2)

    sc.wait_until_done()
    
    sc.move_right_arm(90, 2)
    #sc.move_left_arm(90, 2)
    #sc.move_head(90, 2)

    sc.wait_until_done()

    sc.move_right_arm(0, 2)
    #sc.move_left_arm(0, 2)
    #sc.move_head(0, 2)

    sc.wait_until_done()

if __name__ == '__main__':
    test()
