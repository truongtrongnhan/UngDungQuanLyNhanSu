import tkinter as tk

class Overview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="TỔNG QUAN", font=("Helvetica", 16))
        label.pack(pady=20)
