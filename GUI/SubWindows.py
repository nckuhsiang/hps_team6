from Components import *
import GlobalVar as var
import UserAPI

class MsgWindow(QWidget):
    def __init__(self):  
        super().__init__()
        self.setWindowTitle("Error Message")
        self.setStyleSheet("background-color: #000000;")
        self.msg_lbl = QLabel("")
        self.msg_lbl.setFont(QFont("Agency FB", font_normal_size))
        self.msg_lbl.setStyleSheet("color: #FFC000;")

        self.layout = self.title_box = QHBoxLayout()
        self.layout.addItem(h_expander)
        self.layout.addWidget(self.msg_lbl)
        self.layout.addItem(h_expander)

        self.setLayout(self.layout)

    def setMsg(self, msg):
        self.msg_lbl.setText('ERROR: '+msg)
        self.move(250, 100)

msg_window = MsgWindow()

class IDWindow(QWidget):
    def __init__(self):  
        super().__init__()
        self.setWindowTitle("Enter your old machine ID")
        self.id_lbl = QLabel(" ID: ")
        self.id_lbl.setFont(QFont("Agency FB", font_normal_size))
        self.id_lineEdit = LineEdit()
        self.id_lineEdit.setText(var.id)
        self.id_lineEdit.returnPressed.connect(self.changeID)
        self.id_lineEdit.textChanged.connect(self.checkTextFormat)
        self.change_btn = BlackBtn("Change")
        self.change_btn.setMinimumWidth(140)
        self.change_btn.clicked.connect(self.changeID)

        self.layout = QHBoxLayout()
        self.layout.addItem(h_expander)
        self.layout.addWidget(self.id_lbl)
        self.layout.addWidget(self.id_lineEdit)
        self.layout.addWidget(self.change_btn)
        self.layout.addItem(h_expander)

        self.setLayout(self.layout)

    def setupLineEdit(self):
        self.move(250, 100)
        self.id_lineEdit.setText(var.id)
        self.id_lineEdit.setStyleSheet("color: #000000; border-color: #000000;")

    def changeID(self):
        success = UserAPI.updateMachineID(var.id, self.id_lineEdit.text())
        if not len(self.id_lineEdit.text())== 12:
            self.id_lineEdit.setStyleSheet("color: #C00000; border-color: #C00000;")
            msg_window.setMsg("ID must be 12 chars!")
            msg_window.show()
        elif not success:
            self.id_lineEdit.setStyleSheet("color: #C00000; border-color: #C00000;")
            msg_window.setMsg("ID doesn't exist.")
            msg_window.show()
        else:
            var.id = self.id_lineEdit.text()
            with open(file_path+'id', 'w') as f:
                f.write(var.id)
                f.close()
            print("id: ", var.id)
            self.close()            
    
    def checkTextFormat(self, text: str):
        self.id_lineEdit.setText(self.id_lineEdit.text().lower())
        if len(text) != 12:
            self.id_lineEdit.setStyleSheet("color: #C00000; border-color: #C00000;")
        else:
            self.id_lineEdit.setStyleSheet("color: #000000; border-color: #000000;")