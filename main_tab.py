import tkinter as tk


class MainTab(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

        # Contents of MainTab below
        # "Write" Button
        self.btn_write = tk.Button(self, text="Write")
        self.btn_write.grid(row=0, column=0, ipadx=10, ipady=10)

        # "Read" Button
        self.btn_read = tk.Button(self, text="Read")
        self.btn_read.grid(row=0, column=1, ipadx=10, ipady=10)
