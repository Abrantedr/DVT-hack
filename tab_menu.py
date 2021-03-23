import tkinter as tk        # tk.BOTH
from tkinter import ttk     # ttk.Notebook

# Tab imports
from tab import MainTab, TreeTab, IOTab, PDOTab


class TabMenu(ttk.Notebook):    # self -> ttk.Notebook
    def __init__(self, root, controller, **kwargs):
        super().__init__(root, **kwargs)
        self.controller = controller

        # Create tabs
        self.tab_main = MainTab(self, self.controller)
        self.tab_tree = TreeTab(self)
        self.tab_io = IOTab(self)
        self.tab_pdo = PDOTab(self, self.controller)

        # Add tabs to notebook
        self.add(self.tab_main, text="Main")
        self.add(self.tab_tree, text="Tree")
        self.add(self.tab_io, text="Input / Output")
        self.add(self.tab_pdo, text="TPDO / RPDO")

        # Place the tab menu
        self.pack(fill=tk.BOTH, expand=True)

        # Selecting a tab triggers events
        self.bind('<<NotebookTabChanged>>', self.on_tab_changed)

        # Set on tab selection conditions
        # On Main tab by default
        self.__tab_state = (True, False, False, False)

        # Start SDO requests
        self.sdo_request()

    def sdo_request(self):
        # Keep sending these specific SDOs while we are in Main tab
        if self.__tab_state[0]:
            # NMT State (5110h, 0) read (0x40)
            self.controller.write(0x40, 0x10, 0x51, 0x00)
            # Operational Mode (6061h, 0) read (0x40)
            self.controller.write(0x40, 0x61, 0x60, 0x00)
            # Actual Velocity (606Ch, 0) read (0x40)
            self.controller.write(0x40, 0x6C, 0x60, 0x00)
            # Actual Motor Current (6078h, 0) read (0x40)
            self.controller.write(0x40, 0x78, 0x60, 0x00)
            # Reverse Switch (2122h, 0) read (0x40)
            self.controller.write(0x40, 0x22, 0x21, 0x00)
            # Forward Switch (2121h, 0) read (0x40)
            self.controller.write(0x40, 0x21, 0x21, 0x00)
            # FS1 Switch (2123h, 0) read (0x40)
            self.controller.write(0x40, 0x23, 0x21, 0x00)
            # Seat Switch (2124h, 0) read (0x40)
            self.controller.write(0x40, 0x24, 0x21, 0x00)
            # Max Motor Speed (6080h, 0) read (0x40)
            self.controller.write(0x40, 0x80, 0x60, 0x00)
            # Another SDO
            pass
        # Keep sending these specific SDOs while we are in Tree tab
        if self.__tab_state[1]:
            pass
            # Another SDO
            # Another SDO
        # Keep sending these specific SDOs while we are in I/O tab
        if self.__tab_state[2]:
            pass
            # Another SDO
            # Another SDO
        # Keep sending these specific SDOs while we are in PDO tab
        if self.__tab_state[3]:
            pass
            # Another SDO
            # Another SDO
        # Schedule another SDO request block
        self.after(100, self.sdo_request)

    def on_tab_changed(self, event):
        tab = event.widget.tab('current')['text']
        if tab == "Main":
            self.__tab_state = (True, False, False, False)
        elif tab == "Tree":
            self.__tab_state = (False, True, False, False)
        elif tab == "Input / Output":
            self.__tab_state = (False, False, True, False)
        elif tab == "TPDO / RPDO":
            self.__tab_state = (False, False, False, True)
