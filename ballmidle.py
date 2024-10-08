import argparse
import sys
import time
import cv2
import mediapipe as mp
import serial
from picamera2 import Picamera2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from utils import visualize

# Set up the serial connection to the Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust the port name as needed

def send_command(command):
    print(f"Sending command: {command}")
    ser.write(command.encode())

# Global variables to calculate FPS
COUNTER, FPS = 0, 0
START_TIME = time.time()
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1024,768)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

def calculate_distance(detection):
    # Assuming the actual diameter of the sports ball is known (e.g., 22 cm for a soccer ball)
    actual_diameter = 6.30  # cm
    focal_length = 1024   # Example focal length in pixels, adjust based on your camera calibration

    # Calculate the perceived diameter in pixels
    perceived_diameter = detection.bounding_box.width

    # Calculate the distance using the formula: distance = (actual_diameter * focal_length) / perceived_diameter
    distance = (actual_diameter * focal_length) / perceived_diameter
    return distance

def run(model: str, max_results: int, score_threshold: float, 
        camera_id: int, width: int, height: int) -> None:
  """Continuously run inference on images acquired from the camera.

  Args:
    model: Name of the TFLite object detection model.
    max_results: Max number of detection results.
    score_threshold: The score threshold of detection results.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
  """
  
  # Visualization parameters
  row_size = 50  # pixels
  left_margin = 24  # pixels
  text_color = (0, 0, 0)  # black
  font_size = 1
  font_thickness = 1
  fps_avg_frame_count = 30

  detection_frame = None
  detection_result_list = []

  def save_result(result: vision.ObjectDetectorResult, unused_output_image: mp.Image, timestamp_ms: int):
      global FPS, COUNTER, START_TIME

      # Calculate the FPS
      if COUNTER % fps_avg_frame_count == 0:
          FPS = fps_avg_frame_count / (time.time() - START_TIME)
          START_TIME = time.time()

      detection_result_list.append(result)
      COUNTER += 1

  # Initialize the object detection model
  base_options = python.BaseOptions(model_asset_path=model)
  options = vision.ObjectDetectorOptions(base_options=base_options,
                                         running_mode=vision.RunningMode.LIVE_STREAM,
                                         max_results=max_results, score_threshold=score_threshold,
                                         result_callback=save_result)
  detector = vision.ObjectDetector.create_from_options(options)

  # Continuously capture images from the camera and run inference
  while True:
    im = picam2.capture_array()
    image = cv2.resize(im, (1024, 768))

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

    # Run object detection using the model.
    detector.detect_async(mp_image, time.time_ns() // 1_000_000)

    # Show the FPS
    fps_text = 'FPS = {:.1f}'.format(FPS)
    text_location = (left_margin, row_size)
    current_frame = image
    cv2.putText(current_frame, fps_text, text_location, cv2.FONT_HERSHEY_DUPLEX,
                font_size, text_color, font_thickness, cv2.LINE_AA)

    if detection_result_list:
        result = detection_result_list[0]
        for detection in result.detections:
                bbox = detection.bounding_box
                x_min, y_min = bbox.origin_x, bbox.origin_y
                x_max, y_max = x_min + bbox.width, y_min + bbox.height
                cv2.rectangle(current_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                label = f'{detection.categories[0].category_name} ({x_min}, {y_min})'
                cv2.putText(current_frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Calculate and display the distance
                distance = calculate_distance(detection)
                distance_text = f'Distance: {distance:.2f} cm'
                cv2.putText(current_frame, distance_text, (x_min, y_min - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
        detection_frame = current_frame
        detection_result_list.clear()

    if detection_frame is not None:
        cv2.imshow('object_detection', detection_frame)
        
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
    time.sleep(0.1)

  detector.close()
  cap.release()
  cv2.destroyAllWindows()
  ser.close()

def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Path of the object detection model.',
      required=False,
      default='best.tflite')
  parser.add_argument(
      '--maxResults',
      help='Max number of detection results.',
      required=False,
      default=5)
  parser.add_argument(
      '--scoreThreshold',
      help='The score threshold of detection results.',
      required=False,
      type=float,
      default=0.25)
  parser.add_argument(
      '--cameraId', help='Id of camera.', required=False, type=int, default=0)
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      type=int,
      default=1024)
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      type=int,
      default=768)
  args = parser.parse_args()

  run(args.model, int(args.maxResults),
      args.scoreThreshold, int(args.cameraId), args.frameWidth, args.frameHeight)

if __name__ == '__main__':
  main()
    