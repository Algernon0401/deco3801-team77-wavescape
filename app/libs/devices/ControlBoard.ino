// the setup routine runs once when you press reset:
void setup()
{
    // initialize serial communication at 9600 bits per second:
    Serial.begin(115200);

    // setup pins
    pinMode(A0, INPUT);
    pinMode(A1, INPUT);
    pinMode(A2, INPUT);
    pinMode(3, INPUT);
    pinMode(4, INPUT);
    pinMode(5, INPUT);
}

// the loop routine runs over and over again forever:
void loop()
{
    // read the input on analog and digital pins:
    Serial.print("A0:");
    Serial.print(analogRead(A0));
    Serial.print(";A1:");
    Serial.print(analogRead(A1));
    Serial.print(";A2:");
    Serial.print(analogRead(A2));
    Serial.print(";D3:");
    Serial.print(digitalRead(3));
    Serial.print(";D4:");
    Serial.print(digitalRead(4));
    Serial.print(";D5:");
    Serial.print(digitalRead(5));
    Serial.println();

    // print out the value you read:

    delay(10); // delay in between reads for stability
}
