from servo_controller import servo_controller
from led_controller import led_controller, colors
from time import sleep
import math
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

def test():
    sc = servo_controller()
    lc = led_controller()
    lc.set_eye_color(colors.red)
    sc.move_right_arm(90)
    sc.move_left_arm(90)
    sc.move_head(90)

    sleep(1)

    lc.set_eye_color(colors.green)
    sc.move_right_arm(0)
    sc.move_left_arm(0)
    sc.move_head(0)

    sleep(1)

    lc.set_eye_color(colors.blue)
    sc.move_right_arm(180)
    sc.move_left_arm(180)
    sc.move_head(180)

    sleep(1)

    lc.set_eye_color(colors.black)
    sc.move_right_arm(90)
    sc.move_left_arm(90)
    sc.move_head(90)
    lc.set_light_string(True)

    sleep(1)

    lc.set_light_string(False)

def test2():
    factory = PiGPIOFactory()
    right_arm_pin = 24
    servo = Servo(right_arm_pin, min_pulse_width=1/1000, max_pulse_width=2.5/1000, pin_factory=factory)
    while True:
        for i in range(0,360):
            servo.value = math.sin(math.radians(i))
            sleep(0.01)


if __name__ == '__main__':
    test2()