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

    digitalWrite(PIN_LED, 1);
    delay(500);
    digitalWrite(PIN_LED, 0);
    delay(500);
    digitalWrite(PIN_LED, 1);
    delay(500);
    digitalWrite(PIN_LED, 0);
    delay(500);

    return 0;
}
