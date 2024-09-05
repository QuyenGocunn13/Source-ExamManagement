import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox as mb
import customtkinter
from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup
import os

'''==================PHƯƠNG THỨC TĨNH=================='''
class UserManager:
    @staticmethod
    def save_user(username, password):
        user_data = {
            "username": username,
            "password": password,
            "role": "user"
        }
        try:
            with open("JSON/users.json", "r") as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []
        users.append(user_data)
        with open("JSON/users.json", "w") as file:
            json.dump(users, file, indent=4)

    @staticmethod
    def check_input_login(username, password):
        try:
            with open("JSON/users.json", "r") as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        for user in users:
            if user["username"] == username and user["password"] == password:
                return user["role"]
        return False

'''==================XỬ LÍ LOGIN-REG=================='''
class LoginApp:
    def __init__(self, root):
        self.applg = root
        self.applg.geometry("600x500")
        self.applg.title("ỨNG DỤNG QUẢN LÍ ĐỀ THI CHO GIÁO VIÊN")
        self.applg.resizable(0, 0)

        self.side_img = Image.open("assets/side-img.png")
        self.user_img = Image.open("assets/user-icon.png")
        self.pw_img = Image.open("assets/password-icon.png")

        self.side_img = ImageTk.PhotoImage(self.side_img.resize((300, 500)))
        self.user_icon = ImageTk.PhotoImage(self.user_img.resize((20, 20)))
        self.password_icon = ImageTk.PhotoImage(self.pw_img.resize((17, 17)))

        tk.Label(master=self.applg, image=self.side_img).pack(expand=True, side="left")

        self.login_frame = tk.Frame(master=self.applg, width=300, height=480, bg="#ffffff")
        self.login_frame.pack_propagate(0)
        self.login_frame.pack(expand=True, side="right")

        self.setup_login()

        self.reg_frame = tk.Frame(master=self.applg, width=300, height=480, bg="#ffffff")
        self.reg_frame.pack_propagate(0)
        self.setup_reg()

    '''==================GIAO DIỆN ĐĂNG NHẬP=================='''
    def setup_login(self):
        tk.Label(master=self.login_frame, text="Welcome Back!", fg="#124076", anchor="w", 
                 justify="left", font=("Arial Bold", 24), bg="#ffffff").pack(anchor="w", pady=(50, 5), padx=(25, 0))
        tk.Label(master=self.login_frame, text="Đăng nhập với tài khoản của bạn", fg="#7E7E7E", 
                 anchor="w", justify="left", font=("Arial Bold", 12), bg="#ffffff").pack(anchor="w", padx=(25, 0))

        tk.Label(master=self.login_frame, text="  Username:", fg="#124076", anchor="w", justify="left", 
                 font=("Arial Bold", 14), image=self.user_icon, 
                 compound="left", bg="#ffffff").pack(anchor="w", pady=(38, 0), padx=(25, 0))
        self.user_entry = tk.Entry(master=self.login_frame, width=30, bg="#EEEEEE", bd=1, fg="#000000")
        self.user_entry.pack(anchor="w", padx=(25, 0))

        tk.Label(master=self.login_frame, text="  Password:", fg="#124076", anchor="w", justify="left", 
                 font=("Arial Bold", 14), image=self.password_icon, 
                 compound="left", bg="#ffffff").pack(anchor="w", pady=(21, 0), padx=(25, 0))
        self.pw_entry = tk.Entry(master=self.login_frame, width=30, bg="#EEEEEE", bd=1, fg="#000000", show="*")
        self.pw_entry.pack(anchor="w", padx=(25, 0))

        self.warning_label = tk.Label(master=self.login_frame, text="", fg="red", bg="#ffffff")
        self.warning_label.pack(anchor="w", pady=(5, 0), padx=(25, 0))

        tk.Button(master=self.login_frame, text="Đăng nhập", bg="#124076", activebackground="#E44982", 
                  font=("Arial Bold", 12), fg="#ffffff", width=28, 
                  command=self.validate_login).pack(anchor="w", pady=(40, 0), padx=(25, 0))

        reg_label = tk.Label(master=self.login_frame, text="Chưa có tài khoản? ", fg="#7E7E7E", bg="#ffffff")
        reg_label.pack(anchor="w", pady=(10, 0), padx=(25, 0))

        register_frame = tk.Frame(master=self.login_frame, bg="#ffffff")
        register_frame.pack(anchor="w", padx=(25, 0))

        register_text = tk.Label(master=register_frame, text="Đăng ký", fg="#0000FF", 
                                 bg="#ffffff", cursor="hand2", font=("Arial Bold", 12))
        register_text.pack(side="left")
        register_text.bind("<Button-1>", lambda e: self.show_register())

    '''==================GIAO DIỆN ĐĂNG KÝ=================='''
    def setup_reg(self):
        tk.Label(master=self.reg_frame, text="TẠO TÀI KHOẢN!", fg="#124076", anchor="w", justify="left", 
                 font=("Arial Bold", 23), bg="#ffffff").pack(anchor="w", pady=(50, 5), padx=(25, 0))

        tk.Label(master=self.reg_frame, text="  Username:", fg="#124076", anchor="w", justify="left", 
                 font=("Arial Bold", 14), image=self.user_icon, 
                 compound="left", bg="#ffffff").pack(anchor="w", pady=(38, 0), padx=(25, 0))
        self.reg_user_entry = tk.Entry(master=self.reg_frame, width=30, bg="#EEEEEE", bd=1, fg="#000000")
        self.reg_user_entry.pack(anchor="w", padx=(25, 0))

        tk.Label(master=self.reg_frame, text="  Password:", fg="#124076", anchor="w", justify="left", 
                 font=("Arial Bold", 14), image=self.password_icon, 
                 compound="left", bg="#ffffff").pack(anchor="w", pady=(21, 0), padx=(25, 0))
        self.reg_pw_entry = tk.Entry(master=self.reg_frame, width=30, bg="#EEEEEE", bd=1, fg="#000000", show="*")
        self.reg_pw_entry.pack(anchor="w", padx=(25, 0))

        self.reg_warning_label = tk.Label(master=self.reg_frame, text="", fg="red", bg="#ffffff")
        self.reg_warning_label.pack(anchor="w", pady=(5, 0), padx=(25, 0))

        tk.Button(master=self.reg_frame, text="Đăng ký", bg="#124076", activebackground="#E44982", 
                  font=("Arial Bold", 13), fg="#ffffff", width=28, 
                  command=self.validate_reg).pack(anchor="w", pady=(40, 0), padx=(25, 0))

        login_label = tk.Label(master=self.reg_frame, text="Đã có tài khoản? Đăng nhập", 
                               font=("Arial", 10), fg="#152483", bg="#ffffff", cursor="hand2")
        login_label.pack(anchor="w", pady=(10, 0), padx=(25, 0))
        login_label.bind("<Button-1>", lambda e: self.show_login())

    def show_register(self):
        self.login_frame.pack_forget()
        self.reg_frame.pack(expand=True, side="right")

    def show_login(self):
        self.reg_frame.pack_forget()
        self.login_frame.pack(expand=True, side="right")

    '''==================KIỂM TRA THÔNG TIN ĐK=================='''
    def validate_reg(self):
        username = self.reg_user_entry.get()
        password = self.reg_pw_entry.get()
        if not username or not password:
            self.reg_warning_label.config(text="Username và Password không được bỏ trống", fg="red")
        elif len(password) < 8:
            self.reg_warning_label.config(text="Mật khẩu cần phải có tối thiểu 8 ký tự", fg="red")
        else:
            if self.validate_username_reg(username):  
                self.reg_warning_label.config(text="Username đã tồn tại!", fg="red")
            else:
                UserManager.save_user(username, password)
                self.reg_warning_label.config(text="Đăng ký thành công!", fg="green")

    def validate_username_reg(self, username):
        try:
            with open("JSON/users.json", "r") as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []
        for user in users:
            if user["username"] == username:
                return True
        return False

    '''==================KIỂM TRA THÔNG TIN ĐN=================='''
    def validate_login(self):
        username = self.user_entry.get()
        password = self.pw_entry.get()
        role = UserManager.check_input_login(username, password)
        if role:
            self.warning_label.config(text=f"Đăng nhập thành công! Role: {role}", fg="green")
            self.applg.destroy()
            #TẠO FILE ROLE.JSON ĐỂ XÁC ĐỊNH VAI TRÒ
            with open("JSON/role.json", "w") as role_file:
                json.dump({"role": role}, role_file)
            self.Start_app()
        else:
            self.warning_label.config(text="Kiểm tra lại username hoặc password.", fg="red")

    '''====VÀO TRANG CHỦ===='''
    def Start_app(self):
        main_app = tk.Tk()
        app = ExamApp(main_app)
        main_app.mainloop()

