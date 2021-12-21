import vk_api
import networkx as nx
import pandas as pd
import time
import os.path
import sqlite3
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from itertools import groupby
from datetime import datetime

login, password = '79048595323', 'fffff431518'
visited = []


def createDB():
    conn = sqlite3.connect("Information/database.db")  # или :memory: чтобы сохранить в RAM
    cur = conn.cursor()

    # Создание таблицы
    cur.execute("""CREATE TABLE information
                      (id integer, first_name text, last_name text, typeaccount text, bdate text, 
                      university_name text, instagram text, country text, city text, user_friend integer,
                      subscribers integer, subscriptions integer, status_get text)
                   """)

def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device

def two_factor():
    code = input('Code? ')
    return code

def collectionInformationBD():
    vk_session = vk_api.VkApi(login=login,
                              password=password,
                              auth_handler=auth_handler)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    file_path = "Information/database.db"
    check = os.path.exists(file_path)
    if check == False:
        createDB()
    conn = sqlite3.connect("Information/database.db")
    cur = conn.cursor()
    cur.execute('DELETE FROM information;', )
    openTokens = 0
    closedTokens = 0
    # ---------------------------------------------------------
    info = []
    start = time.time()
    lines = [line.rstrip('\n') for line in open('ids.txt')]
    mes = 'Выполняется сбор информации в БД. Компонентов: ' + str(len(lines))
    logInfo(mes, 'collection')
    for i in range(len(lines)):
        arrayInformation = []
        vk = vk_session.get_api()

        # Имя, фамилия пользователя, тип аккаунта, день рождения, город и страна
        try:
            input_id = lines[i]
            user_get = vk.users.get(user_ids=(input_id), fields=("bdate,city,country,education,connections,domain"))
            user_get = user_get[0]
            first_name = user_get['first_name']
            arrayInformation.append(first_name)
            last_name = user_get['last_name']
            arrayInformation.append(last_name)
            islosed = user_get['is_closed']
            if (islosed):
                statusType = 'closed'
            else:
                statusType = 'opened'
            arrayInformation.append(statusType)
            import datetime

            try:
                bdate = user_get['bdate']
                td = datetime.datetime.now().date()
                array_bd = bdate.split('.')
                bd = datetime.date(int(array_bd[2]), int(array_bd[1]), int(array_bd[0]))
                date = str(array_bd[0]) + '.' + str(array_bd[1]) + '.' + str(array_bd[2])
                arrayInformation.append(date)
            except:
                temp = 'none'
                arrayInformation.append(temp)

            try:
                universityName = user_get['university_name']
                arrayInformation.append(universityName)
            except:
                temp = 'none'
                arrayInformation.append(temp)

            try:
                instagram = user_get['instagram']
                arrayInformation.append(instagram)
            except:
                temp = 'none'
                arrayInformation.append(temp)

            try:
                country = user_get['country']['title']
                arrayInformation.append(country)
            except:
                temp = 'none'
                arrayInformation.append(temp)
            try:
                city = user_get['city']['title']
                arrayInformation.append(city)
            except:
                temp = 'none'
                arrayInformation.append(temp)

            # Количество друзей
            user_friend = vk.friends.get(user_id=(input_id))
            countFriend = user_friend['count']
            arrayInformation.append(countFriend)

            # Количество подписчиков и подписок
            user_getFollowers = vk.users.getFollowers(user_id=(input_id))
            subscribers = user_getFollowers['count']
            user_getSubscriptions = vk.users.getSubscriptions(user_id=(input_id), extended=1)
            subscriptions = user_getSubscriptions['count']
            arrayInformation.append(subscribers)
            arrayInformation.append(subscriptions)

            # Статус пользователя
            status_get = vk.status.get(user_id=(input_id))
            statusOfUser = status_get['text']
            if (statusOfUser == ''):
                temp = 'none'
                arrayInformation.append(temp)
            else:
                try:
                    arrayInformation.append(statusOfUser)
                except:
                    temp = 'unknown symbols'
                    arrayInformation.append(temp)

            info = [input_id, arrayInformation[0], arrayInformation[1], arrayInformation[2], arrayInformation[3],
                     arrayInformation[4], arrayInformation[5], arrayInformation[6], arrayInformation[7],
                     arrayInformation[8], arrayInformation[9], arrayInformation[10], arrayInformation[11]]

            cur.executemany("INSERT INTO information VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", info)
            conn.commit()

            openTokens += 1
            print("{}) Профиль {} просмотрен. Открытый".format(i + 1, lines[i]))
        except:
            closedTokens += 1
            print("{}) Профиль {} просмотрен. Закрытый".format(i + 1, lines[i]))

    print('Итого:', openTokens, "открытых,", closedTokens, 'закрытых')

    tt = round((time.time() - start), 2)
    mes = 'Время выполнения задачи ' + str(tt) + ' секунд'
    logInfo(mes, 'collection')
    return (info)

