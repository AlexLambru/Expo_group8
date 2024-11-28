#include <Wire.h>
#include <SparkFun_TB6612.h>

// Motor pins (adjust these based on your wiring)
const int AIN1 = 12;  // Motor A IN1
const int AIN2 = 13;  // Motor A IN2
const int PWMA = 14;  // Motor A PWM
const int STBY = 15;  // Standby pin

const int BIN1 = 27;  // Motor B IN1
const int BIN2 = 26;  // Motor B IN2
const int PWMB = 25;  // Motor B PWM

// Create motor objects
Motor motorA = Motor(AIN1, AIN2, PWMA, STBY);
Motor motorB = Motor(BIN1, BIN2, PWMB, STBY);

// Additional motor pins
const int motorC_PIN1 = 16;
const int motorC_PIN2 = 17;

const int motorD_PIN1 = 18;
const int motorD_PIN2 = 19;

void setup() {
    Wire.begin(8);  // Join I2C bus with address #8
    Wire.onReceive(receiveEvent);  // Register event

    // Initialize motors
    motorA.begin();
    motorB.begin();
    pinMode(motorC_PIN1, OUTPUT);
    pinMode(motorC_PIN2, OUTPUT);
    pinMode(motorD_PIN1, OUTPUT);
    pinMode(motorD_PIN2, OUTPUT);
}

void loop() {
    delay(100);
}

void receiveEvent(int howMany) {
    String data = "";
    while (Wire.available()) {
        char c = Wire.read();
        data += c;
    }

    // Parse the received data
    data.trim();  // Remove any leading or trailing whitespace
    int dataCount = 6;  // Expecting six elements in the data string
    int values[dataCount];
    int startIndex = 0;
    int endIndex = 0;

    for (int i = 0; i < dataCount; i++) {
        endIndex = data.indexOf(',', startIndex);
        if (endIndex == -1) {
            endIndex = data.length();
        }
        values[i] = data.substring(startIndex, endIndex).toInt();
        startIndex = endIndex + 1;
    }

    // Extract values
    int r2 = values[0];
    int l2 = values[1];
    int buttonX = values[2];
    int buttonCircle = values[3];
    int buttonTriangle = values[4];
    int buttonSquare = values[5];

    // Control driving motors (Motor A and Motor B)
    motorA.drive(r2 - l2);
    motorB.drive(r2 - l2);

    // Control additional motor C (X for forward, Circle for backward)
    if (buttonX == 1) {
        digitalWrite(motorC_PIN1, HIGH);
        digitalWrite(motorC_PIN2, LOW);
    } else if (buttonCircle == 1) {
        digitalWrite(motorC_PIN1, LOW);
        digitalWrite(motorC_PIN2, HIGH);
    } else {
        digitalWrite(motorC_PIN1, LOW);
        digitalWrite(motorC_PIN2, LOW);
    }

    // Control additional motor D (Triangle for forward, Square for backward)
    if (buttonTriangle == 1) {
        digitalWrite(motorD_PIN1, HIGH);
        digitalWrite(motorD_PIN2, LOW);
    } else if (buttonSquare == 1) {
        digitalWrite(motorD_PIN1, LOW);
        digitalWrite(motorD_PIN2, HIGH);
    } else {
        digitalWrite(motorD_PIN1, LOW);
        digitalWrite(motorD_PIN2, LOW);
    }
}
