import serial
import time
import cv2
from picamera2 import Picamera2

# Set up the serial connection to the Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust the port name as needed
#time.sleep(2)  # Wait for the connection to initialize

def send_command(command):
    print(f"Sending command: {command}")
    ser.write(command.encode())
    #time.sleep(0.1)  # Small delay to ensure command is processed

# Initialize the cameraw
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1024,768)
picam2.preview_configuration.main.format = "RGB888"
picam2.start()

while True:
    # Capture frame-by-frame
    frame = picam2.capture_array()
    
    # Display the resulting frame
    cv2.imshow('Camera Feed', frame)
    
    # Check for key presses to control the robot
    key = cv2.waitKey(1) & 0xFF
    if key == ord('w'):
        send_command('F')  # Move forward
    elif key == ord('s'):
        send_command('B')  # Move backward
    elif key == ord('a'):
        send_command('L')  # Move left
    elif key == ord('d'):
        send_command('R')  # Move right
    elif key == ord('q'):
        send_command('K')
    elif key == ord('e'):
        send_command('M')
    elif key == ord('i'):
        send_command('I')
    elif key == ord('o'):
        send_command('D')
    elif key == ord('k'):
        send_command('J')
    elif key == ord('l'):
        send_command('H')
    else:
        send_command('S')  # Stop if no key is pressed
        
    if key == ord('1'):
        send_command('1')  # Speed level 1
    elif key == ord('2'):
        send_command('2')  # Speed level 2
    elif key == ord('3'):
        send_command('3')  # Speed level 3
    elif key == ord('4'):
        send_command('4')  # Speed level 4
    elif key == ord('0'):
        break  # Exit the loop

# Release the camera and close the serial connection
picam2.stop()
cv2.destroyAllWindows()
ser.close()
