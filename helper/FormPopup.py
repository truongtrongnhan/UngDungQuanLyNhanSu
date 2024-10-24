import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from helper.CustomComboboxGrid import CustomComboboxGrid
from helper.CustomInputGridText import CustomInputGridText
from helper.CustomInputDateGrid import CustomInputDateGrid
import time

class FormPopup(tk.Toplevel):
    def __init__(self, parent, title, form_fields ,form_data=None, width = 640, height = 300):
        super().__init__(parent)
        self.withdraw()
        self.geometry(f"{width}x{height}")
        self.title(title)
        self.parent = parent
        
        window_width = width
        window_height = height
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        #Căn giữa popup
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        self.grab_set()

        self.form_fields = form_fields  # Danh sách các trường cần hiển thị

        self.field_widgets = {}

        self.create_form_widgets()

        button_frame = tk.Frame(self)
        button_frame.grid(row=len(self.form_fields) + 1, column=3, padx=10, pady=10)

        self.button_close = tk.Button(button_frame, text="Đóng", command=self.destroy)
        self.button_close.pack(side="right", padx=5)

        self.button_save = tk.Button(button_frame, text="Lưu", command=self.save_form_data)
        self.button_save.pack(side="right", padx=5)

        # Gắn dữ liệu vào form nếu có form_data
        if form_data is not None:
            self.populate_form_data(form_data)

        self.deiconify()

    def create_form_widgets(self):
        for idx, field in enumerate(self.form_fields):
            field_type = field.get('type')
            if(field_type == "ID"):
                entry = tk.Entry(self, width=30)
                entry.grid(row=0, column=1)
                self.field_widgets[field['name']] = entry
                entry.grid_remove()
            
            field_label = tk.Label(self, text=field.get('label') + ':')
            field_label.grid(row=field['row'], column=field['col1'], padx=10, pady=5, sticky="e")
            if field_type == "Entry":
                entry = tk.Entry(self, width=30)
                entry.grid(row=field['row'], column=field['col2'], padx=10, pady=5)
                self.field_widgets[field['name']] = entry
            elif field_type == "DateEntry":
                date_entry = DateEntry(self, width=30-4)
                date_entry.grid(row=field['row'], column=field['col2'], padx=10, pady=5)
                self.field_widgets[field['name']] = date_entry
            elif field_type == "Combobox":
                combobox = ttk.Combobox(self, width=30-4, values=field.get('values', []), state="readonly")
                combobox.grid(row=field['row'], column=field['col2'], padx=10, pady=5)
                self.field_widgets[field['name']] = combobox
            elif field_type == "CustomInput":
                entry = CustomInputGridText(self, field['label'], 30, field['col2'], field['row'])
                self.field_widgets[field['name']] = entry
            elif field_type == "ComboboxCustom":
                comboboxcustom = CustomComboboxGrid(parent = self, text=field['label'], dataArray= field.get('values', []), width=30-4, gridCol= field['col2'], gridRow=field['row'])
                self.field_widgets[field['name']] = comboboxcustom
            elif field_type == "CustomDate":
                date_entry = CustomInputDateGrid(self, field['label'], 30-4, "", "", field['col2'], field['row'])
                self.field_widgets[field['name']] = date_entry
                


    def save_form_data(self):
        form_data = {}
        for field_name, widget in self.field_widgets.items():
            if isinstance(widget, (tk.Entry, ttk.Combobox)):
                form_data[field_name] = widget.get()
            elif isinstance(widget, DateEntry):
                form_data[field_name] = widget.get_date().strftime('%Y-%m-%d')
            elif isinstance(widget, (CustomComboboxGrid, CustomInputGridText)):
                form_data[field_name] = widget.get_value()
            elif isinstance(widget, CustomInputDateGrid):
                form_data[field_name] = widget.get_value().strftime('%Y-%m-%d')

        print(form_data)
        if(not self.validation_all()): return

        id = next(iter(form_data.values()))
        if(id is None or id == ''):
            result = self.parent.insert(form_data)
        else:
            result = self.parent.update(form_data)

        if(result): self.destroy()

    def populate_form_data(self, form_data):
        for field_name, value in form_data.items():
            widget = self.field_widgets.get(field_name)
            if widget is not None:
                if isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)
                    if value is not None:
                        widget.insert(0, value) 
                elif isinstance(widget, DateEntry):
                    try:
                        widget.set_date(value) 
                    except ValueError:
                        widget.set_date("") 
                elif isinstance(widget, ttk.Combobox):
                    if value in widget['values']:
                        widget.set(value)
                elif isinstance(widget, CustomComboboxGrid):
                    widget.set_combobox(value)
                elif isinstance(widget, CustomInputGridText):
                    widget.delete_value()
                    if value is not None:
                        widget.set_value(value)
                elif isinstance(widget , CustomInputDateGrid):
                    try:
                        widget.set_date(value) 
                    except ValueError:
                        widget.set_date("") 
                    
    def validation_all(self):
        for field_name, widget in self.field_widgets.items():
            if isinstance(widget, CustomComboboxGrid):
                if(not widget.validate_input()):  
                    return False
            elif isinstance(widget, CustomInputGridText):
                if(not widget.validate_input()):
                    return False
            elif isinstance(widget, CustomInputDateGrid):
                if(not widget.validate_input()):
                    return False
        return True

    def prepare_popup_data(self):
        print("Đang chuẩn bị dữ liệu cho popup...")
        time.sleep(2)  # Giả lập một hàm chờ 2 giây để chuẩn bị dữ liệu (có thể thay bằng logic xử lý khác)
        print("Dữ liệu đã sẵn sàng!")