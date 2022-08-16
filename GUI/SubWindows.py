from Components import *
import GlobalVar as var
import UserAPI

class SubWindow(QWidget):
    def __init__(self):  
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)

        close_yellow = QIcon()
        close_yellow.addPixmap(QPixmap(file_path+"/images/close_yellow.png"))
        self.close_btn = QToolButton()
        self.close_btn.setObjectName("close_window")
        self.close_btn.setIcon(close_yellow)
        self.close_btn.setIconSize(QSize(32, 32))
        self.close_btn.setMinimumSize(50, 50)
        self.close_btn.clicked.connect(self.deleteLater)
        self.title_lbl = QLabel()
        self.title_lbl.setObjectName("title_lbl")
        self.title_lbl.setStyleSheet("background-color: #000000;")

        self.title_box = QHBoxLayout()
        self.title_box.setSpacing(0)
        self.title_box.addWidget(self.title_lbl)
        self.title_box.addWidget(self.close_btn)

        self.sub_widget = QWidget()
        self.sub_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.addLayout(self.title_box)
        self.layout.addWidget(self.sub_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

class IDWindow(QWidget):
    def __init__(self):  
        super().__init__()
        self.setWindowTitle("Change ID")
        self.id_lbl = QLabel(" ID: ")
        self.id_lbl.setFont(QFont("Agency FB", 24))
        self.id_lineEdit = QLineEdit(var.id)
        self.id_lineEdit.setValidator(QRegExpValidator(QRegExp("[a-z0-9]+$")))
        self.id_lineEdit.returnPressed.connect(self.changeID)
        self.id_lineEdit.textChanged.connect(self.checkTextFormat)
        self.change_btn = BlackBtn("Change")
        self.change_btn.setMinimumWidth(140)
        self.change_btn.clicked.connect(self.changeID)

        self.layout = self.title_box = QHBoxLayout()
        self.layout.addItem(h_expander)
        self.layout.addWidget(self.id_lbl)
        self.layout.addWidget(self.id_lineEdit)
        self.layout.addWidget(self.change_btn)
        self.layout.addItem(h_expander)

        self.setLayout(self.layout)

    def setupLineEdit(self):
        self.id_lineEdit.setText(var.id)
        self.id_lineEdit.setStyleSheet("color: #000000; border-color: #000000;")

    def changeID(self):
        success = UserAPI.updateMachineID(var.id, self.id_lineEdit.text())
        if len(self.id_lineEdit.text()) == 12 and success:
            var.id = self.id_lineEdit.text()
            with open(file_path+'id', 'w') as f:
                f.write(var.id)
                f.close()
            print("id: ", var.id)
            self.close()
        else:
            self.id_lineEdit.setStyleSheet("color: #C00000; border-color: #C00000;")
    
    def checkTextFormat(self, text: str):
        if len(text) != 12:
            self.id_lineEdit.setStyleSheet("color: #C00000; border-color: #C00000;")
        else:
            self.id_lineEdit.setStyleSheet("color: #000000; border-color: #000000;")

class MsgWindow(QWidget):
    def __init__(self):  
        super().__init__()
        self.setWindowTitle("Error Message")
        self.setStyleSheet("background-color: #000000;")
        self.msg_lbl = QLabel("")
        self.msg_lbl.setFont(QFont("Agency FB", 24))
        self.msg_lbl.setStyleSheet("color: #FFC000;")

        self.layout = self.title_box = QHBoxLayout()
        self.layout.addItem(h_expander)
        self.layout.addWidget(self.msg_lbl)
        self.layout.addItem(h_expander)

        self.setLayout(self.layout)

    def setMsg(self, msg):
        self.msg_lbl.setText(msg)