from Design_py import login_wind
from PyQt5 import (QtWidgets, QtGui)
from PyQt5.QtWidgets import *
import RegWindow
import UserClass
import Dialogs
import hashlib
import sys


class AuthWindow(QtWidgets.QDialog, login_wind.Ui_Form):
    def __init__(self, application=None, parent=None, UniskadConnection=None):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. файле design.ру
        QMainWindow.__init__(self)
        QWidget.__init__(self)
        super().__init__(parent)
        self.setupUi(self) # Это нужно для инициализации нашего дизайна
        self .setFixedSize(self.width(), self .height())
        self.application = application

        self.log_in_pushButton.clicked.connect(self.push_log_in_pushButton)
        self.registr_pushButton.clicked.connect(self.push_registr_pushButton)
        self.UniskadConnection = UniskadConnection
        self.sessionUser = None
        self.successAuth = False
        self.registr = None


    def push_log_in_pushButton(self):
        if self.login_line.text() == '' or self.passw_line.text() == '':
            Dialogs.MessageInfo("Все поля обязательны для заполнения")

        else:
            self.sessionUser = UserClass.User()
            self.sessionUser.Login = self.login_line.text()
            self.sessionUser.Password = hashlib.sha224(self.passw_line.text().encode('ascii')).hexdigest()

            # поиск в бд польз по логину и паролю
            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            stmt = "SELECT * FROM auth_user('" + self.sessionUser.Login + "','" + \
               self.sessionUser.Password + "')"
            cursor.execute(stmt)

            for row in cursor:
                self.sessionUser.Id = row[0]
                self.sessionUser.IdLevel = row[1]
                self.sessionUser.Login = row[2]
                self.sessionUser.Password = row[3]
                self.sessionUser.Name = row[4]
                self.sessionUser.NameLevel = row[5]
                self.sessionUser.StatusAcc = row[6]

            if self.sessionUser.Id == None:
                self.successAuth = False
            else:
                self.successAuth = True
            self.close()

    def push_log_in_pushButton2(self):
        if self.login_line.text() == '' or self.passw_line.text() == '':
            Dialogs.MessageInfo("Все поля обязательны для заполнения")

        else:
            self.sessionUser.Login = self.login_line.text()
            self.sessionUser.Password = hashlib.sha224(
                self.passw_line.text().encode('ascii')).hexdigest()

            self.sessionUser.Id = 1
            self.sessionUser.IdLevel = 1
            self.sessionUser.Name = "SSSSSS SS SSS"
            self.sessionUser.NameLevel = 'Главный администратор'
            self.sessionUser.StatusAcc = 0
            self.successAuth = True
            self.close()

    def push_registr_pushButton(self):
        self.registr = RegWindow.RegWindow(flag=True, UniskadConnection=self.UniskadConnection)
        self.registr.exec()
        self.registr = None

    def closeEvent(self, a0: QtGui.QCloseEvent):
        if self.registr == None and self.sessionUser == None:
            sys.exit(self.application.exec_())
