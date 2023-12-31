import RPi.GPIO as GPIO
import time
LED_PIN_RED = 22
LED_PIN_GREEN = 17
LED_PIN_BLUE = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_RED, GPIO.OUT)
GPIO.setup(LED_PIN_GREEN, GPIO.OUT)
GPIO.setup(LED_PIN_BLUE, GPIO.OUT)

GPIO.output(LED_PIN_RED, GPIO.LOW) # led on
time.sleep(1)
GPIO.output(LED_PIN_RED, GPIO.HIGH) # led off

GPIO.output(LED_PIN_GREEN, GPIO.LOW) # led on
time.sleep(1)
GPIO.output(LED_PIN_GREEN, GPIO.HIGH) # led off

GPIO.output(LED_PIN_BLUE, GPIO.LOW) # led on
time.sleep(1)
GPIO.output(LED_PIN_BLUE, GPIO.HIGH) # led off


GPIO.output(LED_PIN_RED, GPIO.LOW) # led on
time.sleep(1)

GPIO.output(LED_PIN_GREEN, GPIO.LOW) # led on
time.sleep(1)


GPIO.output(LED_PIN_BLUE, GPIO.LOW) # led on
time.sleep(1)


GPIO.output(LED_PIN_RED, GPIO.HIGH) # led off
GPIO.output(LED_PIN_BLUE, GPIO.HIGH) # led off
GPIO.output(LED_PIN_GREEN, GPIO.HIGH) # led off
time.sleep(1)

GPIO.output(LED_PIN_RED, GPIO.LOW) # led on
GPIO.output(LED_PIN_GREEN, GPIO.LOW) # led on
GPIO.output(LED_PIN_BLUE, GPIO.LOW) # led on
time.sleep(1)

GPIO.output(LED_PIN_RED, GPIO.HIGH) # led off
GPIO.output(LED_PIN_BLUE, GPIO.HIGH) # led off
GPIO.output(LED_PIN_GREEN, GPIO.HIGH) # led off
x=0.02
for i in range(0,40):
    GPIO.output(LED_PIN_RED, GPIO.LOW) # led on
    time.sleep(x)
    GPIO.output(LED_PIN_RED, GPIO.HIGH) # led off
    time.sleep(x)

    GPIO.output(LED_PIN_BLUE, GPIO.LOW) # led on
    time.sleep(x)
    GPIO.output(LED_PIN_BLUE, GPIO.HIGH) # led off
    time.sleep(x)
    
    GPIO.output(LED_PIN_GREEN, GPIO.LOW) # led on
    time.sleep(x)
    GPIO.output(LED_PIN_GREEN, GPIO.HIGH) # led off
    time.sleep(x)
GPIO.cleanup()