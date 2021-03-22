import tkinter as tk
import logging as log

import csv
import time
import threading

# Model
from model import Model

# Views
from main_window import MainWindow
from menu_bar import MenuBar


class Controller:
    def __init__(self):
        # Controller holds the main application
        self.root = tk.Tk()

        # Controller receives model and views
        self.model = Model(self)
        self.menu_bar = MenuBar(self.root)
        self.main_window = MainWindow(self.root, self)

        # Prepare run_circuit daemonic thread
        self.run_circuit_thread = threading.Thread(target=self.run_circuit,
                                                   daemon=True,
                                                   name="Run Circuit")

    def send_credentials(self):
        self.model.send(0x2B, 0x00, 0x50, 0x02, 0xDF, 0x4B, 0xEF, 0xFA)

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
        self.send_credentials()
        time.sleep(0.05)
        self.model.send(command, index_lsb, index_msb, sub_index, data_0,
                        data_1, data_2, data_3)

    def set_operational_state(self, state, node, command, index_lsb, index_msb,
                              sub_index, data_0=0x00, data_1=0x00, data_2=0x00,
                              data_3=0x00):
        self.send_credentials()
        time.sleep(0.05)
        self.model.send(command, index_lsb, index_msb, sub_index, data_0,
                        data_1, data_2, data_3)
        time.sleep(0.05)
        self.model.nmt_send(state, node)

    def thread_run_circuit(self):
        self.run_circuit_thread.start()

    def run_circuit(self):
        """
        Tool for executing a simulated lap in the ENGIRO MS1920
        Iván Rodríguez Méndez <irodrigu@ull.edu.es> 2021
        """
        last_time = 0

        # TODO: Prepare model to send targets
        # self.model.write ( ...

        filename = "Motorland-lap.csv"
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)

                # Skip (3) headers
                for headers in range(0, 3):
                    next(reader)

                for row in reader:
                    log.info(f"Time:{row[1][:5]}\tSpeed:{row[0][:6]}\t"
                             f"Distance:{row[2][:2]}\tRPM:{row[5][:4]}\t"
                             f"Torque:{row[6][:5]}")

                    # TODO: CAN bus messages
                    # self.model.write( ...

                    # Wait for next torque demand
                    time.sleep(float(row[1]) - last_time)
                    last_time = float(row[1])
        except FileNotFoundError:
            log.info(f"No such file or directory: {filename}")

    def on_close(self):
        # Set stop conditions for all threads
        self.model.thread_stop.set()
        self.main_window.tab_menu.thread_stop.set()

        # Join non-daemonic threads
        self.main_window.tab_menu.main_tab_sdo_thread.join()

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
