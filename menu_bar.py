import tkinter as tk    # tk.Menu


class MenuBar(tk.Menu):     # self -> tk.Menu
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.add_command(label="File")
        self.add_command(label="Software")
        self.add_command(label="Settings")
        self.add_command(label="MACROS")
        self.add_command(label="Tuning")
        self.add_command(label="CAN")
        self.add_command(label="Help")
