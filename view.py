import tkinter as tk

from tab_menu import TabMenu


class View:
    def __init__(self, root, model):
        self.root = root
        self.model = model

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.tab_menu = TabMenu(self.main_frame)

        self.tab_menu.tab_main.btn_led_on.bind("<Button>", self.led_on)
        self.tab_menu.tab_main.btn_led_off.bind("<Button>", self.led_off)

    def led_on(self, event):
        self.model.led_on()

    def led_off(self, event):
        self.model.led_off()
