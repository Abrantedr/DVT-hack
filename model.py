import serial


class Model:
    __SERIAL_BAUDRATE = 115200
    __COM3 = "COM3"
    __COM4 = "COM4"
    __NON_BLOCKING = 0

    def __init__(self):
        try:
            self.arduino = serial.Serial(port=self.__COM3, baudrate=self.__SERIAL_BAUDRATE, timeout=self.__NON_BLOCKING)
            print(f"Port connected: {self.arduino.name}")
        except serial.SerialException:
            print("The device can not be found or can not be configured")

    def on_close(self):
        self.arduino.close()
        exit()

    def write(self):
        print("Sent", self.arduino.write(bytearray([0x01, 0x02, 0x03, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E])), "bytes")

    def read(self):
        print(self.arduino.read(8))
