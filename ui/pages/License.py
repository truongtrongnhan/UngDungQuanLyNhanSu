import tkinter as tk
from ui.pages.BasePage import BasePage

class License(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="ĐƠN XIN PHÉP", font=("Helvetica", 16))
        label.pack(pady=20)
