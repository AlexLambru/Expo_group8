#include <Wire.h>

// Define motor control pins
const int motorPins[4][3] = {
  {0, 1, 2},  // Motor 1: IN1, IN2, PWM
  {3, 4, 5},  // Motor 2: IN1, IN2, PWM
  {6, 7, -1}, // Motor 3: IN1, IN2, no PWM
  {8, 9, -1}  // Motor 4: IN1, IN2, no PWM
};

// I2C address
#define I2C_ADDRESS 0x08

void setup() {
  // Initialize I2C
  Wire.begin(I2C_ADDRESS);
  Wire.onReceive(receiveEvent);

  // Initialize motor control pins
  for (int i = 0; i < 4; ++i) {
    pinMode(motorPins[i][0], OUTPUT);
    pinMode(motorPins[i][1], OUTPUT);
    if (motorPins[i][2] != -1) {
      pinMode(motorPins[i][2], OUTPUT);
      analogWrite(motorPins[i][2], 0); // Set initial motor speed to 0
    }
  }
}

void loop() {
  // The loop function runs continuously, but we don't need to do anything here
  // because motor control is handled by the receiveEvent function.
}

void setMotorSpeed(int motorIndex, int speed) {
  int in1 = motorPins[motorIndex][0];
  int in2 = motorPins[motorIndex][1];
  int pwm = motorPins[motorIndex][2];

  if (speed > 0) {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    if (pwm != -1) analogWrite(pwm, speed);
  } else if (speed < 0) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    if (pwm != -1) analogWrite(pwm, -speed);
  } else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    if (pwm != -1) analogWrite(pwm, 0);
  }
}

void receiveEvent(int howMany) {
  if (howMany >= 3) {
    char motorId = Wire.read(); // First byte indicates the motor
    int speed = Wire.read() << 8; // Second and third bytes indicate speed
    speed |= Wire.read();

    int motorIndex = motorId - '1';
    if (motorIndex >= 0 && motorIndex < 4) {
      setMotorSpeed(motorIndex, speed);
    }
  }
}
