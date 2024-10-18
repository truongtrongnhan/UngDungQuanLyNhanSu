import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from helper.CustomTreeView import CustomTreeView
from ui.pages.BasePage import BasePage
from tkinter import messagebox
from models.department.department_model import department_model
from service.department_service import DepartMentService
from service.employee_service import EmployeeService
from datetime import datetime


class Department(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="QUẢN LÝ PHÒNG BAN", font=("Helvetica", 16))
        label.pack(pady=20)
        self.employee_service = EmployeeService()
        self.data_employee = self.employee_service.getCombox()
        columns = [
            {
                'key': 'ID',
                'name': 'ID',
                'width': 10,
                'anchor': 'center'
            },
            {
                'key': 'Name',
                'name': 'Tên phòng ban',
                'width': 150,
                'anchor': 'center'
            },   
            {
                'key': 'Description',
                'name': 'Mô tả',
                'width': 200,
                'anchor': 'center'
            },
            {
                'key': 'Location',
                'name': 'Địa điểm',
                'width': 150,
                'anchor': 'center'
            },
            {
                'key' : 'CreateDate',
                'name' : 'Ngày tạo',
                'width' : 100,
                'anchor': 'center'
            },
            {
                'key': 'Manager_id',
                'name': 'Người quản lý',
                'width': 150,
                'anchor': 'center'
            },
            {
                'key': 'Action',
                'name': 'Hành động',
                'width': 100,
                'anchor': 'center'
            }
            
        ]


        self.fram_view = tk.Frame(self)
        self.fram_view.pack(padx=10, fill="both", expand=True)
        self.department_service = DepartMentService()
        self.datas = self.search()
        self.treeView = CustomTreeView(self.fram_view, self, self.datas, columns, len(columns) - 1)

    def search(self):
        rows = self.department_service.search()
        return rows
    
    def add(self):
        self.title_popup = "Thêm mới"
        form_popup = DepartmentFormPopup(self, None)
    
    def edit(self, row_id):
        self.title_popup = "Cập nhập"
        data = self.department_service.getById(row_id)
        form_popup = DepartmentFormPopup(self, data)

    def insert(self, data):
        confirm = messagebox.askyesno("Xác nhận thêm mới", "Bạn có chắc chắn muốn thêm mới ?")
        if confirm:
            result = self.department_service.insert(data)
            self.treeView.loadData()

    
    def update(self, data):
        confirm = messagebox.askyesno("Xác nhận cập nhập", "Bạn có chắc chắn muốn cập nhập ?")
        if confirm:
            result = self.department_service.update(data)
            self.treeView.loadData()
    
    def delete(self, row_id):
        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa nhân viên này?")
        if confirm:
            result = self.department_service.delete(row_id)
            self.treeView.loadData()

class DepartmentFormPopup(tk.Toplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.geometry("640x170")
        self.title(parent.title_popup)
        self.parent = parent
        self.selected_employee_id = None
        
        window_width = 640
        window_height = 170
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        #Căn giữa popup
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        self.grab_set()

        self.entry_id = tk.Entry(self)
        self.entry_id.grid(row=0, column=1)
        self.entry_id.grid_remove()

        label_name = tk.Label(self, text="Tên phòng ban:")
        label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_name = tk.Entry(self, width=30)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)


        label_location = tk.Label(self, text="Địa điểm:")
        label_location.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.entry_location = tk.Entry(self, width=30)
        self.entry_location.grid(row=0, column=3, padx=10, pady=10)

        label_desc = tk.Label(self, text="Mô tả:")
        label_desc.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_desc = tk.Entry(self, width=30)
        self.entry_desc.grid(row=1, column=1, padx=10, pady=10)

        label_manager = tk.Label(self, text="Người quản lý:")
        label_manager.grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.manager_combobox = ttk.Combobox(self, width=30-4, state="readonly")
        self.manager_combobox.grid(row=1, column=3, padx=10, pady=10)
        self.manager_combobox['values'] = [f"{emp[1]}" for emp in parent.data_employee]
        self.manager_combobox.current(0)
        self.manager_combobox.bind("<<ComboboxSelected>>", self.on_employee_selected)

        button_frame = tk.Frame(self)
        button_frame.grid(row=6, column=3, padx=10, pady=10, sticky="e")

        # Nếu edit insert data và điều chỉnh readonly
        if(data is not None):
            self.entry_id.insert(0, data[0])
            self.entry_name.insert(0, data[1])
            self.entry_desc.insert(0, data[2])
            self.entry_location.insert(0, data[3])
            self.set_employee_combobox(data[4])


        self.button_close = tk.Button(button_frame, text="Đóng", command=self.destroy)
        self.button_close.pack(side="right", padx=5)

        self.button_save = tk.Button(button_frame, text="Lưu", command=self.save)
        self.button_save.pack(side="right", padx=5)

    def save(self):
        department_id = self.entry_id.get() if self.entry_id.get() is not None else None
        department_input = department_model(
            department_id=department_id,
            department_name=self.entry_name.get(),
            description=self.entry_desc.get(),
            location=self.entry_location.get(),
            create_date= datetime.now().date(),
            manager_id= self.selected_employee_id
        )

        if department_input.department_id is None or department_input.department_id == "":
            self.parent.insert(department_input)
            self.destroy()
        else:
            self.parent.update(department_input)
            self.destroy()

    def on_employee_selected(self, event):
        selected_position_name = self.manager_combobox.get()
        self.selected_employee_id = None
        for pos in self.parent.data_employee:
            if pos[1] == selected_position_name:
                self.selected_employee_id = pos[0]
                break
    
    def set_employee_combobox(self, employee_id):
        self.selected_employee_id = employee_id
        for pos in self.parent.data_employee:
            if pos[0] == employee_id:
                self.manager_combobox.set(pos[1])  
                break