# -*- coding: utf-8 -*-
import os

import GlobalAppParams
import Dialogs as Dialogs
import configparser
import psycopg2

# Функции работы с локальным конфигурационным файлом

# Проверка существования папки хранения конфигурационного файла
def isConfigFolderExist (startFolder):
    workDir = os.path.abspath(os.path.dirname(startFolder)) + "\\Params"
    if not os.path.exists(workDir):
        return False
    else:
        return workDir

# Создание (при отсутствии) папки хранения конфигурационного файла
def CreateConfigFolder (startFolder):
    ConfigFolder = isConfigFolderExist(startFolder)
    if ConfigFolder == False:
        ConfigFolder = os.path.abspath(os.path.dirname(startFolder)) + "\\Params"
        try:
            os.mkdir(ConfigFolder)
        except OSError:
            return False
        else:
            return ConfigFolder
    else:
        return ConfigFolder

# Проверка существования файла хранения конфигурационного файла
def isConfigFileExist(theConfigFolder):
    ConfigFolder = CreateConfigFolder(theConfigFolder)
    if ConfigFolder == False :
        Dialogs.MessageFatalError("Не удалось создать папку для хранения конфигурационного файла.")

    ConfigFile = ConfigFolder+"\\BDConnectParams.prm"
    if not os.path.exists(ConfigFile):
        return False # Такой путь не существует
    else:
        if not os.path.isfile(ConfigFile):
            return False # Путь существует. Но это - не файл,а папка !
        else:
            return ConfigFile

# Класс описания конфигурационных параметров подключения к PostgreSQL серверу
class UniskadPostgreSqlConfig():
    def __init__(self,PostgreSQL_ConfigFilePath="",PostgreSQL_Host="localhost", \
                 PostgreSQL_IP="127.0.0.1", PostgreSQL_Port="5432", \
                 PostgreSQL_Login="evgenia", PostgreSQL_LoginPsw="1234", \
                 PostgreSQL_Database="planetarium"):
        """Конструктор класса UniskadPostgreSqlConfig"""
        self.PostgreSQL_ConfigFilePath = PostgreSQL_ConfigFilePath # Полный путь к файлу конфигурации
        self.PostgreSQL_Host = PostgreSQL_Host # Имя PostgreSql сервера
        self.PostgreSQL_IP = PostgreSQL_IP # IP PostgreSql сервера
        self.PostgreSQL_Port = PostgreSQL_Port # Порт подключения к PostgreSql сервера
        self.PostgreSQL_Login = PostgreSQL_Login # Имя пользователя PostgreSql сервера
        self.PostgreSQL_LoginPsw = PostgreSQL_LoginPsw # Пароль пользователч PostgreSql сервера
        self.PostgreSQL_Database = PostgreSQL_Database # Имя БД PostgreSql сервера
        self.PostgreSql_Connected = False # Состояние подключения к серверу
        self.PostgreSql_Connection = None # Дескриптор соединения с PostgreSQL-сервером

    def read(self):
        """ Чтение конфигурационного файла"""
        config = configparser.ConfigParser()
        config.read(self.PostgreSQL_ConfigFilePath)

        # Читаем некоторые значения из конфиг. файла.
        self.PostgreSQL_Host = config.get("Connect_PostgreSQL", "PostgreSQL_Host")
        self.PostgreSQL_IP = config.get("Connect_PostgreSQL", "PostgreSQL_IP")
        self.PostgreSQL_Port = config.get("Connect_PostgreSQL", "PostgreSQL_Port")
        self.PostgreSQL_Login = config.get("Connect_PostgreSQL", "PostgreSQL_User")
        self.PostgreSQL_LoginPsw = config.get("Connect_PostgreSQL", "PostgreSQL_UserPsw")
        self.PostgreSQL_Database = config.get("Connect_PostgreSQL", "PostgreSQL_DB_name")

    def postgreSQlConnect(self):
        """ Подключение к PostgreSQL серверу """
        try:
            self.PostgreSql_Connection = \
            psycopg2.connect(host=self.PostgreSQL_Host, hostaddr=self.PostgreSQL_IP, \
                             port=self.PostgreSQL_Port, dbname=self.PostgreSQL_Database, \
                             user=self.PostgreSQL_Login, password=self.PostgreSQL_LoginPsw, \
                             sslmode="prefer")
            self.PostgreSql_Connected = True
            GlobalAppParams.UniskadConnection = self.PostgreSql_Connection
            GlobalAppParams.UniskadConnectionState = "Соединение установлено успешно"
            GlobalAppParams.UniskadConnectionStateCode = 0
        except psycopg2.Error as err:
            self.PostgreSql_Connected = False
            GlobalAppParams.UniskadConnection = None
            GlobalAppParams.UniskadConnectionState = "Соединение не установлено. Ошибка:{}".format(err)
            GlobalAppParams.UniskadConnectionStateCode = -1
