#include <wiringPi.h>

#define PIN_LED 26
#define PIN_PIR 20


void setup_io() {
    wiringPiSetupGpio();    // BCM numerointi

    pinMode(PIN_LED, OUTPUT);    // ledi
    pinMode(PIN_PIR, INPUT);     // liiketunnistin
}


int main(void) {
    setup_io();

    int prevState = digitalRead(PIN_PIR);
    
    while(1) {
        int state = digitalRead(PIN_PIR);
        if (state != prevState) {
            prevState = state;
            digitalWrite(PIN_LED, state);
        }
        delay(10);
    }

    return 0;
}
