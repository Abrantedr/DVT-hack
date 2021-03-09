#define STANDARD_FRAME 8
byte buf[STANDARD_FRAME];

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.begin(115200);
  while(!Serial);       // Espera a que se establezca la comunicación
}
 
void loop() {
  // Nada aquí
}

void serialEvent() {
  if (Serial.readBytes(buf, STANDARD_FRAME)){
    if (Serial.availableForWrite() >= STANDARD_FRAME)
      Serial.write(buf, STANDARD_FRAME);
  }
}
