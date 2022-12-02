#include <Servo.h>
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

int incoming[2];

void setup() {
  Serial.begin(115200);
  servo1.attach(2);
  servo2.attach(3);
  servo3.attach(4);
  servo4.attach(5);

  servo1.write(90);
  servo2.write(0);
  servo3.write(0);
  servo4.write(130);
}

void loop() {
  while(Serial.available() == 4){
    for (int i = 0; i < 4; i++){
      incoming[i] = Serial.read();
    }if(incoming[0] >= 30 && incoming[0] <= 170){
      servo1.write(incoming[0]);
    }if(incoming[1] <= 30){servo2.write(0);}
    if(incoming[1] > 30){servo2.write(35);}
    if(incoming[2] <= 65){
      servo3.write(incoming[2]);
    }if(incoming[3] <= 50){servo4.write(60);}
    if(incoming[3] > 50){servo4.write(130);}
    memset(incoming, 0, sizeof(incoming));
  }
}
