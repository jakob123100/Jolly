import servo_controller
import led_controller

def test():
    sc = servo_controller.servo_controller()
    lc = led_controller.led_controller()
    lc.set_eye_color(lc.colors.red)
    sc.move_right_arm(90)
    sc.move_left_arm(90)
    sc.move_head(90)
    lc.set_eye_color(lc.colors.green)
    sc.move_right_arm(0)
    sc.move_left_arm(0)
    sc.move_head(0)
    lc.set_eye_color(lc.colors.blue)
    sc.move_right_arm(180)
    sc.move_left_arm(180)
    sc.move_head(180)
    lc.set_eye_color(lc.colors.off)
    sc.move_right_arm(90)
    sc.move_left_arm(90)
    sc.move_head(90)
    lc.set_light_string(True)
    lc.set_light_string(False)

if __name__ == '__main__':
    test()