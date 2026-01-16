// C++ code
//
#include <Servo.h>

enum RadarState { SCANNING, TRACKING, LOST };
RadarState state = SCANNING;

const int DETECT_DISTANCE = 350; // Distance 350cm
const int MAX_ERROR = 15;        // Error 15 cm

int trackPos = 0;
Servo myservo1;
Servo myservo2; // create servo object to control a servo
int pos = 0;    // variable to store the servo position
const int trigPin1 = 3;  
const int echoPin1 = 2; 
const int trigPin2 = 13;  
const int echoPin2 = 12; 
float duration, distance;
const int maxfilyDistance = 350;

void setup()
{
    myservo1.attach(9);
  	myservo2.attach(8); // attaches the servo on pin 9 and 8 to the servo object
    myservo1.write(0);
	myservo2.write(0);
    pinMode(trigPin1, OUTPUT);   
    pinMode(trigPin2, OUTPUT);
  	pinMode(echoPin1, INPUT); 
	pinMode(echoPin2, INPUT);  
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

    float d1 = sonarSearching1();
    float d2 = sonarSearching2();

    if (d1 > 0 || d2 > 0) {
      trackPos = pos;
      state = TRACKING;
      return;
    }
  }

  for (pos = 50; pos >= 0; pos -= 10) {
    myservo1.write(pos);
    myservo2.write(pos);
    delay(60);

    float d1 = sonarSearching1();
    float d2 = sonarSearching2();

    if (d1 > 0 || d2 > 0) {
      trackPos = pos;
      state = TRACKING;
      return;
    }
  }
}

void trackingMode() {
  static float prevAvgDist = -1;
  static unsigned long prevTime = 0;

  float d1 = sonarSearching1();
  float d2 = sonarSearching2();

  // Tratget lost
  if (d1 < 0 && d2 < 0) {
    state = LOST;
    return;
  }

  // Error occured(make it execption)
  if (d1 > 0 && d2 > 0 && abs(d1 - d2) > MAX_ERROR) {
    state = LOST;
    return;
  }

  // Calibrate angle
  if (d1 > 0 && d2 > 0) {
    float angle = getTargetAngle(d1, d2);

    // Angle --> servo
    trackPos += angle * 0.5; // censitive (0.3~0.7)

    // calculate speed (optional idk)
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
  // when sonar 2 lost target
  else if (d1 > 0) {
    trackPos -= 2; // left
  }
  // when sonar 1 lost target
  else if (d2 > 0) {
    trackPos += 2; // right
  }

  // servo limit
  trackPos = constrain(trackPos, 0, 50);

  myservo1.write(trackPos);
  myservo2.write(trackPos);

  delay(50);
}


void loop() {
  switch (state) {

    case SCANNING:
      scanMode();
      break;

    case TRACKING:
      trackingMode();
      break;

    case LOST:
      state = SCANNING;
      break;
  }
}

float getTargetAngle(float d1, float d2) {
  const float sensorGap = 15.0; // cm

  float diff = d1 - d2;
  float theta = atan(diff / sensorGap); // radian

  return theta * 180.0 / PI; // degree
}

float getTargetSpeed(float prevDist, float currDist, float deltaTime, float angleDeg) {
  float angleRad = angleDeg * PI / 180.0;

  float deltaD = prevDist - currDist; // when approching -> speed +
  float speed = deltaD / deltaTime;   // cm/s

  // Horizontal speed calculate
  return speed * cos(angleRad);
}
