from tkinter import W
from Components import *
from SubWindows import *
import GlobalVar as var
import UserAPI

msg_window = MsgWindow()

class WelcomePage(QWidget):
    def __init__(self):  
        super().__init__()
        self.initializeUI()
        print("id: ", var.id)

         # Create timer object
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.counter = -25

    def initializeUI(self):
        self.title_l = QLabel("FIT")
        self.title_l.setAlignment(Qt.AlignRight)
        self.title_l.setFont(QFont("Agency FB", 160))
        self.title_r = QLabel("EAT")
        self.title_r.setAlignment(Qt.AlignLeft)
        self.title_r.setFont(QFont("Agency FB", 160))
        self.title_l_box = QVBoxLayout()
        self.title_l_box.addItem(v_expander)
        self.title_l_box.addWidget(self.title_l)
        self.title_r_box = QVBoxLayout()
        self.title_r_box.addItem(v_expander)
        self.title_r_box.addWidget(self.title_r)

        pixmap = QPixmap(file_path+"images/logo.png")
        self.logo_pixmap = pixmap.scaledToWidth(180)
        self.logo_lbl = QLabel()
        
        self.sub_title = QLabel(" 2022 Google HPS ")
        self.sub_title.setAlignment(Qt.AlignCenter)
        self.sub_title.setFont(QFont("Agency FB", 40))

        self.black_bar_left = BlackBar()
        self.black_bar_left.setMinimumWidth(70)
        self.black_bar_right = BlackBar()
        self.black_bar_right.setMinimumWidth(70)

        self.title_box = QHBoxLayout()
        self.title_box.addItem(h_expander)
        self.title_box.addLayout(self.title_l_box)
        self.title_box.addWidget(self.logo_lbl)
        self.title_box.addLayout(self.title_r_box)
        self.title_box.addItem(h_expander)
        self.title_box.setSpacing(0)

        self.h_box = QHBoxLayout()
        self.h_box.addItem(h_expander)
        self.h_box.addWidget(self.black_bar_left)
        self.h_box.addWidget(self.sub_title)
        self.h_box.addWidget(self.black_bar_right)
        self.h_box.addItem(h_expander)

        self.layout = QVBoxLayout()
        self.layout.addItem(v_expander)
        self.layout.addLayout(self.title_box)
        self.layout.addLayout(self.h_box)
        self.layout.addItem(QSpacerItem(50, 50, QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.layout.addItem(v_expander)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

    def animate(self):
        self.counter += 1
        if self.counter > 0 and self.counter <= 90:
            self.logo_lbl.setMinimumWidth(self.counter*2)
            self.black_bar_left.setMinimumWidth(70+self.counter)
            self.black_bar_right.setMinimumWidth(70+self.counter)
        if self.counter == 90:
            self.logo_lbl.setPixmap(self.logo_pixmap)
        if self.counter == 120:
            self.timer.stop()
            var.next_page = "Start"
            change_page.trigger()

class StartPage(QWidget):
    def __init__(self):  
        super().__init__()
        self.initializeUI()
        self.use_another_account_btn.clicked.connect(self.leavePage)
        self.id_btn.clicked.connect(self.showIDWindow)

    def initializeUI(self):
        pixmap = QPixmap(file_path+"images/title.png").scaledToWidth(520)
        self.title = QLabel()
        self.title.setPixmap(pixmap)
        self.title.setAlignment(Qt.AlignCenter)

        self.use_another_account_btn = BlackBtn(icon="person_yellow")
        self.use_another_account_btn.setStyleSheet("text-align:left;")
        self.use_another_account_btn.setText(" Use another account ")
        self.use_another_account_btn.setMinimumWidth(430)
        self.id_btn = BlackBtn("ID")
        self.id_btn.setMinimumWidth(65)
        
        self.v_box = QVBoxLayout()
        self.listUser()
        self.h_box = QHBoxLayout()
        self.h_box.addItem(h_expander)
        self.h_box.addLayout(self.v_box)
        self.h_box.addItem(h_expander)
        self.h_box.setContentsMargins(0, 10, 0, 20)

        self.mid_layout = QVBoxLayout()
        self.mid_layout.addItem(v_expander)
        self.mid_layout.addWidget(self.title)
        self.mid_layout.addLayout(self.h_box)
        self.mid_layout.addItem(v_expander)
        self.mid_layout.setSpacing(9)

        self.widget_right = QWidget()
        self.widget_right.setMinimumWidth(100)
        self.widget_right_layout = QVBoxLayout(self.widget_right)
        self.widget_right_layout.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.widget_right_layout.addWidget(self.id_btn)
        self.widget_right_layout.addItem(v_expander)

        self.widget_left = QWidget()
        self.widget_left.setMinimumWidth(100)
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.widget_left)
        self.layout.addLayout(self.mid_layout)
        self.layout.addWidget(self.widget_right)
        self.setLayout(self.layout)

        self.id_window = IDWindow()

    def showIDWindow(self):
        self.id_window.setupLineEdit()
        self.id_window.show()
    
    def listUser(self):
        self.users_num = len(UserAPI.listUser(var.id))
        if self.users_num == 0:
            self.use_another_account_btn.setText(" Create new account ")
            self.user1 = QHBoxLayout()
            self.user2 = QHBoxLayout()

        else:
            self.use_another_account_btn.setText(" Use another account ")
            if len(var.user_list) == 0:
                self.user1 = QHBoxLayout()
                self.user2 = QHBoxLayout()
                self.use_another_account_btn.setText(" Sign in ")
            elif len(var.user_list) == 1:
                self.user1 = UserNameBtn(name = var.user_list[0])
                self.user2 = QHBoxLayout()  
            else:
                self.user1 = UserNameBtn(name = var.user_list[0])
                self.user2 = UserNameBtn(name = var.user_list[1])

        while True:
            item = self.v_box.takeAt(0)
            if item == None:    break
            del item
        self.v_box.addLayout(self.user1)
        self.v_box.addLayout(self.user2)
        self.v_box.addWidget(self.use_another_account_btn)

    def leavePage(self):
        if self.users_num == 0:
            var.next_page = "Enter Info"
            var.create_new_account_flag = True
        else:
            var.next_page = "Sign In"
        change_page.trigger()

class SignInPage(QWidget):
    def __init__(self):  
        super().__init__()
        self.initializeUI()
        self.create_account_btn.clicked.connect(self.jumpToEnterInfoPage)
        self.cancel_btn.clicked.connect(self.jumpToStartPage)
        self.signin_btn.clicked.connect(self.jumpToMenuPage)

    def initializeUI(self):
        self.title = QLabel("SIGN IN")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Agency FB", 64))
        self.title.setMinimumHeight(200)

        self.user_icon = QPixmap(file_path+"images/person_black.png").scaledToHeight(40)
        self.user_icon_lbl = QLabel()
        self.user_icon_lbl.setPixmap(self.user_icon)
        self.user_name_lbl = QLabel("User Name ")
        self.user_name_lbl.setFont(QFont("Agency FB", 24))
        self.line_edit = QLineEdit()
        self.line_edit.setMinimumHeight(70)
        self.create_account_btn = BlackBtn("Create new account", icon="plus_yellow")
        self.cancel_btn = BlackBtn("Cancel")
        self.signin_btn = BlackBtn("Sign in")

        self.user_box = QHBoxLayout()
        self.user_box.addWidget(self.user_icon_lbl)
        self.user_box.addWidget(self.user_name_lbl)
        self.user_box.addWidget(self.line_edit)

        self.h_box = QHBoxLayout()
        self.h_box.addWidget(self.cancel_btn)
        self.h_box.addWidget(self.signin_btn)

        self.v_box = QVBoxLayout()
        self.v_box.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.v_box.addWidget(self.title)
        self.v_box.addLayout(self.user_box)
        self.v_box.addWidget(self.create_account_btn)
        self.v_box.addLayout(self.h_box)
        self.v_box.addItem(v_expander)

        self.layout = QHBoxLayout()
        self.layout.addItem(h_expander)
        self.layout.addLayout(self.v_box)
        self.layout.addItem(h_expander)
        self.layout.setSpacing(12)
        self.setLayout(self.layout)
    
    def clearUserName(self):
        self.line_edit.setText("")
        
    def jumpToEnterInfoPage(self):
        var.next_page = "Enter Info"
        var.create_new_account_flag = True
        change_page.trigger()
    
    def jumpToStartPage(self):
        var.setBackPage()
        change_page.trigger()
    
    def jumpToMenuPage(self):
        user_name = self.line_edit.text()
        if UserAPI.checkAccount(user_name, var.id):
            UserNameBtn(user_name).selectUser()
        else:
            msg_window.setMsg("The account does not exist!")
            msg_window.show()

class MenuPage(QWidget):
    def __init__(self):  
        super().__init__()
        self.initializeUI()
        self.scan_pkg.image_btn.clicked.connect(self.jumpToScanPkgPage)
        self.detect_food.image_btn.clicked.connect(self.jumpToDetectFoodPage)
        self.enter_info.image_btn.clicked.connect(self.jumpToEnterInfoPage)
        self.signout_btn.clicked.connect(self.jumpToStartPage)

    def initializeUI(self):
        self.title = QLabel("MENU")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Agency FB", 64))
        self.title.setMinimumHeight(200)
        self.signout_btn = BlackBtn("Sign out")

        self.layout_mid = QVBoxLayout()
        self.layout_mid.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.layout_mid.addWidget(self.title)
        
        self.widget_right = QWidget()
        self.widget_right.setMinimumWidth(250)
        self.widget_right_layout = QVBoxLayout(self.widget_right)
        self.widget_right_layout.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.widget_right_layout.addWidget(self.signout_btn)
        self.widget_right_layout.addItem(v_expander)
        self.widget_left = QWidget()
        self.widget_left.setMinimumWidth(250)
        self.title_box = QHBoxLayout()
        self.title_box.addWidget(self.widget_left)
        self.title_box.addLayout(self.layout_mid)
        self.title_box.addWidget(self.widget_right)

        self.scan_pkg = MenuItem()
        self.scan_pkg.setupName("Scan food\npackage")
        self.scan_pkg.setupImage("scan_package")
        self.detect_food = MenuItem()
        self.detect_food.setupName("Detect and\nweight food")
        self.detect_food.setupImage("detect_food")
        self.enter_info = MenuItem()
        self.enter_info.setupName("Enter\npersonal info")
        self.enter_info.setupImage("enter_info")

        self.h_box = QHBoxLayout()
        self.h_box.setSpacing(100)
        self.h_box.addItem(h_expander)
        self.h_box.addLayout(self.scan_pkg.layout)
        self.h_box.addLayout(self.detect_food.layout)
        self.h_box.addLayout(self.enter_info.layout)
        self.h_box.addItem(h_expander)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.title_box)
        self.layout.addLayout(self.h_box)
        self.layout.addItem(v_expander)
        self.setLayout(self.layout)
    
    def jumpToScanPkgPage(self):
        var.next_page = "Scan Package"
        change_page.trigger()

    def jumpToDetectFoodPage(self):
        var.next_page = "Detect Food"
        change_page.trigger()

    def jumpToEnterInfoPage(self):
        var.next_page = "Enter Info"
        change_page.trigger()

    def jumpToStartPage(self):
        var.next_page = "Start"
        var.back_flag = True
        change_page.trigger()