def collectionInformationTXT():
    vk_session = vk_api.VkApi(login=login,
                              password=password,
                              auth_handler=auth_handler)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    directory = "Information"
    openTokens = 0
    closedTokens = 0
    start = time.time()
    lines = [line.rstrip('\n') for line in open('ids.txt')]
    mes = 'Выполняется сбор информации в .txt. Компонентов: ' + str(len(lines))
    logInfo(mes, 'collection')
    for i in range(len(lines)):
        vk = vk_session.get_api()

        # Имя, фамилия пользователя, тип аккаунта, день рождения, город и страна
        try:
            nameFile = directory + '/' + lines[i] + ".txt"
            f = open(nameFile, "w")
            input_id = lines[i]
            user_get = vk.users.get(user_ids=(input_id), fields=("bdate,city,country,education,connections,domain"))
            user_get = user_get[0]
            first_name = user_get['first_name']
            f.write('1. Имя пользователя: '+ first_name +'\n')
            last_name = user_get['last_name']
            f.write('2. Фамилия пользователя: '+ last_name +'\n')
            islosed = user_get['is_closed']
            if (islosed):
                f.write('3. Аккаунт закрытый' +'\n')
            else:
                f.write('3. Аккаунт открытый' +'\n')
            import datetime

            try:
                bdate = user_get['bdate']
                td = datetime.datetime.now().date()
                array_bd = bdate.split('.')
                bd = datetime.date(int(array_bd[2]), int(array_bd[1]), int(array_bd[0]))
                date = str(array_bd[0]) + '.' + str(array_bd[1]) + '.' + str(array_bd[2])
                age_years = int((td - bd).days / 365.25)
                f.write('4. День рождения: {}. Полных лет: {} \n'.format(date,age_years))
            except:
                f.write('4. День рождения указан не полностью \n')

            try:
                universityName = user_get['university_name']
                f.write("5. Университет: " + universityName + '\n')
            except:
                f.write("5. Университет не указан \n")

            try:
                instagram = user_get['instagram']
                f.write("6. Инстаграм: " + instagram + '\n')
            except:
                f.write("6. Инстаграм не указан \n")

            try:
                country = user_get['country']['title']
                f.write('7. Страна пользователя: ' + country + '\n')
            except:
                f.write('7. Страна пользователя не указана\n')
            try:
                city = user_get['city']['title']
                f.write('8. Город пользователя: ' + city + '\n')
            except:
                f.write('8. Город пользователя не указан\n')

            # Количество друзей
            user_friend = vk.friends.get(user_id=(input_id))
            countFriend = user_friend['count']
            f.write('9. Количество друзей : '+ str(countFriend) + '\n')

            # Количество подписчиков и подписок
            user_getFollowers = vk.users.getFollowers(user_id=(input_id))
            subscribers = user_getFollowers['count']
            user_getSubscriptions = vk.users.getSubscriptions(user_id=(input_id), extended=1)
            subscriptions = user_getSubscriptions['count']
            f.write('10. Количество подписчиков: '+ str(subscribers) + '\n')
            f.write('11. Количество подписок: '+ str(subscriptions) + '\n')

            # Статус пользователя
            status_get = vk.status.get(user_id=(input_id))
            statusOfUser = status_get['text']
            if (statusOfUser == ''):
                f.write('12. У пользователя не установлен статуса\n')
            else:
                try:
                    f.write('12. У пользователя статус: {} \n'.format(statusOfUser))
                except:
                    f.write('12. В статусе присутствуют символы \n')

            openTokens += 1
            print("{}) Профиль {} просмотрен. Открытый".format(i + 1, lines[i]))
        except:
            closedTokens += 1
            print("{}) Профиль {} просмотрен. Закрытый".format(i + 1, lines[i]))

    print('Итого:', openTokens, "открытых,", closedTokens, 'закрытых')

    tt = round((time.time() - start), 2)
    mes = 'Время выполнения задачи ' + str(tt) + ' секунд'
    logInfo(mes, 'collection')
    return('Итого:', openTokens, "открытых,", closedTokens, 'закрытых')

