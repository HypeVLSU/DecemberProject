import vk_api
import networkx as nx
import time
import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))#Масштаб подсказок

        btn = QPushButton('Подсистема сбора инфорации', self)
        btn.setToolTip('Переход к <b>сбору инфорации</b>')
        btn.resize(300, 50)#размер кнопки
        btn.move(200, 100)#размещение

        btn1 = QPushButton('Подсистема анализа инфорации', self)
        btn1.setToolTip('Переход к <b>анализу инфорации</b>')
        btn1.resize(300, 50)#размер кнопки
        btn1.move(700, 100)#размещение

        qbtn = QPushButton('Выход', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(100, 50)#размер кнопки
        qbtn.move(550, 200)#размещение

        self.setGeometry(100, 150, 1200, 500)
        self.setWindowTitle('Программный комплекс')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

def main():
    login, password = '79048595323', 'ffff431518'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    start = time.time()
    vk = vk_session.get_api()
    g = nx.Graph(directed=False)
    listUsers = []
    print("+")

    lines = [line.rstrip('\n') for line in open('ids.txt')]
    for i in range(len(lines)):
        temp = lines[i]
        temp = str(temp)
        listUsers.append(temp)

    for i in range(len(listUsers)):
        count = 0
        listFriend = []
        commonFriends = []
        user_friend = vk.friends.get(user_id=(listUsers[i]), fields=('domain'))
        countFriend = user_friend['count']

        for j in range(countFriend):
            listFriend.append(str(user_friend['items'][j]['id']))

        for k in listUsers:
            for l in listFriend:
                if k == l:
                    commonFriends.append(k)
                    break
        count = len((commonFriends))

        node = listUsers[i]
        g.add_node(node)
        print('User -', node)
        for j in range(len(commonFriends)):
            if (listUsers[i] != commonFriends[j]):
                g.add_edge(listUsers[i], commonFriends[j])

    print('Время выполнения', round((time.time() - start), 2), 'секунд')
    nx.write_graphml(g, "Information/test.graphml")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

