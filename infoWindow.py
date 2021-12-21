from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import glob
import mainFile

class InfoWindow(QWidget):
    def __init__(self):
        super(InfoWindow, self).__init__()
        
        self.label = QtWidgets.QTextEdit(self)
        self.label.move(270,10)
        self.label.resize(900,550)
        self.newText = QtWidgets.QLabel(self)
        self.setGeometry(300, 100, 1200, 600)
        
        self.setWindowTitle("Сбор информации")
        self.setStyleSheet('background-color: #CD5C5C')
        
        
        btn7 = QtWidgets.QPushButton('Собрать информацию о\nпользователях (в БД) [1+]', self)
        btn7.setToolTip('Переход к <b>сбору инфорации</b>')
        btn7.resize(190, 100)  # размер кнопки
        btn7.move(50, 50)  # размещение
        btn7.clicked.connect(self.clickButton7)
        btn7.setStyleSheet("background-color: white;border-radius: 10px")

        btn8 = QtWidgets.QPushButton('Собрать информацию о\nпользователях (в .txt) [1+]', self)
        btn8.setToolTip('Переход к <b>сбору инфорации</b>')
        btn8.resize(190, 100)  # размер кнопки
        btn8.move(50, 170)  # размещение
        btn8.clicked.connect(self.clickButton8)
        btn8.setStyleSheet("background-color: white;border-radius: 10px")

        btn9 = QtWidgets.QPushButton('Собрать сообщения\nпользователей (со стены) [1+]', self)
        btn9.setToolTip('Переход к <b>сбору инфорации</b>')
        btn9.resize(190, 100)  # размер кнопки
        btn9.move(50, 290)  # размещение
        btn9.clicked.connect(self.clickButton9)
        btn9.setStyleSheet("background-color: white;border-radius: 10px")

        btn12 = QtWidgets.QPushButton('Собрать информацию о\nдрузьях (в БД) [1]', self)
        btn12.setToolTip('Переход к <b>сбору инфорации</b>')
        btn12.resize(190, 100)  # размер кнопки
        btn12.move(50, 410)  # размещение
        btn12.clicked.connect(self.clickButton12)
        btn12.setStyleSheet("background-color: white;border-radius: 10px")
        
    def clickButton7(self):
        self.newText.setText("Сбор информации в БД сделан!")
        self.newText.adjustSize()
        info = mainFile.collectionInformationBD()
        s = ''
        i = ['id: '+ str(info[0]),'Имя пользователя: ' + str(info[1]),'Фамилия пользователя: ' + str(info[2]),'Тип аккаунта: ' + str(info[3]),'Дата рождения: ' + str(info[4]),'Университет: ' + str(info[5]),'Инстаграм: ' + str(info[6]),'Страна: ' + str(info[7]),'Город: ' + str(info[8]),'Количество друзей: ' + str(info[9]),'Kоличество подписчиков: ' + str(info[10]),'Количество подписок: ' + str(info[11]),'Статус: '  + str(info[12])]
        for a in i:
            s = s + str(a) + '\n'
        self.label.setPlainText(s)
    
    def clickButton8(self):
        self.newText.setText("Сбор информации в TXT сделан!")
        self.newText.adjustSize()
        info = mainFile.collectionInformationTXT()
        filename = glob.glob('Information/*.txt')
        f = open(filename[0])
        self.label.setPlainText(str(info) + '\n\n' + f.read())
        
        
    def clickButton9(self):
        self.newText.setText("Сбор информации со стены сделан!")
        self.newText.adjustSize()
        info = mainFile.collectionMessageWall()
        filename = glob.glob('Information/*.txt')
        f = open(filename[0])
        self.label.setPlainText(str(info) + '\n\n' + f.read())
        
    def clickButton12(self):
        self.newText.setText("Информация о друзьях")
        self.newText.adjustSize()
        info = mainFile.collectionInformationFriendDB()
        s = ''
        for a in info:
            s = s + str(a) + '\n'
            
        self.label.setPlainText(s) 