def collectionMessageWall():
    vk_session = vk_api.VkApi(login=login,
                              password=password,
                              auth_handler=auth_handler)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    directory = "Information"
    openTokens = 0
    closedTokens = 0
    tools = vk_api.VkTools(vk_session)
    start = time.time()
    lines = [line.rstrip('\n') for line in open('ids.txt')]
    mes = 'Выполняется сбор информации со стены. Компонентов: ' + str(len(lines))
    logInfo(mes, 'collection')
    for k in range(len(lines)):
        # Имя, фамилия пользователя, тип аккаунта, день рождения, город и страна
        try:
            nameFile = directory + '/' + lines[k] + ".txt"
            f = open(nameFile, "w")
            input_id = lines[k]
            countPosts = 0
            countReposts = 0
            countLikes = 0
            countComments = 0

            # Анализ стены
            f.write("Анализ стены пользователя: " + '\n')
            from datetime import datetime
            wall = tools.get_all('wall.get', 100, {'owner_id': input_id})
            for i in range(wall['count']):
                One = wall['items'][i]['from_id']
                Two = wall['items'][i]['owner_id']
                DateCount = wall['items'][i]['date']
                Date = (datetime.fromtimestamp(DateCount))
                Likes = wall['items'][i]["likes"]["count"]
                countLikes += Likes
                Comments = wall['items'][i]['comments']['count']
                countComments += Comments
                if (One == Two):
                    f.write('Запись №{} является постом. {} лайк(-ов). {} комментариев. Дата {}\n'.format(i + 1, Likes,
                                                                                                          Comments,
                                                                                                          Date))
                    countPosts += 1
                else:
                    f.write(
                        'Запись №{} является репостом или чужой записью. {} лайков. {} комментариев. Дата {}\n'.format(
                            i + 1, Likes, Comments, Date))
                    countReposts += 1
            f.write("Общая информация:\n")
            rep = countPosts + countReposts
            f.write("Количество записей: " + str(rep) + '\n')
            f.write("Количество постов: " + str(countPosts) + '\n')
            f.write("Количество репостов: " + str(countReposts) + '\n')
            f.write("Количество лайков: " + str(countLikes) + '\n')
            f.write("Количество комментов: " + str(countComments) + '\n')

            openTokens += 1
            print("{}) Профиль {} просмотрен. Открытый".format(k + 1, input_id))
        except:
            closedTokens += 1
            print("{}) Профиль {} просмотрен. Закрытый".format(k + 1, input_id))
            f.write("Профиль закрыт" + '\n')

    print('Итого:', openTokens, "открытых,", closedTokens, 'закрытых')

    tt = round((time.time() - start), 2)
    mes = 'Время выполнения задачи ' + str(tt) + ' секунд'
    logInfo(mes, 'collection')
    return('Итого:', openTokens, "открытых,", closedTokens, 'закрытых')

def collectionInformationFriendDB():
    vk_session = vk_api.VkApi(login, password)
    vk = vk_session.get_api()

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    listUsers = []
    openTokens = 0
    closedTokens = 0
    lines = [line.rstrip('\n') for line in open('ids.txt')]
    user_friend = vk.friends.get(user_id=(lines[0]), fields=('domain'))
    countFriend = user_friend['count']
    for j in range(countFriend):
        listUsers.append(str(user_friend['items'][j]['id']))
    mes = 'Выполняется сбор информации о друзьях пользователя. Компонентов: ' + str(len(listUsers))
    logInfo(mes, 'collection')

    file_path = "Information/database.db"
    check = os.path.exists(file_path)
    if check == False:
        createDB()
    conn = sqlite3.connect("Information/database.db")
    cur = conn.cursor()
    cur.execute('DELETE FROM information;', )
    # ---------------------------------------------------------
    info = []
    start = time.time()
    for i in range(len(listUsers)):
        arrayInformation = []
        vk = vk_session.get_api()

        # Имя, фамилия пользователя, тип аккаунта, день рождения, город и страна
        try:
            input_id = listUsers[i]
            user_get = vk.users.get(user_ids=(input_id), fields=("bdate,city,country,education,connections,domain"))
            user_get = user_get[0]
            first_name = user_get['first_name']
            arrayInformation.append(first_name)
            last_name = user_get['last_name']
            arrayInformation.append(last_name)
            islosed = user_get['is_closed']
            if (islosed):
                statusType = 'closed'
            else:
                statusType = 'opened'
            arrayInformation.append(statusType)
            import datetime

            try:
                bdate = user_get['bdate']
                td = datetime.datetime.now().date()
                array_bd = bdate.split('.')
                bd = datetime.date(int(array_bd[2]), int(array_bd[1]), int(array_bd[0]))
                date = str(array_bd[0]) + '.' + str(array_bd[1]) + '.' + str(array_bd[2])
                arrayInformation.append(date)
            except:
                temp = 'none'
                arrayInformation.append(temp)
            try:
                universityName = user_get['university_name']
                arrayInformation.append(universityName)
            except:
                temp = 'none'
                arrayInformation.append(temp)

            try:
                instagram = user_get['instagram']
                arrayInformation.append(instagram)
            except:
                temp = 'none'
                arrayInformation.append(temp)

            try:
                country = user_get['country']['title']
                arrayInformation.append(country)
            except:
                temp = 'none'
                arrayInformation.append(temp)
            try:
                city = user_get['city']['title']
                arrayInformation.append(city)
            except:
                temp = 'none'
                arrayInformation.append(temp)

            # Количество друзей
            user_friend = vk.friends.get(user_id=(input_id))
            countFriend = user_friend['count']
            arrayInformation.append(countFriend)

            # Количество подписчиков и подписок
            user_getFollowers = vk.users.getFollowers(user_id=(input_id))
            subscribers = user_getFollowers['count']
            user_getSubscriptions = vk.users.getSubscriptions(user_id=(input_id), extended=1)
            subscriptions = user_getSubscriptions['count']
            arrayInformation.append(subscribers)
            arrayInformation.append(subscriptions)

            # Статус пользователя
            status_get = vk.status.get(user_id=(input_id))
            statusOfUser = status_get['text']
            if (statusOfUser == ''):
                temp = 'none'
                arrayInformation.append(temp)
            else:
                try:
                    arrayInformation.append(statusOfUser)
                except:
                    temp = 'unknown symbols'
                    arrayInformation.append(temp)

            info += [[input_id, arrayInformation[0], arrayInformation[1], arrayInformation[2], arrayInformation[3],
                     arrayInformation[4], arrayInformation[5], arrayInformation[6], arrayInformation[7],
                     arrayInformation[8], arrayInformation[9], arrayInformation[10], arrayInformation[11]]]

            cur.executemany("INSERT INTO information VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", info)
            conn.commit()

            openTokens += 1
            print("{}) Профиль {} просмотрен. Открытый".format(i + 1, input_id))
        except:
            closedTokens += 1
            print("{}) Профиль {} просмотрен. Закрытый".format(i + 1, input_id))
    print('Итого:', openTokens,"открытых,", closedTokens,'закрытых')

    tt = round((time.time() - start), 2)
    mes = 'Время выполнения задачи ' + str(tt) + ' секунд'
    logInfo(mes, 'collection')
    return(info)

