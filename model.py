import serial
import threading


STANDARD_FRAME = 11


class Model:
    __SERIAL_BAUDRATE = 115200
    __COM3 = "COM3"
    __COM4 = "COM4"
    __COM5 = "COM5"
    __COM6 = "COM6"
    __NON_BLOCKING = 0
    __SYNC_MIN = 0.02       # 10 ms is the minimum SYNC time interval, 65 ms for the ISR

    def __init__(self, controller):
        self.controller = controller
        # Start serial communication
        try:
            self.arduino = serial.Serial(port=self.__COM3, baudrate=self.__SERIAL_BAUDRATE, bytesize=serial.EIGHTBITS,
                                         timeout=self.__SYNC_MIN)
            print(f"Port connected: {self.arduino.name}")
        except serial.SerialException:
            print("The device can not be found or can not be configured")
            exit()

        # Start sniffing the CAN bus
        self.thread_stop = threading.Event()    # Thread flag (false by default)
        self.thread = threading.Thread(target=self.sniff_bus, daemon=True)
        self.thread.start()

    def on_close(self):
        print(f"Closing {self.arduino.name}")

        # End sniffing thread
        # .join() is not needed
        self.thread_stop.set()

        # End serial communication
        self.arduino.close()
        exit()

    def write(self):
        b = self.arduino.write(bytearray([0x05, 0x81, 0x08, 0x60, 0x00, 0x59, 0x01, 0x7F, 0x00, 0x00, 0x00]))
        print(f"Written {b} bytes")
        self.controller.update_label(b)
        # TODO: Write a well defined write-to-serial function

    def sniff_bus(self):
        while True:
            # Get a frame
            frame = self.arduino.read(STANDARD_FRAME).hex()

            # Process frame #
            if frame:
                frame_list = [frame[i:i + 2] for i in range(6, len(frame), 2)]
                msg = frame[0:4] + " " + " ".join(frame_list)
                print(msg)

            # Check if we can close the thread
            if self.thread_stop.is_set():
                break
