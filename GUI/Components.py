import sys, os, time
import cv2
import GlobalVar as var
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from StyleSheet import style_sheet
from numpy import ndarray
import UserAPI
import BarcodeAPI

app = QApplication(sys.argv)
app.setStyleSheet(style_sheet)
file_path = str(os.path.dirname(os.path.abspath(__file__))+'/')
h_expander = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
v_expander = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
change_page = QAction(None)

font_title_size = 180
font_subtitle_size = 70
font_normal_size = 26

def initIcon():
    global person_black, person_red, person_yellow, close_black, close_red, plus_yellow
    person_black = QIcon()
    person_red = QIcon()
    person_yellow = QIcon()
    close_black = QIcon()
    plus_yellow = QIcon()
    
    close_red = QIcon()
    person_black.addPixmap(QPixmap(file_path+"/images/person_black.png"))
    person_red.addPixmap(QPixmap(file_path+"/images/person_red.png"))
    person_yellow.addPixmap(QPixmap(file_path+"/images/person_yellow.png"))
    close_black.addPixmap(QPixmap(file_path+"/images/close_black.png"))
    close_red.addPixmap(QPixmap(file_path+"/images/close_red.png"))
    plus_yellow.addPixmap(QPixmap(file_path+"/images/plus_yellow.png"))

class BlackBar(QLabel):
    def __init__(self):  
        super().__init__()

    def paintEvent(self, event):
        super().paintEvent(event)
        self.rect = QRectF(0, self.height()/2-5, self.width(), 7)
        self.painter = QPainter(self)
        self.painter.setPen(QPen(Qt.black))
        self.painter.fillRect(self.rect, QBrush(Qt.black))
        self.painter.end()

class NameBtn(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Agency FB", font_normal_size))
        self.setIcon(person_black)
        self.setIconSize(QSize(32, 32))
        self.setMinimumWidth(350)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

class CloseBtn(QToolButton):
    def __init__(self):
        super().__init__()
        self.setIcon(close_black)
        self.setIconSize(QSize(32, 32))
        self.setMinimumWidth(65)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

class UserNameBtn(QHBoxLayout):
    def __init__(self, name = ""):
        super().__init__()
        self.name = name
        self.name_btn = NameBtn()
        self.name_btn.setText(" "+name)
        self.close_btn = CloseBtn()
        self.close_btn.clicked.connect(self.removeUser)
        self.close_btn.pressed.connect(self.closeBtnPressed)
        self.close_btn.released.connect(self.closeBtnReleased)
        self.name_btn.pressed.connect(self.nameBtnPressed)
        self.name_btn.released.connect(self.nameBtnReleased)
        self.name_btn.clicked.connect(self.selectUser)

        self.addWidget(self.name_btn)
        self.addWidget(self.close_btn)

    def __del__(self):
        self.removeUser()

    def removeUser(self):
        self.name_btn.setParent(None)
        self.close_btn.setParent(None)
        self.name_btn.deleteLater()
        self.close_btn.deleteLater()
        self.deleteLater()

    def closeBtnPressed(self):
        self.close_btn.setIcon(close_red)
    
    def closeBtnReleased(self):
        self.close_btn.setIcon(close_black)

    def nameBtnPressed(self):
        self.name_btn.setIcon(person_red)
    
    def nameBtnReleased(self):
        self.name_btn.setIcon(person_black)
    
    def selectUser(self):
        info_list = UserAPI.getUserInfo(self.name, var.id)
        print(info_list)
        var.user.setupUserInfo(info_list)
        if len(var.user_list) == 0 or self.name != var.user_list[0]:
            with open(file_path+'user_list', 'w') as f:
                var.user_list.insert(0, self.name)
                for ul in var.user_list:
                    f.write(ul+'\n')
                f.close()
        var.page.append("Menu")
        change_page.trigger()

class BlackBtn(QPushButton):
    def __init__(self, text = "", icon = ""):
        super().__init__()
        self.setText(text)
        self.setFont(QFont("Agency FB", font_normal_size))
        self.setIconSize(QSize(32, 32))
        if icon == "person_yellow":
            self.setIcon(person_yellow)
        elif icon == "plus_yellow":
            self.setIcon(plus_yellow)

class YellowBtn(QPushButton):
    def __init__(self, text = ""):
        super().__init__()
        self.setText(text)
        self.setFont(QFont("Agency FB", font_normal_size))

class CheckBtn(QPushButton):
    def __init__(self, text = ""):
        super().__init__()
        self.setText(text)
        self.setFont(QFont("Agency FB", font_normal_size))
        self.setCheckable(True)
        self.setMaximumHeight(65)
        self.setMinimumHeight(65)

class MenuItem():
    def __init__(self):
        self.name_lbl = QLabel()
        self.name_lbl.setAlignment(Qt.AlignCenter)
        self.name_lbl.setFont(QFont("Agency FB", font_normal_size))
        self.image_btn = QToolButton()
        self.image_btn.setStyleSheet("border-radius: 30px;")
        self.image_btn.setMaximumSize(160, 160)
        self.image_btn.pressed.connect(self.btnPressed)
        self.image_btn.released.connect(self.btnReleased)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_btn)
        self.layout.addWidget(self.name_lbl)
        self.layout.setSpacing(10)

    def setupImage(self, img_name):
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(file_path+"images/"+img_name+".png"))
        self.icon_red = QIcon()
        self.icon_red.addPixmap(QPixmap(file_path+"images/"+img_name+"_red.png"))
        self.image_btn.setIcon(self.icon)
        self.image_btn.setIconSize(QSize(160, 160))
    
    def setupName(self, name):
        self.name = name
        self.name_lbl.setText(name)
    
    def btnPressed(self):
        self.name_lbl.setStyleSheet("color: #C00000;")
        self.image_btn.setIcon(self.icon_red)

    def btnReleased(self):
        self.name_lbl.setStyleSheet("color: #000000;")
        self.image_btn.setIcon(self.icon)

class LineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
    def focusInEvent(self, event):
        super().focusInEvent(event)
        print('onboard')
    def focusOutEvent(self, event):
        super().focusOutEvent(event)

class WeightEditLine(LineEdit):
    def __init__(self, text = ""):
        super().__init__()
        self.setText(text)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setAlignment(Qt.AlignRight)
        self.setStyleSheet("border-color: #FFC000;")
        self.setValidator(QRegExpValidator(QRegExp("^(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*))$")))
        self.returnPressed.connect(self.finishEdit)
        self.setMaximumWidth(200)
        self.ready_to_edit = False
        self.focus_out = QAction(None)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setStyleSheet("border-color: #000000;")
        self.setText(self.text()[:-2])
        if not self.ready_to_edit:
            self.selectAll()
            self.ready_to_edit = True

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        text = self.text() if self.text() != "" else 0
        self.setText(str(float(text))+' g')
        self.finishEdit()
        self.focus_out.trigger()
    
    def finishEdit(self):
        self.setStyleSheet("border-color: #FFC000;")
        self.ready_to_edit = False
        self.clearFocus()

    def getWeight(self):
        text = self.text()[:-2]
        return float(text)

class Nutrition():
    def __init__(self, text = "", show_ratio = False):
        self.name_lbl = QLabel(text)
        self.name_lbl.setFont(QFont("Agency FB", font_normal_size))
        self.name_lbl.setMinimumHeight(55)
        self.num_lbl = QLabel()
        self.num_lbl.setFont(QFont("Agency FB", font_normal_size))
        self.show_ratio = show_ratio
        if self.show_ratio:
            self.num_lbl.setText("10 / 100")
        else:
            self.num_lbl.setText("10 g  ")
        self.value = 10

        h_expender = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.name_lbl)
        self.layout.addItem(h_expender)
        self.layout.addWidget(self.num_lbl)

    def setBaseWeight(self, weight):
        frac, denom = self.num_lbl.text().split(" / ")
        denom = str(weight)
        self.num_lbl.setText(str(frac+' / '+denom))

    def setWeight(self, weight):
        self.value = weight
        if self.show_ratio:
            frac, denom = self.num_lbl.text().split(" / ")
            frac = str(weight)
            self.num_lbl.setText(str(frac+' / '+denom))
            if float(frac) > float(denom):
                self.num_lbl.setStyleSheet("color:  #C00000;")
            else:
                self.num_lbl.setStyleSheet("color:  #000000;")
        else:
            self.num_lbl.setText(str(weight)+' g  ')

class ProgressCircle(QLabel):
    def __init__(self):
        super().__init__()
        self.length = 320
        self.ratio = 0
        self.text = '0 / 2000'
        self.path = QPainterPath()
        self.drawPath()

    def paintEvent(self, event):
        super().paintEvent(event)
        self.drawPath()
        self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        if self.ratio > 1:
            self.painter.setPen(QPen(QColor(192, 0, 0), 3))
            self.painter.fillPath(self.path, QColor(192, 0, 0))
        else:
            self.painter.setPen(QPen(Qt.black, 3))
            self.painter.fillPath(self.path, Qt.black)
        self.painter.drawEllipse(self.r1)
        self.painter.drawEllipse(self.r2)
        self.painter.setFont(QFont("Agency FB", font_normal_size+5))
        self.painter.drawText(QRectF(0, 0, self.width(), self.height()), Qt.AlignCenter, self.text)
        self.painter.end()
    
    def drawPath(self):
        self.r1 = QRectF(self.width()/2-self.length*0.5, self.height()/2-self.length*0.5, self.length, self.length)
        self.r2 = QRectF(self.width()/2-self.length*0.35, self.height()/2-self.length*0.35, self.length*0.7, self.length*0.7)
        self.ang = self.ratio * 360 if self.ratio < 1 else 360 
        self.path = QPainterPath()
        self.path.moveTo(QPointF(self.width()/2, self.height()/2-self.length*0.5))
        self.path.arcTo(self.r1, 90, -self.ang)
        self.path.arcTo(self.r2, 90-self.ang, self.ang)

    def setRatio(self, cal, TDEE):
        self.ratio = cal / TDEE
        self.text = str(int(cal)) + ' / ' + str(int(TDEE))

class CameraThread(QThread):
    frame_data_updated = pyqtSignal(ndarray)
    invalid_video_file = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def run(self):
        capture = cv2.VideoCapture(0)
        if not capture.isOpened():
            self.invalid_video_file.emit()
        else:
            while self.parent.thread_is_running:
                valid, frame = capture.read()
                if not valid:
                    break
                if var.page[-1] == "Scan Package":
                    frame, food_name = BarcodeAPI.detectBarcode(frame)
                    if food_name != None: 
                        print(food_name)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame_data_updated.emit(frame)
                time.sleep(0.03)

    def stopThread(self):
        """Process all pending events before stopping the thread."""
        self.wait()
        QApplication.processEvents()
