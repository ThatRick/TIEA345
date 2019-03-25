
//  Simple Timer class
//  tick returns true per given interval (ms). Must be called frequently.
//  by Markus Polvilampi 2019

class Timer
{
    unsigned long interval;
    unsigned long nextTickTime;

public:
    Timer(unsigned long interval, unsigned long millis) {
        this->interval = interval;
        this->nextTickTime = millis + interval;
    }

    bool tick(unsigned long millis) {
        if (millis >= nextTickTime) {
            unsigned long overstep = millis - nextTickTime;
            nextTickTime = millis + interval - overstep;
            return true;
        }
        return false;
    }
};