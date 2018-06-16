#include <SoftwareSerial.h>
SoftwareSerial RFID(2,3);
//pines 1 y 2 

int i;
int tag[14] = {2,48,66,48,48,53,53,65,57,57,54,54,49,3};

void setup(){
  
  RFID.begin(9600);
  Serial.begin(9600);
  }
  
void loop(){
  
  if (RFID.available()>0)
  {
    i = RFID.read();
    if (i != ' '){
      Serial.print(i,DEC);
    }
  }
}
