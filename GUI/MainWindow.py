import socket, uuid
from Pages import *
import GlobalVar as var

class MainWindow(QMainWindow):
    def __init__(self):  
        super().__init__()
        self.initializeUI()
        change_page.triggered.connect(self.changePage)

    def initializeUI(self):
        self.setMinimumSize(1024, 600)
        self.setWindowTitle("Fiteat")
        self.setWindowIcon(QIcon(file_path+"images/logo_rgb.png"))
        self.welcome_page = WelcomePage()
        self.start_page = StartPage()
        self.sign_in_page = SignInPage()
        self.menu_page = MenuPage()
        self.scan_package_page = ScanPackagePage()
        self.detect_food_page = DetectFoodPage()
        self.enter_info_page = EnterInfoPage()
        self.show_foodinfo_page = ShowFoodInfoPage()
        self.show_usercal_page = ShowUserCalPage()

        self.transition_anim = TransitionAnim()
        
        self.central_widget = QStackedWidget()
        self.central_widget.addWidget(self.welcome_page)
        self.central_widget.addWidget(self.start_page)
        self.central_widget.addWidget(self.sign_in_page)
        self.central_widget.addWidget(self.menu_page)
        self.central_widget.addWidget(self.scan_package_page)
        self.central_widget.addWidget(self.detect_food_page)
        self.central_widget.addWidget(self.enter_info_page)
        self.central_widget.addWidget(self.show_foodinfo_page)
        self.central_widget.addWidget(self.show_usercal_page)
        self.central_widget.addWidget(self.transition_anim)

        self.welcome_page.timer.start(12)
        self.central_widget.setCurrentWidget(self.welcome_page)
        self.setCentralWidget(self.central_widget)
    
    def changePage(self):
        if var.next_page == "Start":
            self.start_page.listUser()
            self.next_page = self.start_page
        elif var.next_page == "Menu":
            self.next_page = self.menu_page
        elif var.next_page == "Sign In":
            self.sign_in_page.clearUserName()
            self.next_page = self.sign_in_page
        elif var.next_page == "Scan Package":
            self.next_page = self.scan_package_page
        elif var.next_page == "Detect Food":
            self.next_page = self.detect_food_page
        elif var.next_page == "Enter Info":
            if var.create_new_account_flag:
                self.enter_info_page.showEmptyPage()
            else:
                self.enter_info_page.showUserInfo()
            self.next_page = self.enter_info_page
        elif var.next_page == "Show Food Info":
            self.next_page = self.show_foodinfo_page
        elif var.next_page == "Show User Cal":
            self.next_page = self.show_usercal_page
        self.transition_anim.start(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.showNormal()

    def closeEvent(self, event):
        super().closeEvent(event)
        QApplication.closeAllWindows()

def getID():
    try:
        with open(file_path+'id', 'r') as f:
            var.id = f.readlines()[0]
            f.close()
    except FileNotFoundError:
        with open(file_path+'id', 'w') as f:
            macaddr = uuid.UUID(int = uuid.getnode()).hex[-12:]
            var.id = macaddr
            f.write(var.id)
            f.close()
def getUserListFromLocal():
    try:
        with open(file_path+'user_list', 'r') as f:
            var.user_list = f.read().splitlines()
            f.close()
    except FileNotFoundError:
        with open(file_path+'user_list', 'w') as f:
            var.user_list = []
            f.close()
    print(var.user_list, len(var.user_list))

class TransitionAnim(QLabel):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.addOffset)

    def start(self, main_window: MainWindow):
        self.main_window = main_window
        self.grab_curr = main_window.grab()
        self.main_window.central_widget.setCurrentWidget(main_window.next_page)
        self.grab_next = main_window.grab()
        self.main_window.central_widget.setCurrentWidget(main_window.transition_anim)

        # Create timer object
        self.timer.start(10)
        self.offset = 0
    
    def paintEvent(self, event):
        super().paintEvent(event)
        self.painter = QPainter(self)
        if var.back_flag:
            self.painter.drawPixmap(0, 0+self.offset, self.grab_curr)
            self.painter.drawPixmap(0, -600+self.offset, self.grab_next)
        else:
            self.painter.drawPixmap(0, 0-self.offset, self.grab_curr)
            self.painter.drawPixmap(0, 600-self.offset, self.grab_next)
        self.painter.end()
    
    def addOffset(self):
        if self.offset >= 600:
            var.moveToNextPage()
            self.timer.stop()
            self.main_window.central_widget.setCurrentWidget(self.main_window.next_page)
        self.offset += 6
        self.update()

# Run main event loop
if __name__ == '__main__':
    getID()
    getUserListFromLocal()
    main_window = MainWindow()
    main_window.show()
    #main_window.showFullScreen()
    sys.exit(app.exec_())