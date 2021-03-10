#include <mcp2515.h>
#include <SPI.h>

#define STANDARD_FRAME 11
#define SERIAL_BAUDRATE 115200

// To CAN bus
struct can_frame msg, reply;
// To serial
byte buf[STANDARD_FRAME];
// MCP2515 Constructor
MCP2515 mcp2515(10);


// MCP2515::sendMessage() wrapper
MCP2515::ERROR send(canid_t can_id=0, __u8 can_dlc=0, __u8 data_0=0,
    __u8 data_1=0, __u8 data_2=0, __u8 data_3=0, __u8 data_4=0, __u8 data_5=0,
    __u8 data_6=0, __u8 data_7=0);


void setup() {

  cli();                          // Disable global interrupts
 
  // Start serial communication
  Serial.begin(SERIAL_BAUDRATE);
  while(!Serial);                 // Wait until port is open
  
  //  MCP2515 configuration
  /* These two lines cause USART transmission to fail */
  //mcp2515.reset();                            
  //mcp2515.setBitrate(CAN_1000KBPS, MCP_8MHZ);
  mcp2515.setNormalMode();
  
  // TIMER1 configuration
  // Overflow @65.54 ms
  TCCR1B = 0x00;                  // Stop the timer
  TCNT1  = 0;                     // Counter to zero
  TCCR1A = 0x00;                  // Normal operation
  TCCR1B |= (1 << CS11);          // Prescaler clkI/O/8
  TIMSK1 |= (1 << TOIE1);         // Enable overflow interrupts
  
  sei();                          // Enable global interrupts
}


void loop() {
  if (Serial.available() >= STANDARD_FRAME) {         // If a 11-byte frame has been sent (or more),
    Serial.readBytes(buf, STANDARD_FRAME);            // just read the first 11 bytes.

    /* Process message to interface with CAN bus */
    //send(buf[0] << 8 | buf[1], ...

    if (Serial.availableForWrite() >= STANDARD_FRAME) // Also, if we are able to send a message,  
      Serial.write(buf, STANDARD_FRAME);              // send it back.
  }
}


ISR(TIMER1_OVF_vect, ISR_BLOCK) { // Has to be less than 65 ms
  if (mcp2515.readMessage(&reply) == MCP2515::ERROR_OK) {
    Serial.print(reply.can_id, HEX);
    Serial.print(" "); 
    Serial.print(reply.can_dlc, HEX);
    Serial.print(" ");
    
    for (int i = 0; i < reply.can_dlc; i++) {
      Serial.print(reply.data[i], HEX);
      Serial.print(" ");
    }
 
    Serial.println();      
  }
}

/* Not compatible with SPI.beginTransaction()
 * as it disables external interrupts  0 and 1
 * (Tx and Rx pins for USART communication

void serialEvent() {
  if (Serial.readBytes(buf, STANDARD_FRAME)){
    if (Serial.availableForWrite() >= STANDARD_FRAME)
      Serial.write(buf, STANDARD_FRAME);
  }
}
*/
 
MCP2515::ERROR send(canid_t can_id=0, __u8 can_dlc=0, __u8 data_0=0,
    __u8 data_1=0, __u8 data_2=0, __u8 data_3=0, __u8 data_4=0, __u8 data_5=0,
    __u8 data_6=0, __u8 data_7=0) {
 
  msg.can_id  = can_id;
  msg.can_dlc = can_dlc;
  msg.data[0] = data_0;
  msg.data[1] = data_1;
  msg.data[2] = data_2;
  msg.data[3] = data_3;
  msg.data[4] = data_4;
  msg.data[5] = data_5;
  msg.data[6] = data_6;
  msg.data[7] = data_7;
 
  return mcp2515.sendMessage(&msg);
}