class ScanPackagePage(QWidget):
    def __init__(self):  
        super().__init__()
        self.initializeUI()
        self.cancel_btn.clicked.connect(self.jumpToMenuPage)

    def initializeUI(self):
        self.title = QLabel("Scan\nfood\npackage")
        self.title.setObjectName("yellow_title")
        self.title.setAlignment(Qt.AlignCenter)

        self.entry_btn = YellowBtn("Manual\nEntry")
        self.cancel_btn = YellowBtn("Cancel")

        self.camara_lbl = QLabel()
        self.camara_lbl.setObjectName("camara_lbl")
        self.camara_lbl.setStyleSheet("#camara_lbl{background-color: #FFFFFF;}") # TODO: change this line to get camera image
        self.camara_lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.sub_layout = QVBoxLayout()
        self.sub_layout.setSpacing(10)
        self.sub_layout.addWidget(self.title)
        self.sub_layout.addItem(v_expander)
        self.sub_layout.addWidget(self.entry_btn)
        self.sub_layout.addWidget(self.cancel_btn)
        self.sub_layout.setContentsMargins(25, 35, 25, 35)

        self.sub_widget = QWidget()
        self.sub_widget.setObjectName("sub_widget")
        self.sub_widget.setMinimumWidth(250)
        self.sub_widget.setLayout(self.sub_layout)

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.addWidget(self.sub_widget)
        self.layout.addWidget(self.camara_lbl)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def jumpToMenuPage(self):
        var.setBackPage()
        change_page.trigger()

