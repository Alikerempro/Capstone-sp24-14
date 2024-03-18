#include <ArduinoJson.h>

const byte numChars = 64;
const int motorL_pin1 = 8;
const int motorL_pin2 = 7;
const int motorR_pin1 = 5;
const int motorR_pin2 = 4;

boolean connectd = false;
char receivedChars[numChars];
boolean newData = false;

JsonDocument docIn;
JsonDocument docOut;

/*
 * START OF PROGRAM
 */

void forward(int power){
  if(power > 0){
    digitalWrite(motorL_pin1, HIGH);
    digitalWrite(motorL_pin2, LOW);
    digitalWrite(motorR_pin1, LOW);
    digitalWrite(motorR_pin2, HIGH);
  }else if (power < 0){
    digitalWrite(motorL_pin1, LOW);
    digitalWrite(motorL_pin2, HIGH);
    digitalWrite(motorR_pin1, HIGH);
    digitalWrite(motorR_pin2, LOW);
  }else {
    digitalWrite(motorL_pin1, LOW);
    digitalWrite(motorL_pin2, LOW);
    digitalWrite(motorR_pin1, LOW);
    digitalWrite(motorR_pin2, LOW);
  }
}

void rotate(int power, int duration){
  
  forward(0);
  
  digitalWrite(motorL_pin1, LOW);
  digitalWrite(motorL_pin2, HIGH);
  digitalWrite(motorR_pin1, HIGH);
  digitalWrite(motorR_pin2, LOW);

  delay(duration);

  forward(0);
}

void recvData() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
    
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();
        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                Serial.println(receivedChars);
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void parseData() {
  if(newData){
    deserializeJson(docIn, receivedChars);
    if(docIn["id"] == "sp2414"){
      if(docIn["type"] == "move"){
        forward(docIn["dir"].as<float>());
      }else if(docIn["type"] == "turn"){
        rotate(docIn["dir"].as<float>(), docIn["dur"].as<float>()*1000);
      }else if(docIn["type"] == "sampler"){
  
      }
      newData = false;
    }
  }
}

void connectToPC() {
  while(connectd == false){
    recvData();
      
    deserializeJson(docIn, receivedChars);

    if(docIn["id"] == "sp2414")
      if(docIn["type"] == "connect"){
        docOut["good"] = 1;
        String serializedJSON = "";
        serializeJson(docOut, serializedJSON);
        Serial.println(serializedJSON);
        connectd = true;
      }
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);  
  Serial.println("Hello");

  pinMode(motorL_pin1, OUTPUT);
  pinMode(motorL_pin2, OUTPUT);
  pinMode(motorR_pin1, OUTPUT);
  pinMode(motorR_pin2, OUTPUT);
  
  forward(0);

  connectToPC();
  delay(500);
}

void loop() {
  // Serial Receiving/Handler Code
  recvData();
  parseData();
}
