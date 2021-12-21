from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap

import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import mainFile

class GraphFrend(QWidget):
    def __init__(self):
        super(GraphFrend, self).__init__()
        self.setGeometry(300, 100, 1200, 600)
        self.container = QtWidgets.QVBoxLayout(self)
        self.fig = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        self.container.addWidget(self.canvas)
        
        g = mainFile.createGraphFriends()
        
        nx.draw(g)
        self.fig = plt.figure(1, figsize=(3, 3))
        self.canvas.draw()

class GraphDefault(QWidget):
    def __init__(self):
        super(GraphDefault, self).__init__()
        self.setGeometry(300, 100, 1200, 600)
        self.container = QtWidgets.QVBoxLayout(self)
        self.fig = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        self.container.addWidget(self.canvas)
        
        g = mainFile.createGraph()
        
        nx.draw(g)
        self.fig = plt.figure(1, figsize=(3, 3))
        self.canvas.draw()
        
class Analitic(QWidget):
    def __init__(self):
        super(Analitic, self).__init__()
        self.setGeometry(300, 100, 1200, 600)
        
        self.setWindowTitle("Анализ графа")
        self.setStyleSheet('background-color: #CD5C5C')
        
        
        self.label = QTextEdit()
        self.label.move(500,10)
        self.label.resize(1000,500)
        layout = QVBoxLayout()
        
        layout.addWidget(self.label)
        self.setLayout(layout)        
        
        mainFile.informationGraph()
        filename = 'Information/informationAboutGraph.txt'
        f = open(filename)
        self.label.setPlainText(f.read())

class StolbGraphic():
    def Stolb(self):
        data_names = ['до 18', 'от 19 до 30', 'от 30 до 60', '60 и выше']
        data_values = [100, 90, 80, 10]

        dpi = 80
        self.fig = plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
        mpl.rcParams.update({'font.size': 10})

        ax = plt.axes()
        ax.yaxis.grid(True, zorder = 1)

        xs = range(len(data_names))

        plt.bar([x + 0.05 for x in xs], [ d * 0.9 for d in data_values],
                width = 0.2, color = 'red', alpha = 0.7, label = '2016',
                zorder = 2)
        plt.xticks(xs, data_names)

        self.fig.autofmt_xdate(rotation = 25)

        self.fig.show()    
    
    
    def Ciricle_18(self):
        data_names = ['Меньше 18 или 18', 'Больше 18']
        data_values = [50, 50]

        dpi = 80
        self.fig = plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
        mpl.rcParams.update({'font.size': 9})

        xs = range(len(data_names))

        plt.pie(
            data_values, autopct='%.1f', radius = 1.1,
            explode = [0.15] + [0 for _ in range(len(data_names) - 1)] )
        plt.legend(
            bbox_to_anchor = (-0.16, 0.45, 0.25, 0.25),
            loc = 'lower left', labels = data_names )
        
        self.fig.show()
        
        
    def Ciricle_Open(self):
        data_names = ['Открыт', 'Закрыт']
        data_values = [50, 50]

        dpi = 80
        self.fig = plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
        mpl.rcParams.update({'font.size': 9})

        xs = range(len(data_names))

        plt.pie(
            data_values, autopct='%.1f', radius = 1.1,
            explode = [0.15] + [0 for _ in range(len(data_names) - 1)] )
        plt.legend(
            bbox_to_anchor = (-0.16, 0.45, 0.25, 0.25),
            loc = 'lower left', labels = data_names )
        
        self.fig.show()    
        
    def Ciricle_Man(self):
        data_names = ['Муж', 'Жен']
        data_values = [50, 50]

        dpi = 80
        self.fig = plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
        mpl.rcParams.update({'font.size': 9})

        xs = range(len(data_names))

        plt.pie(
            data_values, autopct='%.1f', radius = 1.1,
            explode = [0.15] + [0 for _ in range(len(data_names) - 1)] )
        plt.legend(
            bbox_to_anchor = (-0.16, 0.45, 0.25, 0.25),
            loc = 'lower left', labels = data_names )
        
        self.fig.show()    
        
    def Ciricle_Sity(self):
        data_names = ['Владимир', 'Не Владимир']
        data_values = [50, 50]

        dpi = 80
        self.fig = plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
        mpl.rcParams.update({'font.size': 9})

        xs = range(len(data_names))

        plt.pie(
            data_values, autopct='%.1f', radius = 1.1,
            explode = [0.15] + [0 for _ in range(len(data_names) - 1)] )
        plt.legend(
            bbox_to_anchor = (-0.16, 0.45, 0.25, 0.25),
            loc = 'lower left', labels = data_names )
        
        self.fig.show()    
        