def createGraph():
    vk_session = vk_api.VkApi(login, password)
    vk = vk_session.get_api()

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    g = nx.Graph(directed=False)
    listUsers = []
    start = time.time()

    lines = [line.rstrip('\n') for line in open('ids.txt')]
    mes = 'Выполняется построение графа связей. Компонентов: ' + str(len(lines))
    logInfo(mes, 'analysis')
    for i in range(len(lines)):
        temp = lines[i]
        temp = str(temp)
        listUsers.append(temp)

    f = open("Information/listEdges.txt", "w")
    f.close()
    f = open("Information/listEdges.txt", "r+")
    for i in range(len(listUsers)):
        try:
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

            node = listUsers[i]
            g.add_node(node)
            print("{}) Профиль {} просмотрен. Открытый".format(i + 1, node))

            for j in range(len(commonFriends)):
                if (listUsers[i] != commonFriends[j]):
                    g.add_edge(listUsers[i], commonFriends[j])
                    f.write(str(listUsers[i]) + " " + str(commonFriends[j] + "\n"))
                    f.write(str(commonFriends[j]) + " " + str(listUsers[i] + "\n"))
        except:
            print("{}) Профиль {} просмотрен. Закрытый".format(i + 1, node))


    nx.write_graphml(g, "Information/graphRelationships.graphml")
    f.close()
    file = "Information/listEdges.txt"
    uniqlines = set(open(file, 'r', encoding='utf-8').readlines())
    gotovo = open(file, 'w', encoding='utf-8').writelines(set(uniqlines))

    tt = round((time.time() - start), 2)
    mes = 'Время выполнения задачи ' + str(tt) + ' секунд'
    logInfo(mes, 'analysis')
    return(g)
    