class DetectFoodPage(ScanPackagePage):
    def __init__(self):  
        super().__init__()
        self.title.setText("Detect\nand\nweight\nfood")
        self.weight_lbl = QLabel("0.0"+" g ") # TODO: change weight number
        self.weight_lbl.setMinimumWidth(120)
        self.weight_lbl.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.weight_lbl.setFont(QFont("Agency FB", 24))
        self.tare_btn = BlackBtn("TARE")
        self.tare_btn.setMinimumWidth(130)

        self.h_box = QHBoxLayout()
        self.h_box.setSpacing(15)
        self.h_box.addItem(h_expander)
        self.h_box.addWidget(self.tare_btn)
        self.h_box.addWidget(self.weight_lbl)

        self.v_box = QVBoxLayout(self.camara_lbl)
        self.v_box.addLayout(self.h_box)
        self.v_box.addItem(v_expander)

class EnterInfoPage(ScanPackagePage):
    def __init__(self): 
        super().__init__()
        self.title.setText("")
        self.setFocusPolicy(Qt.ClickFocus)
        self.user_name_lbl = QLabel("User Name  ")
        self.user_name_lbl.setFont(QFont("Agency FB", 24))
        self.user_name_line_edit = QLineEdit()
        self.user_name_line_edit.setMaximumHeight(70)

        self.height_lbl = QLabel("Height")
        self.height_lbl.setFont(QFont("Agency FB", 24))
        self.height_line_edit = QLineEdit()
        self.height_line_edit.setMaximumHeight(70)
        self.height_line_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.height_line_edit.setValidator(QRegExpValidator(QRegExp("^(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*))$")))
        self.height_unit_lbl = QLabel("cm ")
        self.height_unit_lbl.setFont(QFont("Agency FB", 24))
        self.height_unit_lbl.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.height_unit_lbl.setMinimumWidth(50) 
        self.height_box = QHBoxLayout()
        self.height_box.addWidget(self.height_line_edit)
        self.height_box.addWidget(self.height_unit_lbl)

        self.weight_lbl = QLabel("Weight")
        self.weight_lbl.setFont(QFont("Agency FB", 24))
        self.weight_line_edit = QLineEdit()
        self.weight_line_edit.setMaximumHeight(70)
        self.weight_line_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.weight_line_edit.setValidator(QRegExpValidator(QRegExp("^(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*))$")))
        self.weight_unit_lbl = QLabel("kg ")
        self.weight_unit_lbl.setFont(QFont("Agency FB", 24))
        self.weight_unit_lbl.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.weight_unit_lbl.setMinimumWidth(50) 
        self.weight_box = QHBoxLayout()
        self.weight_box.addWidget(self.weight_line_edit)
        self.weight_box.addWidget(self.weight_unit_lbl)
        
        self.gender_lbl = QLabel("Gender")
        self.gender_lbl.setFont(QFont("Agency FB", 24))
        self.gender_btn_group = QButtonGroup()
        self.gender_btn_group.setExclusive(True)
        self.male_btn = CheckBtn("male")
        self.female_btn = CheckBtn("female")
        self.male_btn.setChecked(True)
        self.gender_btn_group.addButton(self.male_btn)
        self.gender_btn_group.addButton(self.female_btn)
        self.gender_box = QHBoxLayout()
        self.gender_box.addWidget(self.male_btn)
        self.gender_box.addWidget(self.female_btn)

        self.workload_lbl = QLabel("Workload")
        self.workload_lbl.setFont(QFont("Agency FB", 24))
        self.workload_btn_group = QButtonGroup()
        self.workload_btn_group.setExclusive(True)
        self.light_btn = CheckBtn("light")
        self.mid_btn = CheckBtn("mid")
        self.heavy_btn = CheckBtn("heavy")
        self.light_btn.setChecked(True)
        self.workload_btn_group.addButton(self.light_btn)
        self.workload_btn_group.addButton(self.mid_btn)
        self.workload_btn_group.addButton(self.heavy_btn)
        self.workload_box = QHBoxLayout()
        self.workload_box.addWidget(self.light_btn)
        self.workload_box.addWidget(self.mid_btn)
        self.workload_box.addWidget(self.heavy_btn)

        self.bmi_lbl = QLabel("BMI")
        self.bmi_lbl.setMinimumHeight(60)
        self.bmi_lbl.setFont(QFont("Agency FB", 24))
        self.bmi_number_lbl = QLabel("0")
        self.bmi_number_lbl.setFont(QFont("Agency FB", 24))

        self.tdee_lbl = QLabel("TDEE")
        self.tdee_lbl.setMinimumHeight(60)
        self.tdee_lbl.setFont(QFont("Agency FB", 24))
        self.tdee_number_lbl = QLabel("0")
        self.tdee_number_lbl.setFont(QFont("Agency FB", 24))
        self.tdee_unit_lbl = QLabel("Kcal/day")
        self.tdee_unit_lbl.setFont(QFont("Agency FB", 24))

        self.tdee_box = QHBoxLayout()
        self.tdee_box.addWidget(self.tdee_number_lbl)
        self.tdee_box.addItem(h_expander)
        self.tdee_box.addWidget(self.tdee_unit_lbl)

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.user_name_lbl, 0, 0)        
        self.grid_layout.addWidget(self.height_lbl, 1, 0)
        self.grid_layout.addWidget(self.weight_lbl, 2, 0)
        self.grid_layout.addWidget(self.gender_lbl, 3, 0)
        self.grid_layout.addWidget(self.workload_lbl, 4, 0)
        self.grid_layout.addWidget(self.bmi_lbl, 5, 0)
        self.grid_layout.addWidget(self.tdee_lbl, 6, 0)

        self.grid_layout.addWidget(self.user_name_line_edit, 0, 1)
        self.grid_layout.addLayout(self.height_box, 1, 1)
        self.grid_layout.addLayout(self.weight_box, 2, 1)
        self.grid_layout.addLayout(self.gender_box, 3, 1)
        self.grid_layout.addLayout(self.workload_box, 4, 1)
        self.grid_layout.addWidget(self.bmi_number_lbl, 5, 1)
        self.grid_layout.addLayout(self.tdee_box, 6, 1)
        self.grid_layout.setSpacing(10)

        self.sub_layout_left = QVBoxLayout()
        self.sub_layout_left.addItem(v_expander)
        self.sub_layout_left.addLayout(self.grid_layout)
        self.sub_layout_left.addItem(v_expander)
        self.sub_layout_left.setContentsMargins(90, 0, 100, 0)

        self.camara_lbl.deleteLater()
        self.entry_btn.setText("Done")
        self.layout.addLayout(self.sub_layout_left)

        self.user_name_line_edit.textChanged.connect(self.textName)
        self.height_line_edit.textChanged.connect(self.textHeight)
        self.weight_line_edit.textChanged.connect(self.textWeight)
        self.height_line_edit.editingFinished.connect(self.changeValue)
        self.weight_line_edit.editingFinished.connect(self.changeValue)
        self.light_btn.clicked.connect(self.changeValue)
        self.mid_btn.clicked.connect(self.changeValue)
        self.heavy_btn.clicked.connect(self.changeValue)
        self.male_btn.clicked.connect(self.changeValue)
        self.female_btn.clicked.connect(self.changeValue)
    
    def textName(self, text: str):
        self.user_name_lbl.setStyleSheet("color: #000000;")
        self.user_name_line_edit.setStyleSheet("color: #000000; border-color: #000000;")
    
    def textHeight(self, text: str):
        self.height_lbl.setStyleSheet("color: #000000;")
        self.height_line_edit.setStyleSheet("color: #000000; border-color: #000000;")
        self.height_unit_lbl.setStyleSheet("color: #000000;")

    def textWeight(self, text: str):
        self.weight_lbl.setStyleSheet("color: #000000;")
        self.weight_line_edit.setStyleSheet("color: #000000; border-color: #000000;")
        self.weight_unit_lbl.setStyleSheet("color: #000000;")

    def changeValue(self):
        height_text = self.height_line_edit.text()
        weight_text = self.weight_line_edit.text()
        self.height = 0 if (height_text == '') else float(height_text)
        self.weight = 0 if (weight_text == '') else float(weight_text)
        self.gender = 1 if self.male_btn.isChecked() else 0

        if   self.light_btn.isChecked():          self.workload = 'light'
        elif self.mid_btn.isChecked():            self.workload = 'mid'
        elif self.heavy_btn.isChecked():          self.workload = 'heavy'

        self.height_line_edit.setText(str(round(self.height, 1)))
        self.weight_line_edit.setText(str(round(self.weight, 1)))
        self.bmi_number_lbl.setText(str(var.computeBMI(self.height, self.weight)))
        self.tdee_number_lbl.setText(str(var.computeTDEE(self.height, self.weight, self.workload, self.gender)))
        self.update()

    def showUserInfo(self):
        self.title.setText("Enter\npersonal\ninfo")
        self.entry_btn.setText("Done")
        self.user_name_line_edit.setText(var.user.name)
        self.height_line_edit.setText(str(var.user.height))
        self.weight_line_edit.setText(str(var.user.weight))
        if var.user.gender == 1:
            self.male_btn.setChecked(True)
        else:
            self.female_btn.setChecked(True)
        if var.user.workload == 'light':
            self.light_btn.setChecked(True)
        elif var.user.workload == 'mid':
            self.mid_btn.setChecked(True)
        elif var.user.workload == 'heavy':
            self.heavy_btn.setChecked(True)
        self.bmi_number_lbl.setText(str(var.user.BMI))
        self.tdee_number_lbl.setText(str(var.user.TDEE))
        self.height = var.user.height
        self.weight = var.user.weight
        self.workload = var.user.workload
        self.gender = var.user.gender
        var.next_page = "Menu"

        try: self.entry_btn.clicked.disconnect() 
        except Exception: pass
        self.entry_btn.clicked.connect(self.updateUserInfo)

    def showEmptyPage(self):
        self.title.setText("Create\nnew\naccount")
        self.entry_btn.setText("Create")
        self.user_name_line_edit.setText("")
        self.height_line_edit.setText("")
        self.weight_line_edit.setText("")
        self.male_btn.setChecked(True)
        self.light_btn.setChecked(True)
        self.bmi_number_lbl.setText("0")
        self.tdee_number_lbl.setText("0")
        self.height = 0
        self.weight = 0
        self.workload = "light"
        self.gender = 1
        var.next_page = "Sign In"

        try: self.entry_btn.clicked.disconnect() 
        except Exception: pass
        self.entry_btn.clicked.connect(self.createNewUser)

    def checkInfoComplete(self):
        self.name = self.user_name_line_edit.text()
        if self.name.replace(" ", "") == "":
            self.user_name_lbl.setStyleSheet("color: #C00000;")
            self.user_name_line_edit.setStyleSheet("color: #C00000; border-color: #C00000;")
            msg_window.setMsg("User name cannot be empty!")
            msg_window.show()
            return False
        if self.height <= 0:
            self.height_lbl.setStyleSheet("color: #C00000;")
            self.height_line_edit.setStyleSheet("color: #C00000; border-color: #C00000;")
            self.height_unit_lbl.setStyleSheet("color: #C00000;")
            msg_window.setMsg("Height should be >0")
            msg_window.show()
            return False
        if self.weight <= 0:
            self.weight_lbl.setStyleSheet("color: #C00000;")
            self.weight_line_edit.setStyleSheet("color: #C00000; border-color: #C00000;")
            self.weight_unit_lbl.setStyleSheet("color: #C00000;")
            msg_window.setMsg("Weight should be >0")
            msg_window.show()
            return False
        return True

    def updateUserInfo(self):
        if self.checkInfoComplete():
            #user= (new_account_name,height,weight,workload,gender,calories,fat,carbs,protein,account,machine_id)
            info_list = (self.name, self.height, self.weight, self.workload, self.gender, 0, 0, 0, 0, var.user.name, var.id)
            print(info_list)
            if self.name != var.user.name:
                var.user_list[0] = self.name
                with open(file_path+'user_list', 'w') as f:
                    for ul in var.user_list:
                        f.write(ul+'\n')
                    f.close()
            UserAPI.updateUser(info_list)
            var.back_flag = True
            change_page.trigger()

    def createNewUser(self):
        if self.checkInfoComplete():
            #user = (account,machine_id,height,weight,workload,gender,calories,fat,carbs,protein)
            info_list = (self.name, var.id, self.height, self.weight, self.workload, self.gender, 0, 0, 0, 0)
            print(info_list)
            if UserAPI.createUser(info_list):
                var.back_flag = True
                change_page.trigger()
            else:
                self.user_name_lbl.setStyleSheet("color: #C00000;")
                self.user_name_line_edit.setStyleSheet("color: #C00000; border-color: #C00000;")
                msg_window.setMsg("Account has already existed!")
                msg_window.show()

