#include <Arduino.h>
#include <AccelStepper.h>
#include "Timer.h"
#include "Comm.h"

#define DIR_OUT 2
#define STEP_OUT 3
#define ENABLE_OUT 4
#define ENABLE_IN 6
#define MOVE_IN 7

#define MODE0_OUT 8
#define MODE1_OUT 9
#define MODE2_OUT 10

#define THROTTLE_OUT 11

#define MOTOR_STEPS 200
#define MAX_RATE 4000
#define MAX_MICRO_STEPS 32

int stepsPerRev;
float acceleration = 5;
float throttle = 0;

bool running = false;
short direction = 1;
bool enableButtonPrev = false;
bool moveButtonPrev = false;

Timer oncePerSecond(1000, millis());

AccelStepper stepper(AccelStepper::DRIVER, STEP_OUT, DIR_OUT);

Comm comm(Serial);


// Set acceleration (rev/s^2)
void setAcceleration(float value = acceleration) {
    acceleration = value;
    stepper.setAcceleration(acceleration * stepsPerRev);
}

// Set mode-outputs according to micro stepping value (1..32)
void setMicroSteps(int steps) {
    int table[6][3] = {
        {0, 0, 0},  // full step
        {1, 0, 0},  // half step
        {0, 1, 0},  // 1/4  step
        {1, 1, 0},  // 1/8  step
        {0, 0, 1},  // 1/16 step
        {1, 0, 1}   // 1/32 step
    };

    int index = log(steps) / log(2);
    digitalWrite(MODE0_OUT, table[index][0]);
    digitalWrite(MODE1_OUT, table[index][1]);
    digitalWrite(MODE2_OUT, table[index][2]);
}

// Set speed (rev/s) and micro stepping
void setMaxSpeed(float rps) {
    float maxRps = MAX_RATE / MOTOR_STEPS;
    if (rps > maxRps) rps = maxRps;

    int microSteps = MAX_MICRO_STEPS;
    while (microSteps * rps * MOTOR_STEPS > MAX_RATE) microSteps /= 2;

    setMicroSteps(microSteps);

    stepsPerRev = MOTOR_STEPS * microSteps;
    
    stepper.setMaxSpeed(rps * stepsPerRev);
    comm.sendParam("uS:", microSteps);
    setAcceleration();
}

// Set throttle control (0..100%)
void setThrottle(float value) {
    throttle = value;
    analogWrite(THROTTLE_OUT, 255 * (value / 100.0));
}

// Enable or disable stepper controller
void setEnabled(bool state)
{
    digitalWrite(ENABLE_OUT, !state);
}


// ================================
// **********   SETUP   ***********
// ================================
void setup()
{
    comm.init(9600);
    // Inputs
    pinMode(ENABLE_IN, INPUT_PULLUP);
    pinMode(MOVE_IN, INPUT_PULLUP);
    // Outputs
    pinMode(DIR_OUT, OUTPUT);
    pinMode(STEP_OUT, OUTPUT);
    pinMode(ENABLE_OUT, OUTPUT);
    pinMode(MODE0_OUT, OUTPUT);
    pinMode(MODE1_OUT, OUTPUT);
    pinMode(MODE2_OUT, OUTPUT);
    pinMode(THROTTLE_OUT, OUTPUT);

    setMaxSpeed(2);
}


// ================================
// ********   MAIN LOOP   *********
// ================================
void loop()
{
    unsigned long t = micros();
    bool enableButton = !digitalRead(ENABLE_IN); // internal pull-up used; signal reversed
    bool moveButton = !digitalRead(MOVE_IN);

    // local position control
    if (moveButton && !moveButtonPrev)
    {
        if (!running)
        {
            direction = (direction) ? 0 : 1;
            stepper.moveTo(1 * stepsPerRev * direction);
            setEnabled(true);
        }
        else
        {
            stepper.stop();
        }
    }

    enableButtonPrev = enableButton;
    moveButtonPrev = moveButton;

    // when position is reached, run() returns false and stepper control is disabled
    running = stepper.run();
    if (!running)
        setEnabled(false);

    // Receive serial data
    if (comm.update())
    {
        long value = comm.getValue();
        char param = comm.getParameter();

        // If parameter value given, set parameter to new value.
        // If only parameter name given, send back current parameter value.
        switch(param)
        {
            case 'p':   // Stepper position setpoint
            case 'P': {
                if (comm.hasValue()) {
                    // angle (deg) * 10 => absolute steps
                    long setpoint = floor(stepsPerRev * (value * 0.1 / 360.0f));
                    stepper.moveTo(setpoint);
                    setEnabled(true);
                } else {
                    // absolute steps => angle (deg) * 10
                    long pos = floor((stepper.currentPosition() / float(stepsPerRev)) * 3600);
                    comm.sendParam("P:", pos);
                }
                break;
            }
            case 's':   // Stepper max speed setpoint
            case 'S': {
                if (comm.hasValue()) 
                    setMaxSpeed(value * 0.1f);
                else {
                    comm.sendParam("S:", (stepper.maxSpeed() / stepsPerRev) * 10);
                }
                break;
            }
            case 'a':   // Stepper acceleration setpoint
            case 'A': {
                if (comm.hasValue())
                    setAcceleration(value * 0.1f);
                else
                    comm.sendParam("A:", acceleration * 10);
                break;
            }
            case 't':   // Throttle setpoint
            case 'T': {
                if (comm.hasValue())
                    setThrottle(value * 0.1f);
                else
                    comm.sendParam("T:", throttle * 10);
                break;
            }
        }
    }
}
