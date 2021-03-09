import serial

_STANDARD_FRAME = 8


class Model:
    __SERIAL_BAUDRATE = 115200
    __COM3 = "COM3"
    __COM4 = "COM4"
    __NON_BLOCKING = 0

    def __init__(self):
        try:
            self.arduino = serial.Serial(port=self.__COM3, baudrate=self.__SERIAL_BAUDRATE, bytesize=serial.EIGHTBITS,
                                         timeout=self.__NON_BLOCKING)
            print(f"Port connected: {self.arduino.name}")
        except serial.SerialException:
            print("The device can not be found or can not be configured")

    def on_close(self):
        self.arduino.close()
        exit()

    def write(self):
        self.arduino.write(bytearray([0xFF, 0x3D, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]))

    def read(self):
        print(self.arduino.read(_STANDARD_FRAME).hex())
