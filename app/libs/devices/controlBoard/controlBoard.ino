// Pins
int button_pin = 13;
int pot_pin = A0;

void setup()
{

    // setup pins
    pinMode(pot_pin, INPUT);
    pinMode(button_pin, INPUT_PULLUP);

    // initialize serial communication at 9600 bits per second:
    Serial.begin(115200);
}

// the loop routine runs over and over again forever:
void loop()
{
    // read the input on analog and digital pins:
    Serial.print("A0:");
    Serial.print(analogRead(pot_pin));
    Serial.print(";D13:");
    Serial.print(!digitalRead(button_pin));
    Serial.println();

    // print out the value you read:

    delay(10); // delay in between reads for stability
}