class EnterBarcodePage(QWidget):
    def __init__(self):  
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.text_lbl = QLabel("Enter barcode: ")
        self.text_lbl.setFont(QFont("Agency FB", 24))
        self.line_edit = QLineEdit()

class ShowFoodInfoPage(QWidget):
    def __init__(self):  
        super().__init__()
        self.initializeUI()
        self.weight_line_edit.focus_out.triggered.connect(self.changeCal)

    def initializeUI(self):
        self.food_name_lbl = QLabel("banana")
        self.food_name_lbl.setFont(QFont("Agency FB", 40))
        self.cal_lbl = QLabel("30 Kcal")
        self.cal_lbl.setFont(QFont("Agency FB", 36))
        self.title_box = QHBoxLayout()
        self.title_box.addWidget(self.food_name_lbl)
        self.title_box.addItem(h_expander)
        self.title_box.addWidget(self.cal_lbl)
        
        self.black_bar = BlackBar()
        self.black_bar.setMinimumHeight(25)

        self.weight_lbl = QLabel("Weight")
        self.weight_lbl.setFont(QFont("Agency FB", 24))
        self.weight_lbl.setMinimumHeight(55)
        self.weight_line_edit = WeightEditLine("100.0 g")       
        self.weight_box = QHBoxLayout()
        self.weight_box.addWidget(self.weight_lbl)
        self.weight_box.addItem(h_expander)
        self.weight_box.addWidget(self.weight_line_edit)

        self.carb = Nutrition("Carbs")
        self.protein = Nutrition("Protein")
        self.fat  = Nutrition("Fat")
        
        self.cancel_btn = BlackBtn("Cancel")
        self.save_btn = BlackBtn("Save")
        self.btn_box = QHBoxLayout()
        self.btn_box.setSpacing(30)
        self.btn_box.addWidget(self.cancel_btn)
        self.btn_box.addWidget(self.save_btn)
        self.btn_box.setContentsMargins(100, 10, 100, 10)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.addItem(v_expander)
        self.layout.addLayout(self.title_box)
        self.layout.addWidget(self.black_bar)
        self.layout.addLayout(self.weight_box)
        self.layout.addLayout(self.carb.layout)
        self.layout.addLayout(self.protein.layout)
        self.layout.addLayout(self.fat.layout)
        self.layout.addLayout(self.btn_box)
        self.layout.addItem(v_expander)
        self.layout.setContentsMargins(170, 20, 170, 0)
        self.setLayout(self.layout)
        self.setFocusPolicy(Qt.ClickFocus)

    def changeCal(self):
        print("changeCal")

