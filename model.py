import random
import serial
import threading

from queue import Queue


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
        finally:
            # Create a queue to parse input messages
            self.queue = Queue()

            # Set condition to stop threads
            self.thread_stop = threading.Event()

            # Start sniffing the CAN bus
            self.sniff_thread = threading.Thread(target=self.sniff_bus, daemon=True, name="Sniffer")
            self.sniff_thread.start()

            # Start parsing input messages
            self.queue_thread = threading.Thread(target=self.parse_queue, daemon=True, name="Queue Parser")
            self.queue_thread.start()

    def send(self, command, index, subindex):
        b = self.arduino.write(bytearray(random.getrandbits(8) for _ in range(11)))
        print(command, index, subindex)
        # print(f"Written {b} bytes")
        # self.controller.update_label(b)
        # TODO: Write a well defined write-to-serial function

    def sniff_bus(self):
        while True:
            # Get a frame
            frame = self.arduino.read(STANDARD_FRAME).hex()

            # Queue frame #
            if frame:
                self.queue.put_nowait(frame)

            # Check if we can close the thread
            if self.thread_stop.is_set():
                break

    def parse_queue(self):
        while True:
            item = self.queue.get()
            if item[-1] == "1":
                self.controller.update_label(item)

            # Check if we can close the thread
            if self.thread_stop.is_set():
                break

    def close(self):
        print(f"Closing port: {self.arduino.name}")
        self.arduino.close()