def informationGraph():
    G = nx.read_edgelist('Information/listEdges.txt', create_using=nx.DiGraph())
    start = time.time()
    ig = open("Information/informationAboutGraph.txt", "w")
    ig.close()
    ig = open("Information/informationAboutGraph.txt", "r+")
    mes = 'Выполняется анализ графа связей'
    logInfo(mes, 'analysis')
    # Импорт данных и преобразование их в граф
    ig.write("1. Импорт данных и преобразование их в граф.\n")
    ig.write('\t' + 'Количество вершин: {}'.format(G.number_of_nodes()) + "\n")
    ig.write('\t' + 'Количество рёбер: {}'.format(G. number_of_edges()) + str("\n"))
    ig.write('\t' + 'Среднее количество соседей у узлов в графе: {}'.format(round(G.number_of_edges() / float(G.number_of_nodes()), 4)) + str("\n"))

    # Основные характеристики графов
    ig.write("2. Основные характеристики графов.\n")
    if nx.is_directed(G):
        if nx.is_weakly_connected(G):
                ig.write('\t' + 'Граф является направленным и состоит из одной компоненты слабой связности\n')
                check = False
        else:
                ig.write('\t' + 'Граф является направленным и состоит из нескольких компонент\n')
                check = True
    else:
        if nx.is_connected(G):
            print('\t' + 'Граф является ненаправленным и связным\n')
            check = False
        else:
            print('\t' + 'Граф является ненаправленным и состоит из нескольких компонент\n')
            check = True


    G_weak = G.subgraph(max(nx.weakly_connected_components(G), key=len))
    G_strong = G.subgraph(max(nx.strongly_connected_components(G), key=len))

    if check:
        ig.write('\t' + 'Количество вершин: {}'.format(G_weak.number_of_nodes()) + str("\n"))
        ig.write('\t' + 'Количество рёбер: {}'.format(G_weak.number_of_edges()) + str("\n"))
        ig.write('\t' + 'Среднее количество соседей у узла в графе: {}'.format(
            round(G_weak.number_of_edges() / float(G_weak.number_of_nodes()), 4)) + str("\n"))

        ig.write('\t' + 'Количество вершин: {}'.format(G_strong.number_of_nodes()) + str("\n"))
        ig.write('\t' + 'Количество рёбер: {}'.format(G_strong.number_of_edges()) + str("\n"))
        ig.write('\t' + 'Среднее количество соседей у узла в графе: {}'.format(round(G_strong.number_of_edges() / float(G_strong.number_of_nodes()), 4)) + str("\n"))

    # Путь, диаметр и среднее расстояние в графе
    ig.write("3. Путь, диаметр и среднее расстояние в графе.\n")
    ig.write('\t' + 'Диаметр: ' + str(nx.diameter(G_strong)) + "\n")
    if check:
        ig.write('\t' + 'Среднее расстояние в компоненте сильной связности: ' + str(round(nx.average_shortest_path_length(G_strong), 4)) + "\n")
    ig.write('\t' + 'Среднее расстояние в компоненте слабой связности: ' + str(round(nx.average_shortest_path_length(G_weak), 4)) + "\n")

    # Кластеризация и выделение сообществ
    ig.write("4. Кластеризация и выделение сообществ.\n")
    ig.write('\t' + 'Кластеризация слабой связности: ' + str(round(nx.transitivity(G_weak), 4)) + "\n")
    if check:
        ig.write('\t' + 'Кластеризация сильной связности: ' + str(round(nx.transitivity(G_strong), 4)) + "\n")
        ig.write('\t' + 'Кластерный коэффициент сильной связности: ' + str(round(nx.average_clustering(G_strong), 4)) + "\n")
        ig.write('\t' + 'Количество центральных узлов сильной связности: ' + str(len(nx.center(G_strong))) + "\n")
        ig.write('\t' + 'Количество узлов на периферии сильной связности: ' + str(len(nx.periphery(G_strong))) + "\n")

    # Взаимность связей
    ig.write("5. Взаимность связей.\n")
    ig.write('\t' + 'Уровень взаимности графа: ' + str(round(nx.overall_reciprocity(G),4 )) + "\n")
    ig.write('\t' + 'Уровень взаимности компоненты слабой связности: ' + str(round(nx.overall_reciprocity(G_weak),4 )) + "\n")
    if check:
        ig.write('\t' + 'Уровень взаимности компоненты сильной связности: ' + str(nx.overall_reciprocity(G_strong)) + "\n")

    # Центральность
    ig.write("6. Коэффициенты центральности.\n")
    firstArray = []
    secondArray = []
    matrix = []
    transposed = []
    lines = [line.rstrip('\n') for line in open('Information/listEdges.txt')]
    for i in range(len(lines)):
        input_id = lines[i]
        firstTemp = (input_id.split()[:1])
        firstTemp = firstTemp[0]
        firstArray.append(firstTemp)
        secondTemp = (input_id.split()[1:2])
        secondTemp = secondTemp[0]
        secondArray.append(secondTemp)

    matrix.append(firstArray)
    matrix.append(secondArray)

    for i in range(len(firstArray)):
        transposed_row = []
        for row in matrix:
            transposed_row.append(row[i])
        transposed.append(transposed_row)

    def summary(G):
        cc = nx.closeness_centrality(G)
        df = pd.DataFrame.from_dict({
            'Вершина': list(cc.keys()),
            'Центральность': list(cc.values())
        })
        ig.write(str(df.sort_values('Центральность', ascending=False)))

    G = nx.DiGraph(transposed)
    summary(G)

    #Алгоритмы графа
    cc = nx.closeness_centrality(G)
    arrayCent = list(cc.values())
    arrayVersh = list(cc.keys())
    numberMaxVersh = arrayCent.index(max(arrayCent))
    maxVersh = arrayVersh[numberMaxVersh]

    with open('Information/listEdges.txt') as f:
        myList = [line.split() for line in f]
    first_number_all = []
    second_number = []
    my = {}

    for i in range(len(myList)):
        first_number_all.append(int(myList[i][0]))
        second_number.append(int(myList[i][1]))

    for i in range(len(first_number_all)):
        my[str(first_number_all[i])] = []

    first_number_new = [el for el, _ in groupby(first_number_all)]

    for i in range(len(first_number_all)):
        for j in range(len(first_number_new)):
            if first_number_all[i] == first_number_new[j]:
                my[str(first_number_new[j])].append(str(myList[i][1]))

    for item in tuple(my):
        if my[item] == []:
            del my[item]

    #Ширина
    def bfs_connected_component(my, start):
        explored = []
        queue = [start]

        while queue:
            node = queue.pop(0)
            if node not in explored:
                explored.append(node)
                neighbours = my[node]

                for neighbour in neighbours:
                    queue.append(neighbour)
        return explored
    bfs = bfs_connected_component(my, maxVersh)
    ig.write("\n7. Поиск в ширину.\n")
    for i in range(len(bfs)):
        j = i + 1
        ig.write('\t' + str(j) + ") " + str(bfs[i]) + "\n")

    # Глубина
    def dfs(graph, node):
        global visited
        if node not in visited:
            visited.append(node)
            for n in graph[node]:
                dfs(graph, n)

    dfs(my, maxVersh)
    ig.write("8. Поиск в глубину.\n")
    for k in range(len(visited)):
        j = k + 1
        ig.write('\t' + str(j) + ") " + str(visited[k])+ "\n")

    tt = round((time.time() - start), 2)
    mes = 'Время выполнения задачи ' + str(tt) + ' секунд'
    logInfo(mes, 'analysis')

