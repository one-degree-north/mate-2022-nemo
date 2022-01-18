//RESIGN

//init shite, to be changed
/*
 * header - up to rng later
 * command - 1 to whatever
 * params - whatever length, determined by command
 * footer - also up to rng later
 * 
 */
//LIS STUFF
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_LIS3DH.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

#include <Servo.h>
#include <Adafruit_DotStar.h>

//LIS STUFF
// Used for software SPI
#define LIS3DH_CLK 13
#define LIS3DH_MISO 12
#define LIS3DH_MOSI 11
// Used for hardware & software SPI
#define LIS3DH_CS 10
Adafruit_LIS3DH lis = Adafruit_LIS3DH();

//color stuff
uint32_t forwardThrusterColor = 0x0000FF;
uint32_t stillThrusterColor = 0xFFFFFF;
#define LEDDATAPIN    8
#define LEDCLOCKPIN   6
Adafruit_DotStar strip(1, LEDDATAPIN, LEDCLOCKPIN, DOTSTAR_BRG);

int motorPins[] = {};
int thrusterServoSpeeds[1] = {1500};
int regularServoSpeeds[1] = {90};
double currServoDeg = 0;

int HEADER = 85;
int FOOTER = 170;
int DEBUGHEADER = 120;
int DEBUGFOOTER = 121;
int params[5];
int currPacketIndex = 0;
int paramLength = 0;
int command;
unsigned long deltaTime;
unsigned long pastMicros;

Adafruit_BNO055 bnoIMU = Adafruit_BNO055(55);

int thrusterPin = 11;
int servoPin = 9;
Servo thrusterServo;
Servo regularServo;

bool validHeader = false;

int commandParamLength[] = {};

void setup(){
  thrusterServo.attach(thrusterPin);
  regularServo.attach(servoPin);
  Serial.begin(9600);

  strip.begin(); // Initialize pins for output
  strip.setBrightness(10);
  strip.show();  // Turn all LEDs off ASAP
  strip.setPixelColor(0, stillThrusterColor);
  strip.show();

  pastMicros = micros();

  bno.begin();
}

void loop(){
  //deltaTime = micros() - pastMicros;
  //unsigned long now = micros();
  //deltaTime = now - pastMicros;
  //pastMicros = now;
  
  unsigned long now = micros()
  deltaTime = now - pastMicros;
  pastMicros = now;
  
  readInputsDebug();
  moveThrusters();
  //moveServo();
  checkAccel();
  //pastMicros = micros();
  //digitalWrite(11, LOW);
  
}
void checkAccel(){
  sensors_event_t event;
  lis.getEvent(&event);
  //Serial.write(event.acceleration.x);
  //setServoSpeed(0, event.acceleration.x);
}
void moveThrusters(){
  //ONLY 1 motor for now, use motorPins when using more
  thrusterServo.writeMicroseconds(thrusterServoSpeeds[0]);
}

void moveServo(){
  currServoDeg += regularServoSpeeds[0] * (double) deltaTime / (double) 1000000;
  //modo for int!
  //Serial.println(currServoDeg);
  Serial.println(currServoDeg);
  //doule no modo sadde
  if (currServoDeg > 90){
    currServoDeg -= 90;
  }
  regularServo.write(currServoDeg);
}
void moveServoAbsolute(int newServoDeg){
  currServoDeg = newServoDeg;
  regularServo.write(currServoDeg);
}

//CURR SHITE

void readInputs2(bool validHeader){
  if (Serial.available()){
    if (!validHeader){
      //wait until valid header
      int input = Serial.read();
      if (input == HEADER){
        validHeader = true;
      }
    }
    else if (currPacketIndex == 0){
      command = Serial.read();
      //instead use a dictionary / map
      paramLength = commandParamLength[command];
      currPacketIndex++;
    }
    else if (currPacketIndex < paramLength + 1){
      int param = Serial.read();
      params[currPacketIndex - 1] = param;
      currPacketIndex++; 
    }
    else if (currPacketIndex >= paramLength + 1){
      currPacketIndex = 0;
      validHeader = false;
      int footer = Serial.read();
      if (footer == FOOTER){
        processCommand(command, params);
      }
    }
  }
}
void processCommand(int command, int params[]){
  switch(command){
  case 0:
    //Halt
    
  break;
  case 1:
    //setMotorSpeed
  
  break;
  case 2:
    //getTemp

  break;
  
  case 3:
    //getIMU
  break;

  case 4:
    //setAutoReport
  break;
  } 
}


void setThrusterSpeed(int thrusterServoNum, int speed){
  thrusterServoSpeeds[thrusterServoNum] = speed;
  //for now, testing 1 thruster
  //thrusterServo.writeMicroseconds(thrusterServoSpeeds[0]);
}
void setServoDeg(int servoNum, int deg){
  regularServoSpeeds[servoNum] = 0;
  currServoDeg = deg;
}
void setServoSpeed(int servoNum, int speed){
  regularServoSpeeds[servoNum] = speed;
}

//DEBUG SHITE

void readInputsDebug(){
  if (Serial.available()){
    if (!validHeader){
      //wait until valid header
      int input = Serial.read();
      if (input == DEBUGHEADER){
        validHeader = true;
        Serial.write("valid header\n");
      }
      else{
        Serial.write("invalid header\n");
      }
    }
    else if (currPacketIndex == 0){
      command = Serial.read();
      Serial.write("command: ");
      Serial.write(command);
      Serial.write("\n");
      paramLength = 5;
      currPacketIndex++;
    }
    else if (currPacketIndex < paramLength + 1){
      int param = Serial.read();
      params[currPacketIndex - 1] = param;
      Serial.write(" currPacketIndex: ");
      Serial.write(currPacketIndex);
      Serial.write("param: ");
      Serial.write(currPacketIndex-1);
      Serial.write(" value: ");
      Serial.write(param);
      Serial.write("\n");
      currPacketIndex++; 
    }
    else if (currPacketIndex >= paramLength + 1){
      currPacketIndex = 0;
      validHeader = false;
      int footer = Serial.read();
      if (footer == DEBUGFOOTER){
        Serial.write("valid footer");
        processCommandDebug(command, params);
      }
      else{
        Serial.write("invalid footer");
      }
    }
  }
}


void processCommandDebug(int command, int param[]){
  switch(command){
    case '0':
      Serial.write("com 0");
      //setServoSpeed(0, param[0]);
      moveServoAbsolute(90);
      //thrusterServo.writeMicroseconds(1550);
      break;
    case '1':
      Serial.write("com 1");
      moveServoAbsolute(0);
      break;
    case '2':
      Serial.write("com 2");
      setServoSpeed(0, 3);
      break;
    case '3':
      Serial.write("com 3");
      //setServoSpeed(s0, param[0]);
      setThrusterSpeed(0, 1450);
      //thrusterServo.writeMicroseconds(1550);
      break;
    case '4':
      Serial.write("com 4");
      setThrusterSpeed(0, 1500);
      strip.setPixelColor(0, stillThrusterColor);
      strip.show();
      break;
    case '5':
      Serial.write("com 5");
      //setThrusterSpeed(0, 1550);
      setThrusterSpeed(0, 1550);
      strip.setPixelColor(0, forwardThrusterColor);
      strip.show();
      break;
    case '6':
      Serial.write("come 6");
      regularServo.writeMicroseconds(1400);
      break;
    case '7':
      break;
    case '8':
      break;
    case '9':
      break;
  }
}
