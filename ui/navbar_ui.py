import tkinter as tk
from PIL import Image, ImageTk
from ui.pages.Overview import Overview
from ui.pages.Employee import Employee
from ui.pages.Contract import Contract
from ui.pages.License import License
from ui.pages.Role import Role
from ui.pages.Timesheet import Timesheet
from ui.pages.Department import Department
from ui.pages.Position import Position
from ui.pages.EmployeeRole import EmployeeRole
import globals




class Navbar(tk.Frame):
    def __init__(self, parent, frames):
        super().__init__(parent)
        #Navigation
        navigation = tk.Frame(self, bg="white", width=250)
        navigation.pack(side="left", fill="y")
        navigation.pack_propagate(False)   

        nav_user = tk.Frame(navigation, bg="yellow", height=140)
        nav_user.pack(fill="x")
        nav_user.pack_propagate(False)   
        nav_user_background_img = Image.open("./images/background/nav_user_background.jpg")
        self.nav_user_background_photo = ImageTk.PhotoImage(nav_user_background_img)
        nav_user_background_label = tk.Label(nav_user, image=self.nav_user_background_photo)
        nav_user_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        nav_user_image = Image.open("./images/icons/fingerprint.png")
        resized_nav_user_image = nav_user_image.resize((40,40))
        self.nav_user_image = ImageTk.PhotoImage(resized_nav_user_image)
        nav_user_image_label = tk.Label(nav_user, image=self.nav_user_image, bg="#0178bc", cursor="hand2")
        nav_user_image_label.pack(pady=20)

        label = tk.Label(nav_user, text= globals.current_user.username, font=("Arial", 16), bg="#0178bc", fg="white")
        label.pack()

        nav_main = tk.Frame(navigation, bg="white", height=420)
        nav_main.pack(fill="x", padx=10, pady=10)
        nav_main.pack_propagate(False)  

        self.buttons = []
        self.frames = frames
        
        button_main = self.CreateButtonNav(nav_main, "Tổng quan", "./images/icons/overview.png",True,lambda: self.change_color(button_main, Overview))
        button_main.pack()
        self.buttons.append(button_main)

        button_dep = self.CreateButtonNav(nav_main, "Phòng ban", "./images/icons/department.png",False,lambda: self.change_color(button_dep, Department))
        button_dep.pack()
        self.buttons.append(button_dep)

        button_position = self.CreateButtonNav(nav_main, "Chức vụ", "./images/icons/position.png",False,lambda: self.change_color(button_position, Position))
        button_position.pack()
        self.buttons.append(button_position)
        
        button_employee = self.CreateButtonNav(nav_main, "Nhân viên", "./images/icons/user_menu.png",False,lambda: self.change_color(button_employee, Employee))
        button_employee.pack()
        self.buttons.append(button_employee)

        button_timesheet = self.CreateButtonNav(nav_main,"Bảng chấm công", "./images/icons/timesheet.png",False,lambda: self.change_color(button_timesheet, Timesheet))
        button_timesheet.pack()
        self.buttons.append(button_timesheet)

        button_license = self.CreateButtonNav(nav_main,"Đơn từ", "./images/icons/license.png",False,lambda: self.change_color(button_license, License))
        button_license.pack()
        self.buttons.append(button_license)

        button_contract = self.CreateButtonNav(nav_main,"Hợp đồng", "./images/icons/contract.png",False,lambda: self.change_color(button_contract, Contract))
        button_contract.pack()
        self.buttons.append(button_contract)

        button_employee_role = self.CreateButtonNav(nav_main,"Phân quyền", "./images/icons/role_employee.png",False,lambda: self.change_color(button_employee_role, EmployeeRole))
        button_employee_role.pack()
        self.buttons.append(button_employee_role)

        button_role = self.CreateButtonNav(nav_main,"Quyền", "./images/icons/permission.png",False,lambda: self.change_color(button_role, Role))
        button_role.pack()
        self.buttons.append(button_role)


        
    def CreateButtonNav(self, parent, text, image_path,active, command):
        button_image = Image.open(image_path)
        resized_button_image = button_image.resize((20,20))
        self.button_image_photo = ImageTk.PhotoImage(resized_button_image)
        bg_button_active = "#0178bc" if active else "white"
        fg_button_active = "white" if active else "black"
        button = tk.Button(parent,
            image= self.button_image_photo,
            compound="left",
            text=text,font=(11),
            width=250,
            relief="flat",
            activebackground="#0178bc",
            activeforeground="white",
            cursor="hand2",
            highlightthickness=0,
            bd=0,
            pady=8,
            padx=10,
            bg=bg_button_active, 
            fg=fg_button_active,
            anchor="w",
            command= command
        )
        button.image = self.button_image_photo 
        return button
    
    def change_color(self, button, page):
        # Đặt màu cho các button
        for b in self.buttons:
            b.config(bg="white", fg="black")
        button.config(bg="#0178bc", fg="white")
        self.show_page(page)

    def show_page(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def initNav(self, content, parent):
        for F in (Overview, Department, Position, Employee, Contract, Role, Timesheet, License, EmployeeRole):
            frame = F(content, parent)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