def createGraphFriends():
    vk_session = vk_api.VkApi(login, password)
    vk = vk_session.get_api()

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    g = nx.Graph(directed=False)
    listUsers = []
    start = time.time()

    lines = [line.rstrip('\n') for line in open('ids.txt')]
    user_friend = vk.friends.get(user_id=(lines[0]), fields=('domain'))
    countFriend = user_friend['count']
    for j in range(countFriend):
        listUsers.append(str(user_friend['items'][j]['id']))
    f = open("Information/listEdges.txt", "w")
    f.close()
    f = open("Information/listEdges.txt", "r+")
    listUsers.append(lines[0])
    mes = 'Выполняется построение графа. Компонентов: ' + str(len(listUsers))
    logInfo(mes, 'analysis')
    for i in range(len(listUsers)):
        try:
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

            node = listUsers[i]
            g.add_node(node)
            print("{}) Профиль {} просмотрен. Открытый".format(i + 1, node))

            for j in range(len(commonFriends)):
                if (listUsers[i] != commonFriends[j]):
                    g.add_edge(listUsers[i], commonFriends[j])
                    f.write(str(listUsers[i]) + " " + str(commonFriends[j] + "\n"))
                    f.write(str(commonFriends[j]) + " " + str(listUsers[i] + "\n"))
        except:
            print("{}) Профиль {} просмотрен. Закрытый".format(i + 1, node))

    nx.write_graphml(g, "Information/graphRelationships.graphml")
    f.close()
    file = "Information/listEdges.txt"
    uniqlines = set(open(file, 'r', encoding='utf-8').readlines())
    gotovo = open(file, 'w', encoding='utf-8').writelines(set(uniqlines))

    tt = round((time.time() - start), 2)
    mes = 'Время выполнения задачи ' + str(tt) + ' секунд'
    logInfo(mes, 'analysis')
    return(g)
    
def selectVladimir():
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    lines = [line.rstrip('\n') for line in open('ids.txt')]
    cities = []
    names = []
    mes = 'Выполняется фильтр (г. Владимир). Компонентов: ' + str(len(lines))
    logInfo(mes, 'filter')
    start = time.time()
    for i in range(len(lines)):
        input_id = lines[i]
        user_get = vk.users.get(user_ids=(input_id), fields=("city"))
        user_get = user_get[0]
        names.append(input_id + '\n')
        print("{}) Профиль {} просмотрен".format(i + 1, lines[i]))
        try:
            city = user_get['city']['title']
            cities.append(city)
        except:
            temp = 'none'
            cities.append(temp)
    f = open("ids.txt", "r+")
    d = f.readlines()
    f.seek(0)
    for i in range(len(d)):
        if cities[i] == 'Владимир':
            if i != d[i]:
                f.write(d[i])
    f.truncate()
    f.close()

    tt = round((time.time() - start), 2)
    mes = 'Время выполнения фильтра ' + str(tt) + ' секунд'
    logInfo(mes, 'filter')

