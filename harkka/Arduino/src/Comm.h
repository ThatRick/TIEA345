#include <Arduino.h>

class Comm
{
  private:
    HardwareSerial &serial;
    
    char valueBuffer[32];
    unsigned short valueIndex = 0;
    bool gotValue = false;
    long value = 0;

    char paramBuffer[32];
    unsigned short paramIndex = 0;
    bool gotParam = false;
    char parameter[32];

  public:
    Comm(HardwareSerial &serial_)
    : serial(serial_)
    {}

    void init(unsigned long baudrate)
    {
        serial.begin(baudrate);
    }

    bool update()
    {
        if (serial.available() > 0)
        {
            char c = serial.read();
            if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z'))
            {
                paramBuffer[paramIndex++] = c;
            }
            else if ((c >= '0' && c <= '9') || c == '.' || c == '-') {
                valueBuffer[valueIndex++] = c;
            }
            else if (c == '\n')
            {
                gotValue = false;
                // get value
                if (valueIndex) {
                    valueBuffer[valueIndex] = '\0';
                    value = atoi(valueBuffer);
                    valueIndex = 0;
                    gotValue = true;
                }
                // get parameter
                if (paramIndex) {
                    paramBuffer[paramIndex] = '\0';
                    strncpy(parameter, paramBuffer, paramIndex+1);
                    // reset index counters
                    paramIndex = 0;
                    return true;
                }
            }
        }
        return false;
    }

    bool hasValue() { return gotValue; };

    long getValue() { return value; }

    char getParameter() { return parameter[0]; }

    void sendParam(String text, long value) {
        serial.print(text);
        serial.println(value);
    }

    void sendValue(long value) {
        serial.println(value);
    }

    void sendText(String text) {
        serial.print(text);
    }

    void sendTextLn(String text) {
        serial.println(text);
    }
};