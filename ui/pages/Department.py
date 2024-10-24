import tkinter as tk
from helper.CustomTreeView import CustomTreeView
from ui.pages.BasePage import BasePage
from tkinter import messagebox
from service.department_service import DepartMentService
from service.employee_service import EmployeeService
from helper.FormPopup import FormPopup



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

        self.fields = [
            {'name': 'department_id', 'type': 'ID', 'label': 'ID' , 'row': 0, 'col1' : 1, 'col2': 2},

            {'name': 'department_name', 'type': 'CustomInput', 'label': 'Tên phòng ban' , 'row': 0, 'col1' : 0, 'col2': 1},
            {'name': 'location', 'type': 'CustomInput', 'label': 'Địa điểm', 'row': 0, 'col1' : 2, 'col2': 3},

            {'name': 'description', 'type': 'CustomInput', 'label': 'Mô tả', 'row': 1, 'col1' : 0, 'col2': 1},
            {'name': 'manager_id', 'type': 'ComboboxCustom', 'label': 'Người quản lý', 'values': self.data_employee , 'row': 1, 'col1' : 2, 'col2': 3},
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
        form_popup = FormPopup(parent = self, title = self.title_popup,form_fields = self.fields,form_data = None, width=640, height=170)
    
    def edit(self, row_id):
        self.title_popup = "Cập nhập"
        data = self.department_service.getById(row_id)
        form_popup = FormPopup(parent = self, title = self.title_popup,form_fields = self.fields,form_data = data, width=640, height=170)

    def insert(self, data):
        confirm = messagebox.askyesno("Xác nhận thêm mới", "Bạn có chắc chắn muốn thêm mới ?")
        if confirm:
            result = self.department_service.insert(data)
            self.treeView.loadData()
            return True
        return False

    
    def update(self, data):
        confirm = messagebox.askyesno("Xác nhận cập nhập", "Bạn có chắc chắn muốn cập nhập ?")
        if confirm:
            result = self.department_service.update(data)
            self.treeView.loadData()
            return True
        return False
    
    def delete(self, row_id):
        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa nhân viên này?")
        if confirm:
            result = self.department_service.delete(row_id)
            self.treeView.loadData()
            return True
        return False

