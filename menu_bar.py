import tkinter as tk


class MenuBar(tk.Menu):
    def __init__(self, root, *args, **kwargs):
        tk.Menu.__init__(self, root, *args, **kwargs)
        self.root = root

        self.add_command(label="File")
        self.add_command(label="Software")
        self.add_command(label="Settings")
        self.add_command(label="MACROS")
        self.add_command(label="Tuning")
        self.add_command(label="CAN")
        self.add_command(label="Help")
