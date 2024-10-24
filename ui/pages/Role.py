import tkinter as tk
from helper.CustomTreeView import CustomTreeView
from ui.pages.BasePage import BasePage
from tkinter import messagebox
from models.role.role_model import role_model
from service.role_service import RoleService
from helper.FormPopup import FormPopup

class Role(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="QUYỀN", font=("Helvetica", 16))
        label.pack(pady=20)

        columns = [
            {
                'key': 'ID',
                'name': 'ID',
                'width': 10,
                'anchor': 'center'
            },
            {
                'key': 'Name',
                'name': 'Tên quyền',
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
                'key': 'Action',
                'name': 'Hành động',
                'width': 100,
                'anchor': 'center'
            }
        ]

        self.fields = [
            {'name': 'role_id', 'type': 'ID', 'label': 'ID' , 'row': 0, 'col1' : 1, 'col2': 2},
            {'name': 'role_name', 'type': 'CustomInput', 'label': 'Tên quyền' , 'row': 0, 'col1' : 0, 'col2': 1},
            {'name': 'description', 'type': 'CustomInput', 'label': 'Mô tả', 'row': 0, 'col1' : 2, 'col2': 3}
        ]


        self.fram_view = tk.Frame(self)
        self.fram_view.pack(padx=10, fill="both", expand=True)
        self.role_service = RoleService()
        self.datas = self.search()
        self.treeView = CustomTreeView(self.fram_view, self, self.datas, columns, len(columns) - 1)
    
    def search(self):
        rows = self.role_service.search()
        return rows
    
    def add(self):
        self.title_popup = "Thêm mới"
        form_popup = FormPopup(parent = self, title = self.title_popup,form_fields = self.fields,form_data = None, width=640, height=120)
    
    def edit(self, row_id):
        self.title_popup = "Cập nhập"
        data = self.role_service.getById(row_id)
        form_popup = FormPopup(parent = self, title = self.title_popup,form_fields = self.fields,form_data = data, width=640, height=120)

    def insert(self, data):
        confirm = messagebox.askyesno("Xác nhận thêm mới", "Bạn có chắc chắn muốn thêm mới ?")
        if confirm:
            result = self.role_service.insert(data)
            self.treeView.loadData()
            return True
        return False

    
    def update(self, data):
        confirm = messagebox.askyesno("Xác nhận cập nhập", "Bạn có chắc chắn muốn cập nhập ?")
        if confirm:
            result = self.role_service.update(data)
            self.treeView.loadData()
            return True
        return False
    
    def delete(self, row_id):
        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa nhân viên này?")
        if confirm:
            result = self.role_service.delete(row_id)
            self.treeView.loadData()
            return True
        return False

