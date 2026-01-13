// C++ code
//
#include <Servo.h>

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

void loop()
{
      for (pos = 0; pos <= 50; pos += 10) { // goes from 0 degrees to 180 degrees
    // in steps of 10 degree
    myservo1.write(pos);             // tell servo to go to position in variable 'pos'
    myservo2.write(pos);
    sonarSearching1();
	  sonarSearching2();
    delay(60);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 50; pos >= 0; pos -= 10) { // goes from 180 degrees to 0 degrees
    myservo1.write(pos);
    myservo2.write(pos);			// tell servo to go to position in variable 'pos'
    sonarSearching1();
	  sonarSearching2();
    delay(60);                       // waits 15ms for the servo to reach the position
  }
}

void sonarSearching1() {
    digitalWrite(trigPin1, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin1, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin1, LOW);

    duration = pulseIn(echoPin1, HIGH);
    distance = (duration*.0343)/2;
    Serial.print("Distance1: ");
    Serial.println(distance);
}

void sonarSearching2() {
    digitalWrite(trigPin2, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin2, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin2, LOW);

    duration = pulseIn(echoPin2, HIGH);
    distance = (duration*.0343)/2;
    Serial.print("Distance2: ");
    Serial.println(distance);
}
// tracking
void sonarTracking1() {
    digitalWrite(trigPin2, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin2, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin2, LOW);
	duration = pulseIn(echoPin2, HIGH);
    distance = (duration*.0343)/2;
    Serial.print("Distance2: ");
    Serial.println(distance);
    // If distance doesn't change start to move
  //  if(distance1 =! distance2){
    //}
  	//distance2 = (duration*.0343)/2;
}