def selectNonVladimir():
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    lines = [line.rstrip('\n') for line in open('ids.txt')]
    cities = []
    names = []
    mes = 'Выполняется фильтр (не г. Владимир). Компонентов: ' + str(len(lines))
    logInfo(mes, 'filter')
    start = time.time()
    for i in range(len(lines)):
        input_id = lines[i]
        user_get = vk.users.get(user_ids=(input_id), fields=("city"))
        user_get = user_get[0]
        names.append(input_id + '\n')
        print("{}) Профиль {} просмотрен".format(i + 1, lines[i]))
        try:
            city = user_get['city']['title']
            cities.append(city)
        except:
            temp = 'none'
            cities.append(temp)
    f = open("ids.txt", "r+")
    d = f.readlines()
    f.seek(0)
    for i in range(len(d)):
        if cities[i] != 'Владимир':
            if i != d[i]:
                f.write(d[i])
    f.truncate()
    f.close()

    tt = round((time.time() - start), 2)
    mes = 'Время выполнения фильтра ' + str(tt) + ' секунд'
    logInfo(mes, 'filter')

def selectMoreYears18():
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    lines = [line.rstrip('\n') for line in open('ids.txt')]
    result = []
    names = []
    mes = 'Выполняется фильтр (страше 18 лет). Компонентов: ' + str(len(lines))
    logInfo(mes, 'filter')
    start = time.time()
    for i in range(len(lines)):
        input_id = lines[i]
        user_get = vk.users.get(user_ids=(input_id), fields=("bdate"))
        user_get = user_get[0]
        names.append(input_id+'\n')
        try:
            from datetime import datetime
            bdate = user_get['bdate']
            array_bd = bdate.split('.')
            newyear = int(array_bd[2])+int(18)
            day = int (array_bd[0])
            mon = int(array_bd[1])
            year = int(newyear)
            deadline = datetime(year, mon, day)
            now = datetime.now()
            if now >= deadline:
                result.append(1)
            #elif now.day == deadline.day and now.month == deadline.month and now.year == deadline.year:
            #    result.append('1')
            else:
                result.append(0)
        except:
            result.append(0)
        print("{}) Профиль {} просмотрен".format(i + 1, lines[i]))
    f = open("ids.txt", "r+")
    d = f.readlines()
    f.seek(0)
    for i in range(len(d)):
        if result[i] == 1:
            if i != d[i]:
                f.write(d[i])
    f.truncate()
    f.close()

    tt = round((time.time() - start), 2)
    mes = 'Время выполнения фильтра ' + str(tt) + ' секунд'
    logInfo(mes, 'filter')

def selectLessYears18():
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    lines = [line.rstrip('\n') for line in open('ids.txt')]
    result = []
    names = []
    mes = 'Выполняется фильтр (младше 18 лет). Компонентов: ' + str(len(lines))
    logInfo(mes, 'filter')
    start = time.time()
    for i in range(len(lines)):
        input_id = lines[i]
        user_get = vk.users.get(user_ids=(input_id), fields=("bdate"))
        user_get = user_get[0]
        names.append(input_id+'\n')
        try:
            from datetime import datetime
            bdate = user_get['bdate']
            array_bd = bdate.split('.')
            newyear = int(array_bd[2])+int(18)
            day = int (array_bd[0])
            mon = int(array_bd[1])
            year = int(newyear)
            deadline = datetime(year, mon, day)
            now = datetime.now()
            if now < deadline:
                result.append(1)
            #elif now.day == deadline.day and now.month == deadline.month and now.year == deadline.year:
            #    result.append('1')
            else:
                result.append(0)
        except:
            result.append(0)
        print("{}) Профиль {} просмотрен".format(i + 1, lines[i]))
    f = open("ids.txt", "r+")
    d = f.readlines()
    f.seek(0)
    for i in range(len(d)):
        if result[i] == 1:
            if i != d[i]:
                f.write(d[i])
    f.truncate()
    f.close()

    tt = round((time.time() - start), 2)
    mes = 'Время выполнения фильтра ' + str(tt) + ' секунд'
    logInfo(mes, 'filter')

