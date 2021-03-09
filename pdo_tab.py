import tkinter as tk


class PDOTab(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

        # Contents of IOTab below
        self.lbl_pdo = tk.Label(self, text="PDO Tab")
        self.lbl_pdo.pack()
