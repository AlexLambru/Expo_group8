#include <Wire.h>

// Define motor control pins
#define MOTOR1_IN1 0
#define MOTOR1_IN2 1
#define MOTOR1_PWM 2
#define MOTOR2_IN1 3
#define MOTOR2_IN2 4
#define MOTOR2_PWM 5
#define MOTOR3_IN1 6
#define MOTOR3_IN2 7
#define MOTOR4_IN1 8
#define MOTOR4_IN2 9

// I2C address
#define I2C_ADDRESS 0x08

void setup() {
  // Initialize I2C
  Wire.begin(I2C_ADDRESS);
  Wire.onReceive(receiveEvent);

  // Initialize motor control pins
  pinMode(MOTOR1_IN1, OUTPUT);
  pinMode(MOTOR1_IN2, OUTPUT);
  pinMode(MOTOR1_PWM, OUTPUT);
  pinMode(MOTOR2_IN1, OUTPUT);
  pinMode(MOTOR2_IN2, OUTPUT);
  pinMode(MOTOR2_PWM, OUTPUT);
  pinMode(MOTOR3_IN1, OUTPUT);
  pinMode(MOTOR3_IN2, OUTPUT);
  pinMode(MOTOR4_IN1, OUTPUT);
  pinMode(MOTOR4_IN2, OUTPUT);

  // Set initial motor speed to 0
  analogWrite(MOTOR1_PWM, 0);
  analogWrite(MOTOR2_PWM, 0);
}

void loop() {
  // Nothing to do here, everything is handled in receiveEvent
}

void setMotorSpeed(int in1, int in2, int pwm, int speed) {
  if (speed > 0) {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    analogWrite(pwm, speed);
  } else if (speed < 0) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(pwm, -speed);
  } else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    analogWrite(pwm, 0);
  }
}

void receiveEvent(int howMany) {
  if (howMany >= 3) {
    char motorId = Wire.read(); // First byte indicates the motor
    int speed = Wire.read() << 8; // Second and third bytes indicate speed
    speed |= Wire.read();

    switch (motorId) {
      case '1':
        setMotorSpeed(MOTOR1_IN1, MOTOR1_IN2, MOTOR1_PWM, speed);
        break;
      case '2':
        setMotorSpeed(MOTOR2_IN1, MOTOR2_IN2, MOTOR2_PWM, speed);
        break;
      case '3':
        setMotorSpeed(MOTOR3_IN1, MOTOR3_IN2, -1, speed); // No PWM for motor 3
        break;
      case '4':
        setMotorSpeed(MOTOR4_IN1, MOTOR4_IN2, -1, speed); // No PWM for motor 4
        break;
    }
  }
}
