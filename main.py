from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from filter import FilterWindow
from infoWindow import InfoWindow
from buttonGraphWindow import Graph

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        
        self.newText = QtWidgets.QLabel(self)
        self.setGeometry(300, 100, 1000, 500)
        
        btn1 = QtWidgets.QPushButton('Сбор данных', self)
        btn1.resize(165, 50)  # размер кнопки
        btn1.move(410, 75)  # размещение
        btn1.clicked.connect(self.clickButton1)
        btn1.setStyleSheet("background-color: #FFC0CB;border-radius: 10px")
        
        
        btn2 = QtWidgets.QPushButton('Обработка данных', self)
        btn2.resize(165, 50)  # размер кнопки
        btn2.move(410, 135)  # размещение
        btn2.clicked.connect(self.clickButton2)
        btn2.setStyleSheet("background-color: #FFC0CB;border-radius: 10px")
        
        btn3 = QtWidgets.QPushButton('Фильтр', self)
        btn3.resize(165, 50)  # размер кнопки
        btn3.move(410, 195)  # размещение
        btn3.clicked.connect(self.clickButton3)
        btn3.setStyleSheet("background-color: #FFC0CB;border-radius: 10px")
        
        btn4 = QtWidgets.QPushButton('Выход', self)
        btn4.resize(165, 50)  # размер кнопки
        btn4.move(410, 255)  # размещение
        btn4.clicked.connect(QCoreApplication.instance().quit)
        btn4.setStyleSheet("background-color: #FFC0CB;border-radius: 10px")
        
        self.lbl = QtWidgets.QLabel(self)
        self.pix = QtGui.QPixmap("pic.jpg")
        self.lbl.setPixmap(self.pix)
        self.lbl.resize(400, 200)
        self.lbl.move(350, 335)
        self.show()
        
        self.setWindowTitle("Комплекс сбора и анализа информации")
        self.setStyleSheet('background-color: #CD5C5C')

    
    def clickButton1(self):
        self.Info = InfoWindow()    
        self.Info.show()
        
    def clickButton2(self):
        self.graph = Graph()
        self.graph.show()    
        
    def clickButton3(self):
        self.filter = FilterWindow()
        self.filter.show()



        

def mainApplication():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()


if __name__ == '__main__':
    mainApplication()  
    