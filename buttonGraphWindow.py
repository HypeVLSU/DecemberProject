from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from graphicWindow import GraphFrend,GraphDefault,StolbGraphic,Analitic


class Graph(QWidget):
    def __init__(self):
        super(Graph, self).__init__()
        self.setGeometry(300, 100, 300, 700)
        self.gS = StolbGraphic()        
        
        self.setWindowTitle("Анализ информации")
        self.setStyleSheet('background-color: #CD5C5C')
        
        self.btn7 = QtWidgets.QPushButton('Построить граф связей [1+]', self)
        self.btn7.setToolTip('Переход к <b>сбору инфорации</b>')
        self.btn7.resize(190, 100)  # размер кнопки
        self.btn7.move(50, 50)  # размещение
        self.btn7.clicked.connect(self.clickButton10)
        self.btn7.setStyleSheet("background-color: white;border-radius: 10px")

        self.btn8 = QtWidgets.QPushButton('Анализ графа\n(после построения)', self)
        self.btn8.setToolTip('Переход к <b>сбору инфорации</b>')
        self.btn8.resize(190, 100)  # размер кнопки
        self.btn8.move(50, 170)  # размещение
        self.btn8.clicked.connect(self.clickButton11)
        self.btn8.setStyleSheet("background-color: white;border-radius: 10px")

        self.btn9 = QtWidgets.QPushButton('Построить граф\nсвязей друзей[1]', self)
        self.btn9.setToolTip('Переход к <b>сбору инфорации</b>')
        self.btn9.resize(190, 100)  # размер кнопки
        self.btn9.move(50, 290)  # размещение
        self.btn9.clicked.connect(self.clickButton13)
        self.btn9.setStyleSheet("background-color: white;border-radius: 10px")
        
        self.btn9 = QtWidgets.QPushButton('Столбчатая диаграмма', self)
        self.btn9.setToolTip('Переход к <b>сбору инфорации</b>')
        self.btn9.resize(190, 100)  # размер кнопки
        self.btn9.move(50, 410)  # размещение
        self.btn9.clicked.connect(self.clickButton14)
        self.btn9.setStyleSheet("background-color: white;border-radius: 10px")
        
        self.btn10 = QtWidgets.QPushButton('Круговая диаграмма', self)
        self.btn10.setToolTip('Переход к <b>сбору инфорации</b>')
        self.btn10.resize(190, 100)  # размер кнопки
        self.btn10.move(50, 530)  # размещение
        self.btn10.clicked.connect(self.clickButton15)
        self.btn10.setStyleSheet("background-color: white;border-radius: 10px")
        
        
        
    def clickButton10(self):
        self.gr = GraphDefault()
        self.gr.show()
        
    def clickButton11(self):
        self.a = Analitic()
        self.a.show()

    def clickButton13(self):
        self.g = GraphFrend()
        self.g.show()
        
    def clickButton14(self):
        self.gS.Stolb()
    
    def clickButton15(self):
        self.gS.Ciricle_18()
        self.gS.Ciricle_Open()
        self.gS.Ciricle_Man()
        self.gS.Ciricle_Sity()
        
         