class ShowUserCalPage(QWidget):
    def __init__(self):  
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.user_name_lbl = QLabel("AAA")
        self.user_name_lbl.setFont(QFont("Agency FB", 40))
        
        self.black_bar = BlackBar()
        self.black_bar.setMinimumHeight(25)

        self.calories = Nutrition("Calories", show_ratio=True)
        self.carb = Nutrition("Carbs", show_ratio=True)
        self.protein = Nutrition("Protein", show_ratio=True)
        self.fat  = Nutrition("Fat", show_ratio=True)

        self.layout_left = QVBoxLayout()
        self.layout_left.setSpacing(0)
        self.layout_left.addItem(v_expander)
        self.layout_left.addWidget(self.user_name_lbl)
        self.layout_left.addWidget(self.black_bar)
        self.layout_left.addLayout(self.calories.layout)
        self.layout_left.addLayout(self.carb.layout)
        self.layout_left.addLayout(self.protein.layout)
        self.layout_left.addLayout(self.fat.layout)
        self.layout_left.addItem(v_expander)
        self.layout_left.setContentsMargins(100, 0, 50, 0)

        self.progress_circle = ProgressCircle()
        self.back_btn = BlackBtn("Back")
        self.back_btn.setMinimumWidth(130)
        self.h_box = QHBoxLayout()
        self.h_box.addItem(h_expander)
        self.h_box.addWidget(self.back_btn)

        self.layout_right = QVBoxLayout()
        self.layout_right.addWidget(self.progress_circle)
        self.layout_right.addLayout(self.h_box)
        self.layout_right.setContentsMargins(0, 100, 30, 30)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.layout_left)
        self.layout.addLayout(self.layout_right)
        self.setLayout(self.layout)