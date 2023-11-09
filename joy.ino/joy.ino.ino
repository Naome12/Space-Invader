int joyX, joyY;
void setup() {
  Serial.begin(9600);
}
void loop() {
  joyX = analogRead(A0); // Read X-axis
  joyY = analogRead(A1); // Read Y-axis
  // Read button states if available
  int buttonState = digitalRead(1); // Replace '2' with the actual pin number
  // Send data to the computer
  Serial.print(joyX);
  Serial.print(",");
  Serial.print(joyY);
  Serial.print(",");
  Serial.println(buttonState);
  delay(100); // Adjust the delay as needed
}