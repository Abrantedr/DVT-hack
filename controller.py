import tkinter as tk
import logging as log
import time
import threading

from os import mkdir
from os.path import isdir

# Model
from model import Model

# Views
from main_window import MainWindow
from menu_bar import MenuBar


class Controller:
    def __init__(self):
        # Set path and extension for log files
        path = "./log/"
        ext = ".log"
        # Create directory for logs
        if not isdir(path):
            mkdir(path)

        # Create logger
        date_time = time.strftime("%d-%m-%Y-%H-%M-%S-%p")
        log.basicConfig(
            format="%(asctime)s.%(msecs)03d "
                   "[%(filename)s:%(lineno)s:%(funcName)s()] "
                   "%(levelname)s:\t%(message)s",
            filename=path + date_time + ext,
            datefmt="%d/%m/%Y %H:%M:%S",
            level=log.INFO
        )

        # Controller holds the main application
        self.root = tk.Tk()

        # Controller receives model and views
        self.model = Model(self)
        self.menu_bar = MenuBar(self.root)
        self.main_window = MainWindow(self.root, self)

        # Set condition to stop threads
        self.thread_stop = threading.Event()

        # Start sniffing the CAN bus
        self.sniff_thread = threading.Thread(
            target=self.model.sniff_bus,
            daemon=True,
            name="Sniffer")
        self.sniff_thread.start()

        # Start parsing input messages
        self.queue_thread = threading.Thread(
            target=self.model.parse_queue,
            daemon=True,
            name="Queue Parser"
        )
        self.queue_thread.start()

        # Prepare run_circuit thread
        self.run_circuit_thread = threading.Thread(
            target=self.model.run_circuit,
            daemon=True,
            name="Run Circuit"
        )

    def update_nmt_state(self, state):
        self.main_window.tab_menu.tab_main.var_nmt.set(state)

    def update_operational_mode(self, state):
        self.main_window.tab_menu.tab_main.var_mode.set(state)

    def update_actual_velocity(self, state):
        self.main_window.tab_menu.tab_main.var_vel.set(state)

    def update_actual_motor_current(self, state):
        self.main_window.tab_menu.tab_main.var_current.set(state)

    def update_reverse_switch(self, state):
        self.main_window.tab_menu.tab_main.var_rev.set(state)

    def update_forward_switch(self, state):
        self.main_window.tab_menu.tab_main.var_fwd.set(state)

    def update_fs_switch(self, state):
        self.main_window.tab_menu.tab_main.var_fs.set(state)

    def update_seat_switch(self, state):
        self.main_window.tab_menu.tab_main.var_seat.set(state)

    def update_max_speed(self, state):
        self.main_window.tab_menu.tab_main.var_max_speed.set(state)

    def write(self, command, index_lsb, index_msb, sub_index, data_0=0x00,
              data_1=0x00, data_2=0x00, data_3=0x00):
        self.model.send(command, index_lsb, index_msb, sub_index, data_0,
                        data_1, data_2, data_3)

    def set_operational_mode(self, command, index_lsb, index_msb,
                             sub_index, data_0=0x00, data_1=0x00, data_2=0x00,
                             data_3=0x00):
        self.model.send_credentials()
        time.sleep(0.05)
        self.model.send(command, index_lsb, index_msb, sub_index, data_0,
                        data_1, data_2, data_3)

    def set_operational_state(self, state, node, command, index_lsb, index_msb,
                              sub_index, data_0=0x00, data_1=0x00, data_2=0x00,
                              data_3=0x00):
        self.model.send_credentials()
        time.sleep(0.05)
        self.model.send(command, index_lsb, index_msb, sub_index, data_0,
                        data_1, data_2, data_3)
        time.sleep(0.05)
        self.model.send_nmt(state, node)

    def thread_run_circuit(self):
        # TODO: Refactor thread to avoid starting it twice
        try:
            self.run_circuit_thread.start()
        except RuntimeError:
            log.warning("run_circuit_thread is already running")

    def on_close(self):
        # Set stop conditions for all threads
        self.thread_stop.set()
        log.info("Exiting all threads safely")

        # End serial communication
        self.model.close()
        exit()  # And get out...

    def run(self):
        self.root.title("DVTH")
        self.root.geometry("600x800")
        self.root.deiconify()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.config(menu=self.menu_bar)
        self.root.mainloop()
