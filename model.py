import serial


class Model:
    __SERIAL_BAUDRATE = 115200
    __COM3 = "COM3"
    __COM4 = "COM4"

    def __init__(self):
        self.arduino = serial.Serial(self.__COM3, self.__SERIAL_BAUDRATE, timeout=0)

    def on_close(self):
        self.arduino.close()
        exit()

    def write(self):
        print("Sent", self.arduino.write(bytearray([0x01, 0x02, 0x03, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E])), "bytes")

    def read(self):
        print(self.arduino.read(8))
