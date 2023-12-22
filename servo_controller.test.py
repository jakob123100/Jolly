import RPi.GPIO as GPIO
import unittest
from servo_controller import servo, servo_controller
from time import sleep

class TestServo(unittest.TestCase):
    def setUp(self):
        GPIO.setmode(GPIO.BOARD)
        self.servo_pin = 18
        self.servo = servo(self.servo_pin)

    def tearDown(self):
        GPIO.cleanup()

    def test_servo_initialization(self):
        self.assertEqual(self.servo.pin, self.servo_pin)
        self.assertEqual(self.servo.range_of_motion, 180)
        self.assertEqual(self.servo.current_angle, 0)
        self.assertTrue(self.servo.is_initialized)

    def test_servo_move(self):
        angle = 90
        self.servo.move(angle)
        self.assertEqual(self.servo.current_angle, angle)

class TestServoController(unittest.TestCase):
    def setUp(self):
        GPIO.setmode(GPIO.BOARD)
        self.right_arm_pin = 16
        self.left_arm_pin = 18
        self.head_pin = 22
        self.servo_controller = servo_controller(self.right_arm_pin, self.left_arm_pin, self.head_pin)

    def tearDown(self):
        GPIO.cleanup()

    def test_servo_controller_initialization(self):
        self.assertEqual(self.servo_controller.right_arm.pin, self.right_arm_pin)
        self.assertEqual(self.servo_controller.left_arm.pin, self.left_arm_pin)
        self.assertEqual(self.servo_controller.head.pin, self.head_pin)
        self.assertTrue(self.servo_controller.is_initialized)

    def test_servo_controller_move_right_arm(self):
        angle = 90
        self.servo_controller.move_right_arm(angle)
        self.assertEqual(self.servo_controller.right_arm.current_angle, angle)

    def test_servo_controller_move_left_arm(self):
        angle = 90
        self.servo_controller.move_left_arm(angle)
        self.assertEqual(self.servo_controller.left_arm.current_angle, angle)
    
    def test_servo_controller_move_head(self):
        angle = 90
        self.servo_controller.move_head(angle)
        self.assertEqual(self.servo_controller.head.current_angle, angle)

if __name__ == '__main__':
    unittest.main()