def selectBoys():
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    lines = [line.rstrip('\n') for line in open('ids.txt')]
    sexes = []
    names = []
    mes = 'Выполняется фильтр (мужчины). Компонентов: ' + str(len(lines))
    logInfo(mes, 'filter')
    start = time.time()
    for i in range(len(lines)):
        input_id = lines[i]
        user_get = vk.users.get(user_ids=(input_id), fields=("sex"))
        user_get = user_get[0]
        sex = user_get['sex']
        sexes.append(sex)
        names.append(input_id+'\n')
        print("{}) Профиль {} просмотрен".format(i + 1, lines[i]))
    f = open("ids.txt", "r+")
    d = f.readlines()
    f.seek(0)
    for i in range(len(d)):
        if sexes[i] == 2:
            if i != d[i]:
                f.write(d[i])
    f.truncate()
    f.close()

    tt = round((time.time() - start), 2)
    mes = 'Время выполнения фильтра ' + str(tt) + ' секунд'
    logInfo(mes, 'filter')

def selectGirls():
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    lines = [line.rstrip('\n') for line in open('ids.txt')]
    sexes = []
    names = []
    mes = 'Выполняется фильтр (девушки). Компонентов: ' + str(len(lines))
    logInfo(mes, 'filter')
    start = time.time()
    for i in range(len(lines)):
        input_id = lines[i]
        user_get = vk.users.get(user_ids=(input_id), fields=("sex"))
        user_get = user_get[0]
        sex = user_get['sex']
        sexes.append(sex)
        names.append(input_id+'\n')
        print("{}) Профиль {} просмотрен".format(i + 1, lines[i]))
    f = open("ids.txt", "r+")
    d = f.readlines()
    f.seek(0)
    for i in range(len(d)):
        if sexes[i] == 1:
            if i != d[i]:
                f.write(d[i])
    f.truncate()
    f.close()

    tt = round((time.time() - start), 2)
    mes = 'Время выполнения фильтра ' + str(tt) + ' секунд'
    logInfo(mes, 'filter')

def selectOpenedToken():
    vk_session = vk_api.VkApi(login=login,
                              password=password,
                              auth_handler=auth_handler)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    start = time.time()
    lines = [line.rstrip('\n') for line in open('ids.txt')]
    typeAccount = []
    mes = 'Выполняется фильтр (открытый профиль). Компонентов: '+ str(len(lines))
    logInfo(mes, 'filter')
    for i in range(len(lines)):
        vk = vk_session.get_api()

        input_id = lines[i]
        user_get = vk.users.get(user_ids=(input_id), fields=("bdate,city,country,education,connections,domain"))
        user_get = user_get[0]
        islosed = user_get['is_closed']
        typeAccount.append(islosed)
        print("{}) Профиль {} просмотрен".format(i+1, lines[i]))

    f = open("ids.txt", "r+")
    d = f.readlines()
    f.seek(0)
    for i in range(len(d)):
        if typeAccount[i] == False:
            if i != d[i]:
                f.write(d[i])
    f.truncate()
    f.close()

    tt = round((time.time() - start), 2)
    mes = 'Время выполнения фильтра ' + str(tt) + ' секунд'
    logInfo(mes, 'filter')

def selectClosedToken():
    vk_session = vk_api.VkApi(login=login,
                              password=password,
                              auth_handler=auth_handler)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    lines = [line.rstrip('\n') for line in open('ids.txt')]
    typeAccount = []
    mes = 'Выполняется фильтр (закрытый профиль). Компонентов: ' + str(len(lines))
    logInfo(mes, 'filter')
    start = time.time()
    for i in range(len(lines)):
        vk = vk_session.get_api()
        input_id = lines[i]
        user_get = vk.users.get(user_ids=(input_id), fields=("bdate,city,country,education,connections,domain"))
        user_get = user_get[0]
        islosed = user_get['is_closed']
        typeAccount.append(islosed)
        print("{}) Профиль {} просмотрен".format(i + 1, lines[i]))

    f = open("ids.txt", "r+")
    d = f.readlines()
    f.seek(0)
    for i in range(len(d)):
        if typeAccount[i] == True:
            if i != d[i]:
                f.write(d[i])
    f.truncate()
    f.close()
    tt = round((time.time() - start), 2)
    mes = 'Время выполнения фильтра ' + str(tt) + ' секунд'
    logInfo(mes, 'filter')

def logInfo(mes, fileLog):
    current_datetime = datetime.now()
    message = '\n'
    if (fileLog == 'collection'):
        file = open("collection_logs.txt", 'a')
    elif (fileLog == 'analysis'):
        file = open("analysis_logs.txt", 'a')
    elif (fileLog == 'filter'):
        file = open("filter_logs.txt", 'a')
    message += str(current_datetime)
    message += " "
    message += str(mes)

    file.write(message)
    file.close

if __name__ == '__main__':
    mainApplication()