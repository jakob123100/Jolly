import RPi.GPIO as GPIO

class colors:
    red = (True, False, False)
    green = (False, True, False)
    blue = (False, False, True)
    yellow = (True, True, False)
    cyan = (False, True, True)
    magenta = (True, False, True)
    white = (True, True, True)
    black = (False, False, False)

class led_controller:
    
    DEFAULT_RED_PIN = 22
    DEFAULT_GREEN_PIN = 17
    DEFAULT_BLUE_PIN = 27
    
    DEFAULT_LIGHT_STRING_PIN = 12

    red_pin: int
    green_pin: int
    blue_pin: int

    is_initialized: bool = False

    def __init__(self, red_pin = DEFAULT_RED_PIN, green_pin = DEFAULT_GREEN_PIN, 
                 blue_pin = DEFAULT_BLUE_PIN, light_string_pin = DEFAULT_LIGHT_STRING_PIN):
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        self.light_string_pin = light_string_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)
        GPIO.setup(self.light_string_pin, GPIO.OUT)

        self.is_initialized = True
    
    def set_eye_color(self, color):
        if not self.is_initialized:
            raise Exception("led_controller not initialized")

        GPIO.output(self.red_pin, color[0])
        GPIO.output(self.green_pin, color[1])
        GPIO.output(self.blue_pin, color[2])
    
    def set_light_string(self, is_on):
        if not self.is_initialized:
            raise Exception("led_controller not initialized")

        if is_on:
            GPIO.output(self.DEFAULT_LIGHT_STRING_PIN, GPIO.LOW)
        else:
            GPIO.output(self.DEFAULT_LIGHT_STRING_PIN, GPIO.HIGH)