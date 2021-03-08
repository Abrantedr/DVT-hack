import tkinter as tk


class MainTab(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

        # Contents of MainTab below
        # "LED ON" Button
        self.btn_led_on = tk.Button(self, text="Write")
        self.btn_led_on.grid(row=0, column=0, ipadx=10, ipady=10)

        # "LED OFF" Button
        self.btn_led_off = tk.Button(self, text="Read")
        self.btn_led_off.grid(row=0, column=1, ipadx=10, ipady=10)
