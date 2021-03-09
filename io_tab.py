import tkinter as tk  # tk.Frame


class IOTab(tk.Frame):  # self -> tk.Frame
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        # I/O tab contents
        self.lbl_io = tk.Label(self, text="I/O tab")
        self.lbl_io.pack()
