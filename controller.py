import tkinter as tk
import time

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
        self.main_window = MainWindow(self.root, self)  # Sends controller to main window

    def update_nmt_state(self, state):
        self.main_window.tab_menu.tab_main.var_nmt.set(state)

    def update_operational_mode(self, state):
        self.main_window.tab_menu.tab_main.var_mode.set(state)

    def update_actual_velocity(self, state):
        self.main_window.tab_menu.tab_main.var_vel.set(state)

    def update_actual_motor_current(self, state):
        self.main_window.tab_menu.tab_main.var_current.set(state)

    def write(self, command, index_lsb, index_msb, sub_index, data_0=0x00, data_1=0x00, data_2=0x00, data_3=0x00):
        self.model.send(command, index_lsb, index_msb, sub_index, data_0, data_1, data_2, data_3)

    def set_operational_state(self, state, node, command, index_lsb, index_msb, sub_index, data_0=0x00, data_1=0x00,
                              data_2=0x00, data_3=0x00):
        self.model.send(command, index_lsb, index_msb, sub_index, data_0, data_1, data_2, data_3)
        time.sleep(0.05)
        self.model.nmt_send(state, node)

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
        self.root.geometry("800x800")
        self.root.deiconify()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.config(menu=self.menu_bar)
        self.root.mainloop()
