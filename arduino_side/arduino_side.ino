#include <mcp2515.h>
#include <SPI.h>

#define STANDARD_FRAME (11)
#define SERIAL_BAUDRATE (115200)
#define SERIAL_TIMEOUT (50)
#define CHIP_SELECT (10)

// To CAN bus
struct can_frame msg, reply;

// To serial
byte buf[STANDARD_FRAME];
byte rep[STANDARD_FRAME];

// MCP2515 Constructor
MCP2515 mcp2515(CHIP_SELECT);


// MCP2515::sendMessage() wrapper declaration
MCP2515::ERROR send(canid_t can_id=0, __u8 can_dlc=0, __u8 data_0=0,
    __u8 data_1=0, __u8 data_2=0, __u8 data_3=0, __u8 data_4=0, __u8 data_5=0,
    __u8 data_6=0, __u8 data_7=0);


void setup() {

  cli();                              // Disable global interrupts
 
  // Start serial communication
  Serial.begin(SERIAL_BAUDRATE);
  Serial.setTimeout(SERIAL_TIMEOUT);  // Timeout serial read
  while(!Serial);                     // Wait until port is open
  
  //  MCP2515 configuration
  mcp2515.reset();                            
  mcp2515.setBitrate(CAN_500KBPS, MCP_8MHZ);
  mcp2515.setNormalMode();

  // TIMER1 configuration
  // Overflow @65.54 ms
  /*
  TCCR1B = 0x00;                  // Stop the timer
  TCNT1  = 0;                     // Counter to zero
  TCCR1A = 0x00;                  // Normal operation
  TCCR1B |= (1 << CS11);          // Prescaler clkI/O/8
  TIMSK1 |= (1 << TOIE1);         // Enable overflow interrupts
  */

  sei();                          // Enable global interrupts
}


void loop() {
  if (mcp2515.readMessage(&reply) == MCP2515::ERROR_OK) {
    rep[0] = reply.can_id >> 8;     // Extract COB-ID msb
    rep[1] = reply.can_id & 0xFF;   // Extract COB-ID lsb
    rep[2] = reply.can_dlc;         // Extract data length
    /*  Extract data bytes */
    for (int i = 0; i < reply.can_dlc; ++i) {
      rep[i + 3] = reply.data[i];
    }

    /* Sends latest captured CAN message */
    if (Serial.availableForWrite() >= STANDARD_FRAME)
      Serial.write(rep, STANDARD_FRAME);
  }
}

// Not an ISR, it's called at the top of loop() function
void serialEvent() {
  // Blocks until we have read STANDARD_FRAME bytes or timeout
  if (Serial.readBytes(buf, STANDARD_FRAME))
    send(buf[0] << 8 | buf[1], buf[2], buf[3], buf[4], buf[5], buf[6], buf[7],
        buf[8], buf[9], buf[10]);
}

/*
// Timer 1 overflow interrupt service routine
// Anything here has to take less than 65 ms
ISR(TIMER1_OVF_vect, ISR_BLOCK) {
}
*/

// MCP2515::sendMessage() wrapper definition
MCP2515::ERROR send(canid_t can_id, __u8 can_dlc, __u8 data_0,
    __u8 data_1, __u8 data_2, __u8 data_3, __u8 data_4, __u8 data_5,
    __u8 data_6, __u8 data_7) {

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