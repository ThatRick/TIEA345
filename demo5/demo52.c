#include <wiringPi.h>

#define AUTO_R 4
#define AUTO_Y 5
#define AUTO_G 6
#define JALAN_R 13
#define JALAN_G 19
#define NAPPI 12


void setup_io() {
    wiringPiSetupGpio();    // BCM numerointi

    pinMode(AUTO_R, OUTPUT);
    pinMode(AUTO_Y, OUTPUT);
    pinMode(AUTO_G, OUTPUT);

    pinMode(JALAN_R, OUTPUT);
    pinMode(JALAN_G, OUTPUT);

    pinMode(NAPPI, INPUT);

    digitalWrite(AUTO_R, 0);
    digitalWrite(AUTO_Y, 0);
    digitalWrite(AUTO_G, 1);
    digitalWrite(JALAN_R, 1);
    digitalWrite(JALAN_G, 0);
}

void sekvenssi() {
    // autotien valot keltaisen kautta punaiseksi
    digitalWrite(AUTO_Y, 1);
    digitalWrite(AUTO_G, 0);
    delay(2000);
    digitalWrite(AUTO_R, 1);
    digitalWrite(AUTO_Y, 0);
    delay(3000);
    // jalankulkijan valot vihreaksi
    digitalWrite(JALAN_R, 0);
    digitalWrite(JALAN_G, 1);
    // jalankulkijan vihreä valo vilkkuu pari kertaa ennen vaihtumista punaiseksi
    delay(3000);
    digitalWrite(JALAN_G, 0);
    delay(500);
    digitalWrite(JALAN_G, 1);
    delay(500);
    digitalWrite(JALAN_G, 0);
    delay(500);
    digitalWrite(JALAN_G, 1);
    delay(500);
    // jalankulkijan valot punaiseksi
    digitalWrite(JALAN_R, 1);
    digitalWrite(JALAN_G, 0);
    delay(3000);
    // autotien valot keltaisen kautta vihreäksi
    digitalWrite(AUTO_Y, 1);
    delay(2000);
    digitalWrite(AUTO_R, 0);
    digitalWrite(AUTO_Y, 0);
    digitalWrite(AUTO_G, 1);
    // autotien valot vihreänä vähintään minimiajan
    delay(5000);
}

int main(void) {
    setup_io();

    while(1) {
        while(!digitalRead(NAPPI)) {
            delay(100);
        }
        sekvenssi();
    }

    return 0;
}
