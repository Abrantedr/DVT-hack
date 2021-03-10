import serial

STANDARD_FRAME = 11


class Model:
    __SERIAL_BAUDRATE = 115200
    __COM3 = "COM3"
    __COM4 = "COM4"
    __COM5 = "COM5"
    __COM6 = "COM6"
    __NON_BLOCKING = 0

    def __init__(self):
        try:
            self.arduino = serial.Serial(port=self.__COM3, baudrate=self.__SERIAL_BAUDRATE, bytesize=serial.EIGHTBITS,
                                         timeout=self.__NON_BLOCKING)
            print(f"Port connected: {self.arduino.name}")
        except serial.SerialException:
            print("The device can not be found or can not be configured")

    def on_close(self):
        print(f"Closing {self.arduino.name}")
        self.arduino.close()
        exit()

    def write(self):
        b = self.arduino.write(bytearray([0x05, 0x81, 0x08, 0x60, 0x00, 0x59, 0x01, 0x2B, 0x00, 0x00, 0x00]))
        print(f"Written {b} bytes")

    def read(self):
        frame = self.arduino.read(STANDARD_FRAME).hex()
        if frame:
            frame_list = [frame[i:i + 2] for i in range(6, len(frame), 2)]
            msg = frame[0:4] + " " + " ".join(frame_list)
            print(msg)
