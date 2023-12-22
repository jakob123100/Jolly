import RPi.GPIO as GPIO
import unittest
import time
from led_controller import led_controller, colors

class TestLedController(unittest.TestCase):

    def setUp(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.controller = led_controller()

    def tearDown(self):
        GPIO.cleanup()

    def test_initialization(self):
        self.assertTrue(self.controller.is_initialized)
        self.assertEqual(self.controller.red_pin, led_controller.DEFAULT_RED_PIN)
        self.assertEqual(self.controller.green_pin, led_controller.DEFAULT_GREEN_PIN)
        self.assertEqual(self.controller.blue_pin, led_controller.DEFAULT_BLUE_PIN)
        self.assertEqual(self.controller.light_string_pin, led_controller.DEFAULT_LIGHT_STRING_PIN)

    def test_set_eye_color(self):
        self.controller.set_eye_color(colors.red)
        self.assertTrue(GPIO.input(self.controller.red_pin))
        self.assertFalse(GPIO.input(self.controller.green_pin))
        self.assertFalse(GPIO.input(self.controller.blue_pin))

        time.sleep(1)

        self.controller.set_eye_color(colors.green)
        self.assertFalse(GPIO.input(self.controller.red_pin))
        self.assertTrue(GPIO.input(self.controller.green_pin))
        self.assertFalse(GPIO.input(self.controller.blue_pin))

        time.sleep(1)

        self.controller.set_eye_color(colors.blue)
        self.assertFalse(GPIO.input(self.controller.red_pin))
        self.assertFalse(GPIO.input(self.controller.green_pin))
        self.assertTrue(GPIO.input(self.controller.blue_pin))

    def test_set_light_string(self):
        self.controller.set_light_string(True)
        self.assertFalse(GPIO.input(self.controller.light_string_pin))

        time.sleep(1)

        self.controller.set_light_string(False)
        self.assertTrue(GPIO.input(self.controller.light_string_pin))

if __name__ == '__main__':
    unittest.main()