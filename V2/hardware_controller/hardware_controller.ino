const int pulPin1 = 2; // Pulse for motor 1
const int dirPin1 = 3; // Direction for motor 1
const int enablePin1 = 13; // Enable for motor 1
const int pulPin2 = 4; // Pulse for motor 2
const int dirPin2 = 5; // Direction for motor 2
const int enablePin2 = 12; // Enable for motor 2
const int limitSwitchFront = 6; // Front limit switch connected to pin 6
const int limitSwitchRear = 7; // Rear limit switch connected to pin 7

void setup() {
  Serial.begin(9600);
  pinMode(pulPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);
  pinMode(enablePin1, OUTPUT);
  pinMode(pulPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  pinMode(enablePin2, OUTPUT);
  pinMode(limitSwitchFront, INPUT_PULLUP);
  pinMode(limitSwitchRear, INPUT_PULLUP);

  disableMotors();
}

void loop() {
  if (Serial.available() > 0) {
    char motor = Serial.read(); // Read motor identifier ('1' or '2')
    int steps = Serial.parseInt(); // Read the number of steps
    char direction = Serial.read(); // Read the direction ('F' or 'B')

    if (motor == '1' || motor == '2') {
      enableMotors();
      moveStepper(motor, steps, direction);
      disableMotors();
    }
  }
}

void moveStepper(char motor, int steps, char direction) {
  int dirPin = (motor == '1') ? dirPin1 : dirPin2;
  int pulPin = (motor == '1') ? pulPin1 : pulPin2;
  int limitSwitch = (motor == '1') ? limitSwitchFront : limitSwitchRear;

  bool forwardDirection = (direction == 'F');
  digitalWrite(dirPin, forwardDirection ? HIGH : LOW);

  for (int i = 0; i < steps; i++) {
    if ((forwardDirection && digitalRead(limitSwitchFront) == LOW) || 
        (!forwardDirection && digitalRead(limitSwitchRear) == LOW)) {
      Serial.println("Motion stopped due to limit switch");
      break;
    }
    digitalWrite(pulPin, HIGH);
    delayMicroseconds(800); // Speed control
    digitalWrite(pulPin, LOW);
    delayMicroseconds(800); // Speed control
  }
}

void enableMotors() {
  digitalWrite(enablePin1, HIGH); // Enable motor 1
  digitalWrite(enablePin2, HIGH); // Enable motor 2
}

void disableMotors() {
  digitalWrite(enablePin1, LOW); // Disable motor 1
  digitalWrite(enablePin2, LOW); // Disable motor 2
}
