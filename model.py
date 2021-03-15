import serial
import threading

from queue import Queue

# CAN constants
STANDARD_FRAME = 11
DLC = 8
SDO_LSB = 0x01
SDO_MSB = 0x06


class Model:
    __SERIAL_BAUDRATE = 115200
    __COM3 = "COM3"
    __COM4 = "COM4"
    __COM5 = "COM5"
    __COM6 = "COM6"
    __NON_BLOCKING = 0
    __SYNC = 0.02       # 10 ms is the minimum SYNC time interval, 65 ms for the ISR

    def __init__(self, controller):
        self.controller = controller

        # Start serial communication
        try:
            self.arduino = serial.Serial(port=self.__COM3, baudrate=self.__SERIAL_BAUDRATE, bytesize=serial.EIGHTBITS,
                                         timeout=self.__SYNC)
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

    def send(self, command, index_lsb, index_msb, sub_index, data_0=0x00, data_1=0x00, data_2=0x00, data_3=0x00):
        self.arduino.write(bytearray([SDO_MSB, SDO_LSB, DLC, command, index_lsb, index_msb, sub_index, data_0, data_1,
                                      data_2, data_3]))

    def nmt_send(self, state, node):
        self.arduino.write(bytearray([0x00, 0x02, state, node, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

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
            print(item)
            if item[:4] == "0581":              # We caught a response from Gen4
                if item[6:8] == "60":           # It was a successful read
                    if item[8:14] == "105100":  # It's NMT State
                        if item[14:16] == "04":
                            self.controller.update_nmt_state("Stopped")
                        elif item[14:16] == "05":
                            self.controller.update_nmt_state("Operational")
                        elif item[14:16] == "7f":
                            self.controller.update_nmt_state("Pre-Operational")
                    if item[8:14] == "616000":  # It's Operational Mode
                        if item[14:16] == "03":
                            self.controller.update_operational_mode("Speed Mode")
                        elif item[14:16] == "04":
                            self.controller.update_operational_mode("Torque Mode")
                        elif item[14:16] == "05":
                            self.controller.update_operational_mode("Open Loop Speed Mode")
                    if item[8:14] == "6c600":   # It's Actual Velocity
                        self.controller.update_actual_velocity(str(int(item[16:18] + item[14:16], base=16)))
                    if item[8:14] == "78600":   # It's Actual Motor Current
                        self.controller.update_actual_motor_current(str(int(item[16:18] + item[14:16], base=16)))
                    if item[8:14] == "21210":   # It's Forward Switch
                        if item[14:16] == "00":
                            self.controller.update_forward_switch("Disabled")
                        elif item[14:16] == "01":
                            self.controller.update_forward_switch("Enabled")

            # Check if we can close the thread
            if self.thread_stop.is_set():
                break

    def close(self):
        print(f"Closing port: {self.arduino.name}")
        self.arduino.close()