'''========Cấu hình chung giao diện Button CRUD========'''
class CustomButton(customtkinter.CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            text_color="white",
            font=('Arial Bold', 13),
            hover=True, #Sự kiện di chuột vào button
            hover_color="#0a3d04", #Màu khi di chuột vào
            height=30,
            width=60,
            border_width=2, #Độ dày viền
            corner_radius=5, #Độ cong viền
            border_color="#06D001", #Màu viền
            bg_color="#d4d4d4",
            fg_color="#363636"
        )

'''==================TRANG CHỦ - CRUD=================='''
class ExamApp:
    def __init__(self, root):
        self.app = root
        self.app.geometry("856x645")
        self.app.title("Exam Application")
        self.app.resizable(0, 0)
        self.menubar = tk.Menu(self.app)
        self.app.tk_setPalette(background='#F0EBE3', foreground='#000000', activeBackground='#207244', activeForeground='#ffffff')

        self.setuo_gui()
        self.role = None
        self.exam_names = []
        self.test_names = []
        self.current_list = ''

    '''====THIẾT LẬP GIAO DIỆN===='''
    def setuo_gui(self):
        self.create_sidebar()
        self.create_listbox()
        self.create_menubar()
        self.create_buttons()
        self.login()
        self.TrangChu()
        self.button_crawl.place_forget()
        self.button_xem.place_forget()
        self.button_them.place_forget()

    '''==================SIDEBAR=================='''
    def create_sidebar(self):
        self.sidebar = tk.Frame(master=self.app, bg="#0A6847", width=176, height=650)
        self.sidebar.pack_propagate(0)
        self.sidebar.pack(fill="y", anchor="w", side="left")

        logo_img_data = Image.open("assets/logo.png")
        logo_img_data.thumbnail((130, 130))
        self.logo_img = ImageTk.PhotoImage(logo_img_data)

        self.logo_label = tk.Label(master=self.sidebar, image=self.logo_img, bg="#0A6847")
        self.logo_label.pack(pady=(38, 0), anchor="center")

    '''==================LISTBOX=================='''
    def create_listbox(self):
        self.text_frame = tk.Frame(self.app, bg="white", width=680, height=645)
        self.text_frame.pack_propagate(0)
        self.text_frame.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(self.text_frame, width=60, height=10)
        self.listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.text_frame, orient="vertical", command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

    '''==================MENUBAR=================='''
    def create_menubar(self):
        self.addimage = tk.PhotoImage(file="assets/add_icon.png")
        self.deleteimage = tk.PhotoImage(file="assets/delete_icon.png")
        self.editimage = tk.PhotoImage(file="assets/edit_icon.png")
        self.crawlimage = tk.PhotoImage(file="assets/crawl_image.png")

        self.crud_menu = tk.Menu(self.menubar, tearoff=0, font=("Arial", 12))
        self.crud_menu.configure(background='#E5DDC5')
        self.menubar.add_cascade(label="CRUD", font="montserrat 12", menu=self.crud_menu) 
        self.menubar.configure(background='lightblue')

        self.crud_menu.add_command(label="Thêm", command=self.Add_Question, image=self.addimage, compound='left')
        self.crud_menu.add_command(label="Thư viện đề", command=self.Add_KhoDe, image=self.addimage, compound='left')
        self.crud_menu.add_command(label="Sửa", command=self.Edit_Question, image=self.editimage, compound='left')

        self.file_menu = tk.Menu(self.menubar, tearoff=0, font=("Arial", 12))
        self.menubar.add_cascade(label="FILE", font="montserrat 12", menu=self.file_menu)
        self.file_menu.configure(background='#F5DAD2') 
        self.file_menu.add_command(label="From Website", command=self.Crawl_Display, image=self.crawlimage, compound='left')
        self.app.config(menu=self.menubar)

    '''==================BUTTON=================='''
    def create_buttons(self):
        self.button_xem = self.create_button(self.sidebar, "assets/note.png", "Trang chủ", command=self.TrangChu)
        self.button_xem.pack(anchor="center", ipady=5, pady=(30, 0))

        self.button_dethi = self.create_button(self.sidebar, "assets/note.png", "Đề thi", command=self.Read_NameDT)
        self.button_dethi.pack(anchor="center", ipady=5, pady=(16, 0))

        self.button_baitap = self.create_button(self.sidebar, "assets/note.png", "Bài tập", command=self.Read_NameBT)
        self.button_baitap.pack(anchor="center", ipady=5, pady=(16, 0))

        self.button_thuvien = self.create_button(self.sidebar, "assets/note.png", "Thư viện đề", command=self.Read_KhoDe)
        self.button_thuvien.pack(anchor="center", ipady=5, pady=(16, 0))

        separator = tk.Frame(self.sidebar, height=2, width=150, bg="yellow")
        separator.pack(anchor="center", pady=(10, 0))

        self.button_logout = self.create_button(self.sidebar, "assets/exit.png", "Đăng xuất", command=self.logout)
        self.button_logout.pack(anchor="center", ipady=5, pady=(10, 0))
        self.button_quit = self.create_button(self.sidebar, "assets/out_image.png", "Thoát", command=self.app.destroy)
        self.button_quit.pack(anchor="center", ipady=5, pady=(16, 0))

        self.button_xoa = CustomButton(master=self.app, text="Xóa")
        self.button_xoa.place(x=780, y=5)

        self.button_xem = CustomButton(master=self.app, text="Xem", command=self.View_Question)
        self.button_xem.place(x=780, y=40)

        self.button_fix = CustomButton(master=self.app, text="Sửa", command=self.Edit_QuestionKD)
        self.button_fix.place(x=780, y=75)

        self.button_them = CustomButton(master=self.app, text="Thêm", command=self.Add_QuestionKD)
        self.button_them.place(x=780, y=75)

        self.button_crawl = CustomButton(master=self.app, text="Lấy", command=self.Add_FromCrawl)
        self.button_crawl.place(x=780, y=5)

    '''==================PHƯƠNG THỨC CHUNG CHO BUTTON=================='''
    def create_button(self, master, image_path, text, command=None):
        img_data = Image.open(image_path)
        img_data.thumbnail((32, 32))
        img = ImageTk.PhotoImage(img_data)
        button = tk.Button(master=master, image=img, text=text, compound=tk.LEFT, bg="#0A6847", font=("Arial Bold", 14), fg="#ffffff", bd=0, activebackground="#207244", command=command)
        button.image = img
        return button

    def TrangChu(self):
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, "Chào mừng đến với 'Exam App'")
        self.listbox.insert(tk.END, "Ứng dụng quản lí đễ thi/bài tập giành cho giáo viên")
        self.listbox.insert(tk.END, "Đồ án số 9 - Nhóm Chim Sơn Ca")
        self.listbox.insert(tk.END, "")
        self.listbox.insert(tk.END, "25 - Trần Huỳnh Phụng Quyên - 2001224008")
        self.listbox.insert(tk.END, "15 - Bùi Tuấn Kiệt - 2001221885")
        self.listbox.insert(tk.END, "13- Trần Thanh Huy - 2033221631")
        self.listbox.config(fg='#362FD9', font=('Arial Bold', 16))
        self.listbox.config(selectforeground='#FFEA20', selectbackground='#04364A')
        self.button_xem.place_forget()
        self.button_xoa.place_forget()
        self.button_fix.place_forget()
        self.button_them.place_forget()
        self.button_crawl.place_forget()

    '''==================XÁC ĐỊNH ROLE=================='''
    def read_role(self):
        try:
            with open('JSON/role.json', 'r') as file:
                data = json.load(file)
                self.role = data.get('role', None)
                if self.role == 'user' or self.role == 'admin':
                    return self.role
                else:
                    return None
        except FileNotFoundError:
            print("File role.json not found.")
            return None
        except json.JSONDecodeError:
            print("Error decoding JSON in role.json.")
            return None
    '''=====THÔNG BÁO VAI TRÒ====='''
    def login(self):
        role_ouput = self.read_role()
        if role_ouput:
            mb.showinfo("Thông báo", f"Bạn đã đăng nhập với vai trò {role_ouput}.")
        else:
            mb.showerror("Lỗi", "Không thể xác định vai trò.")

    '''======PHƯƠNG THỨC CHUNG CHO ĐỌC ĐỀ ('name')======'''
    def Read_Name(self, data_type):
        self.current_list = data_type
        names = []
        if not os.path.exists('JSON/practice.json'):
            return names
        try:
            with open('JSON/practice.json', 'r', encoding='utf-8') as f: 
                data = json.load(f)
                names = [("Đề", item['name']) for item in data.get(data_type, [])]  
        except json.JSONDecodeError:
            pass
        self.button_xoa.configure(command=self.Delete_Name)
        self.button_xoa.place(x=780, y=5)
        self.button_xem.place(x=780, y=40)
        self.button_fix.place_forget()
        self.button_them.place_forget()
        self.button_crawl.place_forget()
        self.Display_Name(names)

    def Read_NameDT(self):
        self.Read_Name('exams')

    def Read_NameBT(self):
        self.Read_Name('test')

    '''=====HIỂN THỊ CHUNG CHO ĐỀ====='''
    def Display_Name(self, names):  
        self.listbox.delete(0, tk.END)
        for name in names:
            self.listbox.insert(tk.END, f"{name[0]} - {name[1]}")  
        self.listbox.config(fg='#003C43', font=('Arial Bold', 14))
        self.listbox.config(selectforeground='#EE4E4E', selectbackground='#FFD0D0')

    '''=====ĐỌC THƯ VIỆN ĐỀ====='''
    def Read_KhoDe(self):
        role_output = self.read_role()
        self.listbox.delete(0, tk.END)
        count = 1
        with open('JSON/cauhoi.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            questions = data.get('questions', [])
        for question_data in questions:
            question_text = question_data['question']
            options = question_data['options']
            self.listbox.insert(tk.END, f"Câu {count}: {question_text}")
            for key, value in options.items():
                self.listbox.insert(tk.END, f"{key}. {value}")
            self.listbox.insert(tk.END, "")
            count += 1
        '''=====PHÂN QUYỀN DỰA TRÊN ROLE ĐÃ XÁC ĐỊNH Ở ROLE.JSON======'''
        if role_output == 'admin':
            self.button_xoa.configure(command=self.Delete_KhoDe)
            self.button_xoa.place(x=780, y=5)
            self.button_fix.place(x=780, y=40)
            self.button_them.place(x=780, y=75)
            self.button_xem.place_forget()
            self.button_crawl.place_forget()
            self.listbox.config(fg='#003C43', font=('Arial Bold', 14))
            self.listbox.config(selectforeground='#EE4E4E', selectbackground='#FFD0D0')
        else:
            self.button_xoa.place_forget()
            self.button_fix.place_forget()
            self.button_them.place_forget()
            self.button_xem.place_forget()
            self.button_crawl.place_forget()
            self.listbox.config(fg='#003C43', font=('Arial Bold', 14))
            self.listbox.config(selectforeground='#EE4E4E', selectbackground='#FFD0D0')

    '''======PHƯƠNG THỨC XÓA ĐỀ========'''
    def Delete_Name(self):
        selected_exam = self.listbox.curselection()
        if selected_exam:
            answer = mb.askyesno("Xóa mã đề", "Bạn có chắc chắn muốn xóa mã đề này?")
            if answer:
                index = selected_exam[0]
                with open('JSON/practice.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                exams = data.get('exams', [])
                tests = data.get('test', [])
                if self.current_list == 'exams':
                    exams.pop(index)
                elif self.current_list == 'test':
                    tests.pop(index)
                data['exams'] = exams
                data['test'] = tests
                with open('JSON/practice.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                if self.current_list == 'exams':
                    self.Read_NameDT()  
                    mb.showinfo("Thành công", "Đã xóa đề thành công!")
                elif self.current_list == 'test':
                    self.Read_NameBT() 
                    mb.showinfo("Thành công", "Đã xóa đề thành công!")
        else:
            mb.showerror("Lỗi", "Vui lòng chọn đề để xóa!")

    '''===PHƯƠNG THỨC XÓA CÂU HỎI TRONG ĐỀ===='''
    def Delete_Question(self):
        selected_item = self.listbox.curselection()
        if selected_item:
            index = selected_item[0]
            selected_question = self.listbox.get(index)
            question_name = selected_question.split(": ", 1)[1].strip()
            try:
                with open('JSON/practice.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except FileNotFoundError:
                mb.showerror("Lỗi", "Không tìm thấy tệp 'practice.json'.")
                return
            except json.JSONDecodeError:
                mb.showerror("Lỗi", "Lỗi khi đọc tệp 'practice.json'.")
                return
            found = False
            for category in data.get("exams", []) + data.get("test", []):
                questions = category.get('questions', [])
                for question in questions:
                    if question['question'] == question_name:
                        questions.remove(question)
                        found = True
                        break
                if found:
                    break
            if found:
                try:
                    with open('JSON/practice.json', 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                except IOError:
                    mb.showerror("Lỗi", "Không thể ghi vào tệp 'practice.json'.")
            else:
                mb.showerror("Lỗi", "Không tìm thấy câu hỏi để xóa.")

            if self.current_list == 'exams':    
                self.Read_NameDT()  
                mb.showinfo("Thành công", "Đã xóa câu hỏi thành công!")
            elif self.current_list == 'test':
                self.Read_NameBT() 
                mb.showinfo("Thành công", "Đã xóa câu hỏi thành công!")
        else:
            mb.showerror("Lỗi", "Vui lòng chọn câu hỏi để xóa")

    '''=====PHƯƠNG THỨC XÓA CÂU HỎI TỪ THƯ VIỆN ĐỀ====='''
    def Delete_KhoDe(self):
        selected_listbox = self.listbox.curselection()
        if selected_listbox:
            question_index = selected_listbox[0]
            question_text = self.listbox.get(question_index)
            question_number = int(''.join(filter(str.isdigit, question_text)))
            with open('JSON/cauhoi.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            questions = data.get('questions', [])
            listbox_count = question_number - 1
            if 0 <= listbox_count < len(questions):
                del questions[listbox_count]
                with open('JSON/cauhoi.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)

                mb.showinfo("Thành công", "Đã xóa câu hỏi thành công!")
                self.Read_KhoDe() 
            else:
                mb.showerror("Lỗi", "Không tìm thấy câu hỏi.")
        else:
            mb.showerror("Lỗi", "Vui lòng chọn câu hỏi để xóa")

    '''=====PHƯƠNG THỨC THÊM CÂU HỎI======'''
    def Add_Question(self):
        add_window = tk.Toplevel(self.app)
        add_window.title("Thêm câu hỏi")
        add_window.geometry("300x200")
        add_window.configure(bg='pink')

        type_label = tk.Label(add_window, text="Loại:", bg='pink')
        type_label.grid(row=0, column=0, padx=10, pady=5)

        type_var = tk.StringVar(add_window)
        type_var.set("Đề thi")
        type_cbox = ttk.Combobox(add_window, textvariable=type_var, values=["Đề thi", "Bài tập"])
        type_cbox.grid(row=0, column=1, padx=10, pady=5)

        pick_label = tk.Label(add_window, text="Lựa chọn:", bg='pink')
        pick_label.grid(row=1, column=0, padx=10, pady=5)

        action_var = tk.StringVar(add_window)
        action_var.set("Tạo mới")
        action_cbox = ttk.Combobox(add_window, textvariable=action_var, values=["Tạo mới", "Thêm câu hỏi"])
        action_cbox.grid(row=1, column=1, padx=10, pady=5)

        name_label = tk.Label(add_window, text="Tên mã đề:", bg='pink')
        name_label.grid(row=2, column=0, padx=10, pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=2, column=1, padx=10, pady=5)

        question_label = tk.Label(add_window, text="Câu hỏi:", bg='pink')
        question_label.grid(row=3, column=0, padx=10, pady=5)
        question_entry = tk.Entry(add_window)
        question_entry.grid(row=3, column=1, padx=10, pady=5)

        options_label = tk.Label(add_window, text="Đáp án:", bg='pink')
        options_label.grid(row=4, column=0, padx=10, pady=5)

        options_frame = tk.Frame(add_window, bg='pink')
        options_frame.grid(row=4, column=1, padx=10, pady=5)

        options = ["A", "B", "C", "D"]
        option_entries = []
        for option in options:
            option_label = tk.Label(options_frame, text=option, bg='pink')
            option_label.pack(side="left")
            option_entry = tk.Entry(options_frame, width=5)
            option_entry.pack(side="left")
            option_entries.append(option_entry)

        name_label.grid_remove()
        name_entry.grid_remove()

        namexams_label = tk.Label(add_window, text="Chọn mã đề:", bg='pink')
        namexams_label.grid(row=2, column=0, padx=10, pady=5)

        if os.path.exists('JSON/practice.json'):
            with open('JSON/practice.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"exams": [], "test": []}

        def show_hide_fields(event):
            if action_var.get() == "Tạo mới":
                name_label.grid()
                name_entry.grid()
                namexams_label.grid_remove()
                exam_cbox.grid_remove()
            elif action_var.get() == "Thêm câu hỏi":
                name_label.grid_remove()
                name_entry.grid_remove()
                if type_var.get() == "Đề thi":
                    namexams_label.grid()
                    exam_cbox.grid()
                    exam_cbox['values'] = [exam['name'] for exam in data.get('exams', [])]
                else:
                    namexams_label.grid()
                    exam_cbox.grid()
                    exam_cbox['values'] = [test['name'] for test in data.get('test', [])]

        action_cbox.bind("<<ComboboxSelected>>", show_hide_fields)
        exam_var = tk.StringVar(add_window)
        exam_cbox = ttk.Combobox(add_window, textvariable=exam_var, values=[])
        exam_cbox.grid(row=2, column=1, padx=10, pady=5)
        namexams_label.grid_remove()
        exam_cbox.grid_remove()

        '''=====LƯU THAO TÁC======'''
        def save_question():
            selected_action = action_var.get()
            selected_type = type_var.get()
            selected_name = name_entry.get()
            selected_question = question_entry.get()

            if not selected_question:
                mb.showerror("Lỗi", "Vui lòng nhập câu hỏi")
                return
            if selected_action == "Tạo mới":
                if not selected_name:
                    mb.showerror("Lỗi", "Vui lòng nhập tên câu hỏi")
                    return
                if selected_type == "Đề thi":
                    selected_list = "exams"
                else:
                    selected_list = "test"
                new_question = {
                    "question": selected_question,
                    "options": {option: entry.get() for option, entry in zip(options, option_entries)}
                }
                data[selected_list].append({"name": selected_name, "questions": [new_question]})
            elif selected_action == "Thêm câu hỏi":
                if selected_type == "Đề thi":
                    selected_list = "exams"
                else:
                    selected_list = "test"
                selected_name = exam_var.get()
                if not selected_name:
                    mb.showerror("Lỗi", "Vui lòng chọn mã đề để thêm câu hỏi")
                    return
                for item in data[selected_list]:
                    if item['name'] == selected_name:
                        item['questions'].append({
                            "question": selected_question,
                            "options": {option: entry.get() for option, entry in zip(options, option_entries)}
                        })
            with open('JSON/practice.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            if self.current_list == 'exams':
                self.Read_NameDT()  
            elif self.current_list == 'test':
                self.Read_NameBT() 
            mb.showinfo("Thành công", "Thêm câu hỏi thành công!")
            add_window.destroy()

        save_button = tk.Button(add_window, text="Lưu", font=('Arial Bold', 10), fg="green", borderwidth=3, relief="groove", command=save_question)
        save_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    '''=====PHƯƠNG THỨC THÊM CÂU HỎI TỪ THƯ VIỆN ĐỀ======'''
    def Add_KhoDe(self):
        add_window = tk.Toplevel(self.app)
        add_window.title("Thêm câu hỏi")
        add_window.geometry("300x150")
        add_window.configure(bg='pink')

        type_label = tk.Label(add_window, text="Loại:", bg='pink')
        type_label.grid(row=0, column=0, padx=10, pady=5)

        type_var = tk.StringVar(add_window)
        type_var.set("Đề thi") 
        type_cbox = ttk.Combobox(add_window, textvariable=type_var, values=["Đề thi", "Bài tập"])
        type_cbox.grid(row=0, column=1, padx=10, pady=5)

        pick_label = tk.Label(add_window, text="Chọn đề:", bg='pink')
        pick_label.grid(row=1, column=0, padx=10, pady=5)

        name_var = tk.StringVar(add_window)
        name_cbox = ttk.Combobox(add_window, textvariable=name_var)
        name_cbox.grid(row=1, column=1, padx=10, pady=5)

        question_label = tk.Label(add_window, text="Chọn câu hỏi:", bg='pink')
        question_label.grid(row=2, column=0, padx=10, pady=5)

        question_var = tk.StringVar(add_window)
        question_cbox = ttk.Combobox(add_window, textvariable=question_var)
        question_cbox.grid(row=2, column=1, padx=10, pady=5)

        if os.path.exists('JSON/practice.json'):
            with open('JSON/practice.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                exams = data.get('exams', [])
                tests = data.get('test', [])
        else:
            exams = []
            tests = []
        def update_names(event):
            selected_type = type_var.get()
            if selected_type == "Đề thi":
                name_cbox['values'] = [exam['name'] for exam in exams]
            elif selected_type == "Bài tập":
                name_cbox['values'] = [test['name'] for test in tests]

        type_cbox.bind("<<ComboboxSelected>>", update_names)

        with open('JSON/cauhoi.json', 'r', encoding='utf-8') as file:
            cauhoi_data = json.load(file)
            questions = cauhoi_data.get('questions', [])
        question_cbox['values'] = [f"Câu {i+1}" for i in range(len(questions))]

        def add_question():
            selected_type = type_var.get()
            selected_name = name_var.get()
            selected_questiondem = question_cbox.current()

            if selected_type == "" or selected_name == "" or selected_questiondem == -1:
                mb.showerror("Lỗi", "Vui lòng chọn đầy đủ thông tin!")
                return
            data_slt_question = questions[selected_questiondem]
            target_list = exams if selected_type == "Đề thi" else tests
            for item in target_list:
                if item['name'] == selected_name:
                    item['questions'].append(data_slt_question)
                    break
            with open('JSON/practice.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            if self.current_list == 'exams':
                self.Read_NameDT()  
            elif self.current_list == 'test':
                self.Read_NameBT() 
            mb.showinfo("Thành công", "Thêm câu hỏi thành công!")
            add_window.destroy()
        add_button = tk.Button(add_window, text="Thêm", font=('Arial Bold', 10), fg="green",borderwidth=3, relief="groove",command=add_question)
        add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        add_window.mainloop()

    '''=====PHƯƠNG THỨC THÊM CÂU HỎI TỪ WEBSITE======'''
    def Add_FromCrawl(self):
        selected_items = self.listbox.curselection()
        if selected_items:
            questions_data = {"questions": []}
            for index in selected_items:
                question_text = self.listbox.get(index)
                question_text = question_text.replace("Câu", "").split(":", 1)[1].strip()
                question_text = question_text.replace("–", "-")
                options = {}
                for i in range(index + 1, len(self.listbox.get(0, tk.END))):
                    if self.listbox.get(i).strip():
                        option, value = self.listbox.get(i).split(". ", 1)
                        option, value = option.replace("–", "-").strip(), value.strip()
                        options[option] = value
                    else:
                        break
                questions_data["questions"].append({"question": question_text, "options": options})
            if os.path.exists('JSON/cauhoi.json'):
                with open('JSON/cauhoi.json', 'r', encoding='utf-8') as file:
                    existing_data = json.load(file)
                    existing_data["questions"].extend(questions_data["questions"])
                with open('JSON/cauhoi.json', 'w', encoding='utf-8') as file:
                    json.dump(existing_data, file, indent=4, ensure_ascii=False)
            else:
                with open('JSON/cauhoi.json', 'w', encoding='utf-8') as file:
                    json.dump(questions_data, file, indent=4, ensure_ascii=False)
            
            mb.showinfo("Thành công", "Đã thêm câu hỏi vào thư viện đề!")
        else:
            mb.showerror("Lỗi", "Vui lòng chọn câu hỏi để thêm vào thư viện đề!")

    '''=====PHƯƠNG THỨC CHUNG XỬ LÍ LƯU/SỬA TRONG THƯ VIỆN ĐỀ======'''
    def QuestionKD(self, mode, question_data=None):
        window_title = "Thêm câu hỏi" if mode == "add" else "Chỉnh sửa câu hỏi"
        save_button_text = "Lưu câu hỏi" if mode == "add" else "Lưu thay đổi"
        
        kd_window = tk.Toplevel(self.app)
        kd_window.title(window_title)
        kd_window.geometry("300x150")
        kd_window.configure(bg='pink')
        
        question_label = tk.Label(kd_window, text="Câu hỏi:", bg='pink')
        question_label.grid(row=0, column=0, padx=10, pady=5)
        
        question_entry = tk.Entry(kd_window)
        question_entry.grid(row=0, column=1, padx=10, pady=5)
        if question_data:
            question_entry.insert(0, question_data['question'])
        
        options_label = tk.Label(kd_window, text="Tùy chọn:", bg='pink')
        options_label.grid(row=1, column=0, padx=10, pady=5)
        
        options_frame = tk.Frame(kd_window, bg='pink')
        options_frame.grid(row=1, column=1, padx=10, pady=5)
        
        options = ["A", "B", "C", "D"]
        option_entries = []
        for option in options:
            option_label = tk.Label(options_frame, text=option, bg='pink')
            option_label.pack(side="left")
            option_entry = tk.Entry(options_frame, width=5)
            option_entry.pack(side="left")
            if question_data:
                option_entry.insert(0, question_data['options'].get(option, ''))
            option_entries.append(option_entry)
        
        def save_question():
            new_question = {
                "question": question_entry.get(),
                "options": {option: entry.get() for option, entry in zip(options, option_entries)}
            }
            with open('JSON/cauhoi.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            if mode == "add":
                data.setdefault('questions', []).append(new_question)
            elif mode == "edit":
                for i, question in enumerate(data.get('questions', [])):
                    if question['question'] == question_data['question']:
                        data['questions'][i] = new_question
                        break
            with open('JSON/cauhoi.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            mb.showinfo("Thành công", "Thao tác thành công!")
            kd_window.destroy()
            self.Read_KhoDe()
        save_button = tk.Button(kd_window, text=save_button_text, fg="red", borderwidth=3, relief="groove", command=save_question)
        save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    #====Kế thừa QuestionKD========================
    def Add_QuestionKD(self):
        self.QuestionKD("add")
    #====Kế thừa QuestionKD========================
    def Edit_QuestionKD(self):
        selected_item = self.listbox.curselection()
        if selected_item:
            index = selected_item[0]
            selected_question_text = self.listbox.get(index).split(": ", 1)[1].strip()
            with open('JSON/cauhoi.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            questions = data.get('questions', [])
            for question in questions:
                if question['question'] == selected_question_text:
                    self.QuestionKD("edit", question)
                    break
            else:
                mb.showerror("Lỗi", "Không tìm thấy câu hỏi.")
        else:
            mb.showerror("Lỗi", "Vui lòng chọn câu hỏi để sửa.")

    '''=====PHƯƠNG THỨC CHỈNH SỬA CÂU HỎI======'''
    def Edit_Question(self):
        selected_item = self.listbox.curselection()
        if selected_item:
            index = selected_item[0]
            selected_question = self.listbox.get(index)
            question_type, question_name = selected_question.split(" - ", 1)
            if self.current_list == 'exams':
                data_type = "exams"
            elif self.current_list == 'test':
                data_type = "test"
            else:
                mb.showerror("Lỗi", "Không xác định được loại câu hỏi")
                return
            with open('JSON/practice.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            items = data.get(data_type, [])
            slt_itemi4 = None
            for item_info in items:
                if item_info['name'] == question_name:
                    slt_itemi4 = item_info
                    break
            if slt_itemi4:
                choose_window = tk.Toplevel(self.app)
                choose_window.title("Chỉnh sửa nội dung")
                choose_window.geometry("300x200")
                choose_window.configure(bg='lightblue')

                questions_listbox = tk.Listbox(choose_window)
                questions_listbox.pack(fill="both", expand=True)
                for question in slt_itemi4['questions']:
                    questions_listbox.insert(tk.END, question['question'])

                def edit_question_stl():
                    selected_listbox = questions_listbox.curselection()
                    if selected_listbox:
                        q_index = selected_listbox[0]
                        question_info = slt_itemi4['questions'][q_index]

                        edit_window = tk.Toplevel(self.app)
                        edit_window.title("Sửa câu hỏi")
                        edit_window.geometry("300x250")
                        edit_window.configure(bg='pink')

                        name_label = tk.Label(edit_window, text="Name:", bg='pink')
                        name_label.grid(row=0, column=0, padx=10, pady=5)
                        name_entry = tk.Entry(edit_window)
                        name_entry.insert(tk.END, slt_itemi4['name'])
                        name_entry.grid(row=0, column=1, padx=10, pady=5)

                        question_label = tk.Label(edit_window, text="Câu hỏi:", bg='pink')
                        question_label.grid(row=1, column=0, padx=10, pady=5)
                        question_entry = tk.Entry(edit_window)
                        question_entry.insert(tk.END, question_info['question'])
                        question_entry.grid(row=1, column=1, padx=10, pady=5)

                        options_label = tk.Label(edit_window, text="Đáp án:", bg='pink')
                        options_label.grid(row=2, column=0, padx=10, pady=5)

                        options_frame = tk.Frame(edit_window, bg='pink')
                        options_frame.grid(row=2, column=1, padx=10, pady=5)

                        options = ["A", "B", "C", "D"]
                        option_entries = []
                        for i, (option, value) in enumerate(question_info['options'].items()):
                            option_label = tk.Label(options_frame, text=option, bg='pink')
                            option_label.grid(row=i, column=0, padx=5, pady=5)
                            option_entry = tk.Entry(options_frame, width=5)
                            option_entry.insert(tk.END, value)
                            option_entry.grid(row=i, column=1, padx=5, pady=5)
                            option_entries.append(option_entry)

                        def save_question():
                            slt_itemi4['name'] = name_entry.get()
                            question_info['question'] = question_entry.get()
                            question_info['options'] = {option: entry.get() for option, entry in zip(options, option_entries)}
                            with open('JSON/practice.json', 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=4, ensure_ascii=False)
                            if self.current_list == 'exams':
                                self.Read_NameDT()
                            elif self.current_list == 'test':
                                self.Read_NameBT()
                            mb.showinfo("Thành công", "Cập nhật câu hỏi thành công!")
                            edit_window.destroy()
                        save_button = tk.Button(edit_window, text="Lưu", command=save_question)
                        save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
                        choose_window.destroy()
                    else:
                        mb.showerror("Lỗi", "Vui lòng chọn câu hỏi để sửa")
                select_button = tk.Button(choose_window, text="Chọn",fg="red", borderwidth=3, relief="groove", command=edit_question_stl)
                select_button.pack(pady=10)
            else:
                mb.showerror("Lỗi", "Không tìm thấy câu hỏi được chọn")
        else:
            mb.showerror("Lỗi", "Vui lòng chọn mã đề cần sửa")
    
    '''=====ĐỌC THƯ VIỆN ĐỀ======'''
    def View_Question(self):
        selected_item = self.listbox.curselection()
        if selected_item:
            index = selected_item[0]
            selected_question = self.listbox.get(index)
            if " - " in selected_question:
                question_type, question_name = selected_question.split(" - ", 1)
            else:
                question_name = selected_question
            with open('JSON/practice.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            items = data.get(self.current_list, [])
            slt_itemi4 = None
            for item_info in items:
                if item_info['name'] == question_name:
                    slt_itemi4 = item_info
                    break
            if slt_itemi4:
                self.listbox.delete(0, tk.END)
                for question in slt_itemi4['questions']:
                    self.listbox.insert(tk.END, f"Câu: {question['question']}")
                    for option, answer in question['options'].items():
                        self.listbox.insert(tk.END, f"{option}: {answer}")
                    self.listbox.insert(tk.END, "") 
            self.button_xoa.configure(command=lambda: self.Delete_Question())
            self.button_xoa.place(x=780, y=5)
            self.button_xem.place_forget()
            self.button_fix.place_forget()
            self.button_them.place_forget()
            self.button_crawl.place_forget()
        else:
            mb.showerror("Lỗi", "Vui lòng chọn đề để xem")

    '''====LẤY DỮ LIỆU CÂU HỎI TỪ WEBSITE======'''
    def CrawlToFile(self):
        url = 'https://vndoc.com/de-thi-trac-nghiem-mon-toan-tieu-hoc-190373#mcetoc_1dse3js9u1'
        response = requests.get(url)
        response.encoding = 'utf-8'
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        questions = soup.find_all('p', style="text-align:justify")
        stop_crawling = False
        questions_list = []
        current_question = None
        answers = []

        for p in questions:
            if p.find_previous('h3', id='mcetoc_1dse3js9u1'):
                stop_crawling = True
            if stop_crawling:
                break
            text = p.get_text().strip()
            if text.startswith('Câu'):
                if current_question and len(answers) == 4:
                    questions_list.append((current_question, answers))
                current_question = text
                answers = []
            elif text.startswith('A.'):
                answers.append(text)
            elif text.startswith('B.'):
                answers.append(text)
            elif text.startswith('C.'):
                answers.append(text)
            elif text.startswith('D.'):
                answers.append(text)
        if current_question and len(answers) == 4:
            questions_list.append((current_question, answers))
        return questions_list

    '''=====HIỂN THỊ CÂU HỎI TỪ HÀM 'CrawlToFile()'======'''
    def Crawl_Display(self):
        role_output = self.read_role()
        questions_list = self.CrawlToFile()
        self.listbox.delete(0, tk.END)
        for question, answers in questions_list:
            self.listbox.insert(tk.END, question)
            for answer in answers:
                self.listbox.insert(tk.END, answer)
            self.listbox.insert(tk.END, "")  
        #=============Phân quyền===================
        if role_output == 'admin':
            self.button_crawl.place(x=780, y=5)
            self.button_xem.place_forget()
            self.button_xoa.place_forget()
            self.button_fix.place_forget()
            self.button_them.place_forget()
        else: 
            self.button_crawl.place_forget()
            self.button_xem.place_forget()
            self.button_xoa.place_forget()
            self.button_fix.place_forget()
            self.button_them.place_forget()

    #=============Xử lí đăng xuất============
    def logout(self):
        self.app.destroy()
        main()

#=============Hàm chạy nội dung Login============
def main():
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()