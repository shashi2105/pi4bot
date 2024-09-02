import RPi.GPIO as GPIO
import time
import math

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for the servos
servo_z_pin = 3
servo_y_pin = 2
servo_gripper_pin = 4

# Set up the GPIO pins as output
GPIO.setup(servo_z_pin, GPIO.OUT)
GPIO.setup(servo_y_pin, GPIO.OUT)
GPIO.setup(servo_gripper_pin, GPIO.OUT)

# Set up PWM for the servos
pwm_z = GPIO.PWM(servo_z_pin, 50)  # 50Hz frequency
pwm_y = GPIO.PWM(servo_y_pin, 50)
pwm_gripper = GPIO.PWM(servo_gripper_pin, 50)

# Start PWM with a duty cycle of 0 (servos in neutral position)
pwm_z.start(0)
pwm_y.start(0)
pwm_gripper.start(0)

def set_angle(pwm, angle):
    duty = angle / 18 + 2
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    pwm.ChangeDutyCycle(0)

def inverse_kinematics(y, z, l1, l2):
    # Calculate the angles using inverse kinematics
    d = math.sqrt(y**2 + z**2)
    if d > (l1 + l2):
        raise ValueError("Target is out of reach")
    
    theta2 = math.acos((d**2 - l1**2 - l2**2) / (2 * l1 * l2))
    theta1 = math.atan2(z, y) - math.atan2(l2 * math.sin(theta2), l1 + l2 * math.cos(theta2))
    
    return math.degrees(theta1), math.degrees(theta2)

try:
    while True:
        # Example coordinates
        y = 0
        z = 0
        l1 = 15  # Length of the first arm segment
        l2 = 15	  # Length of the second arm segment
        
        theta1, theta2 = inverse_kinematics(y, z, l1, l2)
        
        set_angle(pwm_z, theta1)  # Move along z-axis
        set_angle(pwm_y, theta2)  # Move along y-axis
        set_angle(pwm_gripper, 30)  # Close gripper
        time.sleep(2)
        
        y = 5
        z = 15
        theta1, theta2 = inverse_kinematics(y, z, l1, l2)
        
        set_angle(pwm_z, theta1)  # Move along z-axis
        set_angle(pwm_y, theta2)  # Move along y-axis
        set_angle(pwm_gripper, 0)  # Open gripper
        time.sleep(2)

except KeyboardInterrupt:
    pass

# Clean up GPIO
pwm_z.stop()
pwm_y.stop()
pwm_gripper.stop()
GPIO.cleanup()
