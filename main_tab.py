import tkinter as tk    # tk.Frame, tk.Button


class MainTab(tk.Frame):    # self -> tk.Frame
    def __init__(self, root, controller, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        # Main tab contents
        # "Write" Button
        self.btn_write = tk.Button(self, text="Write", command=controller.write)
        self.btn_write.grid(row=0, column=0, ipadx=10, ipady=10)

        # "Read" Button
        self.btn_read = tk.Button(self, text="Read", command=controller.read)
        self.btn_read.grid(row=0, column=1, ipadx=10, ipady=10)
