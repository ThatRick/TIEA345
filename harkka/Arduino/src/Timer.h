/*
*   Simple timer class
*   by Markus Polvilampi
*/
class Timer
{
    unsigned long interval;
    unsigned long lastUpdate;

public:
    Timer(unsigned long interval, unsigned long millis) {
        this->interval = interval;
        this->lastUpdate = millis;
    }

    bool tick(unsigned long millis) {
        unsigned long elapsed = millis - lastUpdate;
        if (elapsed >= interval) {
            unsigned long overstep = elapsed - interval;
            lastUpdate = millis - overstep;
            return true;
        }
        return false;
    }
};