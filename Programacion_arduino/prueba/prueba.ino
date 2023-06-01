int altura_actual = 150;
String alt = "altura";
String serial;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){
    serial = Serial.readString();
    if(serial.compareTo(alt) == 0){
      Serial.print(altura_actual);
    }
  }
}
