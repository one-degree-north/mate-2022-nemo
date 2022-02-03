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

//motor stuff
int thrusterPins[] = {5, 7, 9, 10, 11, 12};
Servo thrusterServos[6];

int clawPins[] = {9, 0};
Servo clawServos[2];


int thrusterServoSpeeds[1] = {1500};
int regularServoSpeeds[1] = {90};
double currServoDeg = 0;


int HEADER = 0xAB;
int FOOTER = 0xB3;
int DEBUGHEADER = 72;
int DEBUGFOOTER = 73;

int currParamNum = 0;
int currParamLength = 0;

int params[4];
int currPacketIndex = 0;
int command;
bool validHeader = false;

//sensor data
float orientationVector[3];
float temperature;

int sensorOutputDelays[5];
int sensorTimes[5];


int deltaTime;
unsigned long pastMicros;

Adafruit_BNO055 bnoIMU = Adafruit_BNO055(55);


void setup(){
  for (int i = 0; i < 6; i++){
    thrusterServos[i].attach(thrusterPins[i]);
  }

  for (int i = 0; i < 2; i++){
    clawServos[i].attach(clawPins[i]);
  }
  
  Serial.begin(9600);
  delay(10);

  strip.begin(); // Initialize pins for output
  strip.setBrightness(10);
  strip.show();  // Turn all LEDs off ASAP
  strip.setPixelColor(0, stillThrusterColor);
  strip.show();

  bnoIMU.begin();
  pastMicros = micros();
}

void loop(){
  unsigned long now = micros();
  deltaTime = now - pastMicros;
  pastMicros = now;
  sendSensorData();
  readInputs2();
  //readInputsDebug2();
}


//READING INPUTS AND EXECUTING COMMANDS

void readInputsDebug2(){
  if (Serial.available()){
    char input = Serial.read();
    if (input == '0'){
      float* currPos;
      sendOrientation();
    }
    if (input == '1'){
      float temp = getTemperature();
      Serial.println(temp);
    }
    else if (input == '2'){
      //imu::Vector<3> currAccel = getAccel();
      sendAccel();
    }
    else if (input == '3'){
      moveClaw(30);
    }

    else if (input == '4'){
      moveClaw(40);
    }
    else if (input == '5'){
      clawServos[0].write(40);
    }
    else if (input == '6')
      sendOrientation();

    else if (input == '7')
      sendTemperature();

    else if (input == '8')
      setAutoReport(0x1C, 1000);
    Serial.println("---");
  }
}


void readInputs2(){
  if (Serial.available()){
    if (!validHeader){
      //wait until valid header
      int input = Serial.read();
      if (input == HEADER){
        validHeader = true;
        currPacketIndex = 0;
        currParamLength = 0;
      }
      Serial.print("why");
    }
    else if (currPacketIndex == 0){
      command = Serial.read();
      currPacketIndex++;
      Serial.write(0x12);
    }
    else{
      int param = Serial.read();
      
      if (param == FOOTER){
        //execute com!
        processCommand(command, params, currParamLength);
        resetInputReading();
      }
      else if (currPacketIndex-1 >= 5){
        //too many params to be possible!
        
        resetInputReading();
        
      }
      params[currPacketIndex - 1] = param;
      currPacketIndex++;
      currParamLength++;
    }
  }
}

void resetInputReading(){
  currPacketIndex = 0;
  validHeader = false;
  //params = new int[5];
  currParamLength = 0;
  command = 0;
  
}

void sendSensorData(){
  for (int i = 0; i < 5; i++){
    int currDelay = sensorOutputDelays[i];
    if (currDelay == 0){
      continue;
    }
    sensorTimes[0] -= deltaTime;
    if (sensorTimes[0] <= 0){
      switch(i){
        case 0:
          //accel
          sendAccel();
        break;
        case 1:
          //temp
          sendTemperature();
        break;
        case 2:
          //orientation
          sendOrientation();
        break;
        case 3:
          //voltage
          sendVoltage();
        break;
      }
      sensorTimes[0] = currDelay;
    }
  }
}

void processCommand(int command, int params[], int currParamLength){
  //Serial.print("ayy processing com");
  switch(command){
  case 0x10:
    if (currParamLength == 0)
      halt();
    
  break;
  case 0x20:
    if (currParamLength == 2)
      moveThruster(params[0], params[1]);
    
  break;
  case 0x12:
    if (currParamLength == 0){
      //Serial.print("WOA");
      sendTemperature();
    }
  break;
  
  case 0x30:
    //getIMU
    if (currParamLength == 1){
      if (params[0] == 0x10)
        sendAccel();
      else if (params[1] == 0x12)
        sendOrientation();
    }
    
  break;

  case 0x50:
    //setAutoReport
    if (currParamLength == 2)
      setAutoReport(params[0], params[1]);
  break;
  } 
}




//COMMANDS

void sendOrientation(){
  int orientationValues[3];
  getOrientation(orientationValues);
  sendReturnPacket(0x1E, orientationValues[0], 0x00);
  sendReturnPacket(0x1E, orientationValues[1], 0x30);
  sendReturnPacket(0x1E, orientationValues[2], 0x60);
}

int* getOrientation(int orientationVector[]){
  sensors_event_t event;
  bnoIMU.getEvent(&event);
  
  orientationVector[0] = event.orientation.x;
  orientationVector[1] = event.orientation.y;
  orientationVector[2] = event.orientation.z;

  return orientationVector;
}

void sendTemperature(){
  int temperature = getTemperature();
  sendReturnPacket(0x1D, temperature);
}

float getTemperature(){
  sensors_event_t event;
  bnoIMU.getEvent(&event);
  return event.temperature;
}

void sendAccel(){
  int accelValues[3];
  getAccel(accelValues);
  sendReturnPacket(0x1C, accelValues[0], 0x00);
  sendReturnPacket(0x1C, accelValues[1], 0x30);
  sendReturnPacket(0x1C, accelValues[2], 0x60);
}

int* getAccel(int accelValues[]){
  imu::Vector<3> currAccel = bnoIMU.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);

  accelValues[0] = currAccel.x();
  accelValues[1] = currAccel.y();
  accelValues[2] = currAccel.z();
  return accelValues;
}

void sendReturnPacket(int sensorType, int sensorValue, int param){
  Serial.write(HEADER);
  Serial.write(sensorType);
  Serial.write(param);
  Serial.write(sensorValue);
  Serial.write(FOOTER);
}

void sendReturnPacket(int sensorType, int sensorValue){
  Serial.write(HEADER);
  Serial.write(sensorType);
  Serial.write(sensorValue);
  Serial.write(FOOTER);
}

void sendVoltage(){
  
}

void getVoltage(){

}

void halt(){
  //reset all motor functions
  
}

void moveThruster(int selectedThruster, int selectedSpeed){
  thrusterServos[selectedThruster].writeMicroseconds(selectedSpeed - 1600);
}

//in case claw cannot writemicroseconds
void moveClaw(int deg){
  clawServos[0].write(deg);
}

void getIMU(int selectedValue){
  if (selectedValue == 0x10){
  
  }
}

void setAutoReport(int selectedValue, int reportDelay){
  switch(selectedValue){
  case 0x1C:
    sensorOutputDelays[0] = reportDelay;
  break;

  case 0x1D:
    sensorOutputDelays[1] = reportDelay;
  break;

  case 0x1E:
    sensorOutputDelays[2] = reportDelay;
  break;

  case 0x1f:
    sensorOutputDelays[3] = reportDelay;
  break;
  }
}
