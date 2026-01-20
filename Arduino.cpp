// C++ code
//
#include <Servo.h>

enum RadarState { SCANNING, TRACKING, LOST };
RadarState state = SCANNING;

const int DETECT_DISTANCE = 350; // Distance 350cm
const int MAX_ERROR = 15;        // Error 15 cm

int trackPosR = 0;   // Right servo
int trackPosL = 0;   // Left servo

Servo myservo1; // R
Servo myservo2; // L

int pos = 0;

const int trigPin1 = 3;
const int echoPin1 = 2;
const int trigPin2 = 13;
const int echoPin2 = 12;
const int trackSwitchPin = 6;

float duration;
const int maxfilyDistance = 50;

void setup()
{
  myservo1.attach(9);   // R
  myservo2.attach(8);   // L

  myservo1.write(0);
  myservo2.write(0);

  pinMode(trigPin1, OUTPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(echoPin2, INPUT);
  pinMode(trackSwitchPin, INPUT);

  Serial.begin(9600);
}

float sonarSearching1() {
  digitalWrite(trigPin1, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);

  duration = pulseIn(echoPin1, HIGH, 30000);
  if (duration == 0) return -1;

  float d = (duration * 0.0343) / 2;
  Serial.print("D1: ");
  Serial.println(d);
  return d;
}

float sonarSearching2() {
  digitalWrite(trigPin2, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);

  duration = pulseIn(echoPin2, HIGH, 30000);
  if (duration == 0) return -1;

  float d = (duration * 0.0343) / 2;
  Serial.print("D2: ");
  Serial.println(d);
  return d;
}

void scanMode() {
  for (pos = 0; pos <= 50; pos += 10) {
    myservo1.write(pos);
    myservo2.write(pos);
    delay(60);
    sonarSearching1();
    sonarSearching2();
  }

  for (pos = 50; pos >= 0; pos -= 10) {
    myservo1.write(pos);
    myservo2.write(pos);
    delay(60);
    sonarSearching1();
    sonarSearching2();
  }
}

void trackingMode() {
  static float prevAvgDist = -1;
  static unsigned long prevTime = 0;

  float d1 = sonarSearching1(); // R
  float d2 = sonarSearching2(); // L

  // Target lost
  if (d1 < 0 && d2 < 0) {
    state = LOST;
    return;
  }

  // Error too large > LOST
  if (d1 > 0 && d2 > 0 && abs(d1 - d2) > MAX_ERROR) {
    state = LOST;
    return;
  }

  // -- BOTH DETECTED
  if (d1 > 0 && d2 > 0) {

    float angle = getTargetAngle(d1, d2);
    int deltaR = trackPosL * 0.5;  // sensitivity
    int deltaL = trackPosR * 0.5;  // sensitivity

    // calibrate base on closer target
    if (d1 < d2) {
      // Right is closer → trust R
      trackPosL += deltaR;   // L move
    }
    else if (d2 < d1) {
      // Left is closer → trust L
      trackPosR += deltaL;   // R move
    }

    // speed calculation 
    float avgDist = (d1 + d2) / 2.0;
    unsigned long now = millis();

    if (prevAvgDist > 0) {
      float dt = (now - prevTime) / 1000.0;
      float speed = getTargetSpeed(prevAvgDist, avgDist, dt, angle);

      Serial.print("Angle: ");
      Serial.print(angle);
      Serial.print(" | Speed: ");
      Serial.println(speed);
    }

    prevAvgDist = avgDist;
    prevTime = now;
  }

  // === ONE SENSOR ONLY ===
  else if (d1 > 0) {
    // Right only
    trackPosL -= 2;
    trackPosR -= 2;
  }
  else if (d2 > 0) {
    // Left only
    trackPosR += 2;
    trackPosL += 2;
  }

  // limit
  trackPosR = constrain(trackPosR, 0, 50);
  trackPosL = constrain(trackPosL, 0, 50);

  myservo1.write(trackPosR); // R
  myservo2.write(trackPosL); // L

  delay(50);
}


void loop() {
  bool trackSwitch = digitalRead(trackSwitchPin);

  if (trackSwitch == HIGH) {
    state = TRACKING;
  }

  switch (state) {
    case SCANNING:
      if (trackSwitch == LOW) {
        scanMode();
      }
      break;

    case TRACKING:
      trackingMode();
      break;

    case LOST:
      if (trackSwitch == HIGH) {
        state = TRACKING;
      } else {
        state = SCANNING;
      }
      break;
  }
}

float getTargetAngle(float d1, float d2) {
  const float sensorGap = 15.0;
  float diff = d1 - d2;
  float theta = atan(diff / sensorGap);
  return theta * 180.0 / PI;
}

float getTargetSpeed(float prevDist, float currDist, float deltaTime, float angleDeg) {
  float angleRad = angleDeg * PI / 180.0;
  float deltaD = prevDist - currDist;
  float speed = deltaD / deltaTime;
  return speed * cos(angleRad);
}
