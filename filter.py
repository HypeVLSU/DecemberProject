from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

import mainFile

class FilterWindow(QMainWindow):
    def __init__(self):
        super(FilterWindow, self).__init__()
        
        self.newText = QtWidgets.QLabel(self)
        self.setGeometry(300, 100, 490, 500)
        
        self.setWindowTitle("Фильтры")
        self.setStyleSheet('background-color: #CD5C5C')
        
        btn1 = QtWidgets.QPushButton('Фильтр: г.Владимир', self)
        btn1.setToolTip('Фильтрация списка')
        btn1.resize(170, 50)  # размер кнопки
        btn1.move(50, 50)  # размещение
        btn1.clicked.connect(self.clickButton1)
        btn1.setStyleSheet("background-color: white;border-radius: 10px")

        btn2 = QtWidgets.QPushButton('Фильтр: не г.Владимир', self)
        btn2.setToolTip('Фильтрация списка')
        btn2.resize(170, 50)  # размер кнопки
        btn2.move(270, 50)  # размещение
        btn2.clicked.connect(self.clickButton2)
        btn2.setStyleSheet("background-color: white;border-radius: 10px")

        btn3 = QtWidgets.QPushButton('Фильтр: старше 18 лет', self)
        btn3.setToolTip('Фильтрация списка')
        btn3.resize(170, 50)  # размер кнопки
        btn3.move(50, 120)  # размещение
        btn3.clicked.connect(self.clickButton3)
        btn3.setStyleSheet("background-color: white;border-radius: 10px")

        btn4 = QtWidgets.QPushButton('Фильтр: младше 18 лет', self)
        btn4.setToolTip('Фильтрация списка')
        btn4.resize(170, 50)  # размер кнопки
        btn4.move(270, 120)  # размещение
        btn4.clicked.connect(self.clickButton4)
        btn4.setStyleSheet("background-color: white;border-radius: 10px")

        btn5 = QtWidgets.QPushButton('Фильтр: мужчины', self)
        btn5.setToolTip('Фильтрация списка')
        btn5.resize(170, 50)  # размер кнопки
        btn5.move(50, 190)  # размещение
        btn5.clicked.connect(self.clickButton5)
        btn5.setStyleSheet("background-color: white;border-radius: 10px")

        btn6 = QtWidgets.QPushButton('Фильтр: девушки', self)
        btn6.setToolTip('Фильтрация списка')
        btn6.resize(170, 50)  # размер кнопки
        btn6.move(270, 190)  # размещение
        btn6.clicked.connect(self.clickButton6)
        btn6.setStyleSheet("background-color: white;border-radius: 10px")
        
        btn14 = QtWidgets.QPushButton('Фильтр: открытые профили', self)
        btn14.setToolTip('Фильтрация списка')
        btn14.resize(170, 50)  # размер кнопки
        btn14.move(50, 260)  # размещение
        btn14.clicked.connect(self.clickButton14)
        btn14.setStyleSheet("background-color: white;border-radius: 10px")

        btn15 = QtWidgets.QPushButton('Фильтр: закрытые профили', self)
        btn15.setToolTip('Фильтрация списка')
        btn15.resize(170, 50)  # размер кнопки
        btn15.move(270, 260)  # размещение
        btn15.clicked.connect(self.clickButton15)
        btn15.setStyleSheet("background-color: white;border-radius: 10px")
        
        
    def clickButton1(self):
        self.newText.setText("Фильтр #1 выполнен!")
        self.newText.adjustSize()
        mainFile.selectVladimir()

    def clickButton2(self):
        self.newText.setText("Фильтр #2 выполнен!")
        self.newText.adjustSize()
        mainFile.selectNonVladimir()

    def clickButton3(self):
        self.newText.setText("Фильтр #3 выполнен!")
        self.newText.adjustSize()
        mainFile.selectMoreYears18()

    def clickButton4(self):
        self.newText.setText("Фильтр #4 выполнен!")
        self.newText.adjustSize()
        mainFile.selectLessYears18()

    def clickButton5(self):
        self.newText.setText("Фильтр #5 выполнен!")
        self.newText.adjustSize()
        mainFile.selectBoys()

    def clickButton6(self):
        self.newText.setText("Фильтр #6 выполнен!")
        self.newText.adjustSize()
        mainFile.selectGirls()    
        
        
    def clickButton14(self):
        self.newText.setText("Фильтр #7 выполнен!")
        self.newText.adjustSize()
        mainFile.selectOpenedToken()

    def clickButton15(self):
        self.newText.setText("Фильтр #8 выполнен!")
        self.newText.adjustSize()
        mainFile.selectClosedToken()    
        
        
def mainApp():
    app = QApplication(sys.argv)
    window = FilterWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    mainApp()          