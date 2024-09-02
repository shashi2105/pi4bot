import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the servo
servo_pin = 3

# Set up the GPIO pin for output
GPIO.setup(servo_pin, GPIO.OUT)

# Set up PWM on the servo pin
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz frequency
pwm.start(0)

def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        # Test the servo by moving it to different angles
        set_angle(10)
        time.sleep(2)
        #set_angle(100)
        time.sleep(2)
        
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
