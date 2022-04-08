int ledPin = 5;

void setup()
{
  pinMode(ledPin, OUTPUT);
}

void loop()
{
  flash(200); flash(200); flash(200);
  delay(300);
  flash(500); flash(500); flash(500);
  flash(200); flash(200); flash(200);
  delay(1000);
}

void flash(int duration)
{
  digitalWrite(ledPin, HIGH);
  delay(duration);
  digitalWrite(ledPin, LOW);
  delay(duration);
}
