#include <Wire.h>
#include <AFMotor.h>

// Create the motor shield object with the default I2C address
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Connect a motor to port M1, M2, M3, & M4

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

int speed = 25; // Initial speed

void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud
 // AFMS.begin(); // Create with the default frequency 1.6KHz

  // Set all motors to stop
  motor1.setSpeed(0);
  motor2.setSpeed(0);
  motor3.setSpeed(0);
  motor4.setSpeed(0);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the incoming byte
    executeCommand(command);
  }
}

void executeCommand(char command) {
  switch (command) {
    case 'F': // Move forward
      moveForward();
      break;
    case 'B': // Move backward
      moveBackward();
      break;
    case 'L': // Move left
      moveLeft();
      break;
    case 'R': // Move right
      moveRight();
      break;
      case 'M': // Move right
      rotRight();
      break;
      case 'K': // Move left
      rotLeft();
      break;
      
    case '1': // Speed stage 1
      setSpeed(90);
      break;
    case '2': // Speed stage 2
      setSpeed(125);
      break;
    case '3': // Speed stage 3
      setSpeed(150);
      break;
    case '4': // Speed stage 4
      setSpeed(255);
      break;
    case 'S': // Stop
      stopMotors();
      break;
  }
}

void setSpeed(int newSpeed) {
  speed = newSpeed;
  motor1.setSpeed(speed);
  motor2.setSpeed(speed);
  motor3.setSpeed(speed);
  motor4.setSpeed(speed);
  Serial.print("Speed set to: ");
  Serial.println(speed);
}

void moveForward() {
  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}

void moveBackward() {
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}

void rotRight() {
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}

void rotLeft() {
  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}

void stopMotors() {
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
}

void moveRight() {
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}

void moveLeft() {
  motor1.run(BACKWARD);
  motor2.run(FORWARD);
  motor3.run(BACKWARD);
  motor4.run(FORWARD);
}
