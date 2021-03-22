import serial
import threading
import logging as log

from os.path import isdir
from os import mkdir
from time import strftime
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
    __SYNC = 0.02   # 10 ms min SYNC time interval, 65 ms for the ISR

    def __init__(self, controller):
        self.controller = controller

        # Set path and extension for log files
        path = "./log/"
        ext = ".log"
        # Create directory for logs
        if not isdir(path):
            mkdir(path)

        # Create logger
        date_time = strftime("%d-%m-%Y-%I-%M-%S")
        log.basicConfig(
            format="%(asctime)s:%(levelname)s:%(message)s",
            filename=path + date_time + ext,
            datefmt="%d/%m/%Y %I:%M:%S %p",
            level=log.INFO
        )

        # Start serial communication
        try:
            self.arduino = serial.Serial(port=self.__COM3,
                                         baudrate=self.__SERIAL_BAUDRATE,
                                         bytesize=serial.EIGHTBITS,
                                         timeout=self.__SYNC)
            log.info(f"Port connected: {self.arduino.name}")
        except serial.SerialException:
            log.info("The device can not be found or can not be configured")
            exit()
        finally:
            # Create a queue to parse input messages
            self.queue = Queue()

            # Set condition to stop threads
            self.thread_stop = threading.Event()

            # Start sniffing the CAN bus
            self.sniff_thread = threading.Thread(target=self.sniff_bus,
                                                 daemon=True,
                                                 name="Sniffer")
            self.sniff_thread.start()

            # Start parsing input messages
            self.queue_thread = threading.Thread(target=self.parse_queue,
                                                 daemon=True,
                                                 name="Queue Parser")
            self.queue_thread.start()

    def send(self, command, index_lsb, index_msb, sub_index, data_0=0x00,
             data_1=0x00, data_2=0x00, data_3=0x00):
        self.arduino.write(bytearray([SDO_MSB, SDO_LSB, DLC, command,
                                      index_lsb, index_msb, sub_index,
                                      data_0, data_1, data_2, data_3]))

    def nmt_send(self, state, node):
        self.arduino.write(bytearray([0x00, 0x02, state, node, 0x00, 0x00,
                                      0x00, 0x00, 0x00, 0x00, 0x00]))

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

            # Extract frame fields
            cob_id = item[:4]
            command = item[6:8]
            index = item[8:14]
            # Data bytes
            byte_one = item[14:16]      # LSB
            byte_two = item[16:18]
            byte_three = item[18:20]
            byte_four = item[20:22]     # MSB

            # Sort message
            if cob_id == "0581":     # We caught a response from Gen4
                if command == "4f":  # It was a successful 1 byte read
                    if index == "105100":  # It's NMT State
                        if byte_one == "04":
                            self.controller.update_nmt_state("Stopped")
                        elif byte_one == "05":
                            self.controller.update_nmt_state("Operational")
                        elif byte_one == "7f":
                            self.controller.update_nmt_state("Pre-Operational")

                    if index == "616000":  # It's Operational Mode
                        if byte_one == "03":
                            self.controller.update_operational_mode(
                                "Speed Mode")
                        elif byte_one == "04":
                            self.controller.update_operational_mode(
                                "Torque Mode")
                        elif byte_one == "05":
                            self.controller.update_operational_mode(
                                "Open Loop Speed Mode")

                    if index == "222100":   # It's Reverse Switch
                        if byte_one == "00":
                            self.controller.update_reverse_switch("Disabled")
                        elif byte_one == "01":
                            self.controller.update_reverse_switch("Enabled")

                    if index == "212100":   # It's Forward Switch
                        if byte_one == "00":
                            self.controller.update_forward_switch("Disabled")
                        elif byte_one == "01":
                            self.controller.update_forward_switch("Enabled")

                    if index == "232100":   # It's FS1 Switch
                        if byte_one == "00":
                            self.controller.update_fs_switch("Disabled")
                        elif byte_one == "01":
                            self.controller.update_fs_switch("Enabled")

                    if index == "242100":   # It's Seat Switch
                        if byte_one == "00":
                            self.controller.update_seat_switch("Disabled")
                        elif byte_one == "01":
                            self.controller.update_seat_switch("Enabled")

                if command == "4b":
                    if index == "786000":   # It's Act. Motor Curr.
                        # TODO: It's not actually working atm.
                        self.controller.update_actual_motor_current(
                            str(int(byte_two + byte_one, base=16)))

                if command == "43":
                    if index == "6c6000":   # It's Actual Velocity
                        # TODO: Doesn't work in reverse mode
                        self.controller.update_actual_velocity(
                            str(int(byte_four + byte_three + byte_two +
                                    byte_one, base=16)))

                    if index == "806000":   # It's Max Motor Speed
                        self.controller.update_max_speed(str(int(byte_four +
                                                                 byte_three +
                                                                 byte_two +
                                                                 byte_one,
                                                                 base=16)))

            # Check if we can close the thread
            if self.thread_stop.is_set():
                break

    def close(self):
        log.info(f"Closing port: {self.arduino.name}")
        self.arduino.close()
