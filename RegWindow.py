from Design_py import reg_wind
from PyQt5 import (QtWidgets, QtCore)
from PyQt5.QtWidgets import *
import UserClass
import Dialogs as Dialogs
import hashlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class RegWindow(QtWidgets.QDialog, reg_wind.Ui_Form):
    def __init__(self, parent=None, application=None, flag=None, UniskadConnection=None):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. файле design.ру
        QMainWindow.__init__(self)
        self.application = application
        QWidget.__init__(self)
        super().__init__(parent)
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.setFixedSize(self.width(), self.height())

        self.reg_pushButton.clicked.connect(self.push_reg_pushButton)
        self.UniskadConnection = UniskadConnection
        self.successReg = False
        self.design_flag = flag # bool: t - обычный user, f - регистрирует админ
        self.set_design()

    def set_design(self):
        _translate = QtCore.QCoreApplication.translate
        if self.design_flag:
            self.label_login.setVisible(True)
            self.login_line_reg.setVisible(True)
            self.label_pass_or_mail.setText(_translate("Form",
                                                       "<html><head/><body><p><span style=\" font-size:12pt;\">Пароль:</span></p></body></html>"))
            self.label_pass2_or_lev.setText(_translate("Form",
                                                       "<html><head/><body><p><span style=\" font-size:12pt;\">Повторите пароль:</span></p></body></html>"))
            self.lev_acc_comboBox.setVisible(False)
            self.passw2_line_reg.setVisible(True)
        else:
            self.label_login.setVisible(False)
            self.login_line_reg.setVisible(False)
            self.label_pass_or_mail.setText(_translate("Form",
                                                       "<html><head/><body><p><span style=\" font-size:12pt;\">Почта:</span></p></body></html>"))
            self.label_pass2_or_lev.setText(_translate("Form",
                                                       "<html><head/><body><p><span style=\" font-size:12pt;\">Уровень доступа:</span></p></body></html>"))
            self.lev_acc_comboBox.setVisible(True)
            self.passw2_line_reg.setVisible(False)
            self.passw_or_mail_line_reg.setVisible(False)
            self.label_pass_or_mail.setVisible(False)

            # выгрузка уровней доступа из бд

            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            # Оператор вызова хранимой процедуры проверки пароля на сервере
            stmt = "SELECT * FROM get_accesslevels()"

            # Вызов выполнения хранимой процедуры
            cursor.execute(stmt)
            arr_levels = []

            # Проверка результата регистрации
            for row in cursor:
                arr_levels.append(row[0])

            self.lev_acc_comboBox.addItems(arr_levels)
            #self.lev_acc_comboBox.activated[str].connect(self.onActivated_lev_acc_comboBox)
            #self.lev_acc_comboBox.currentText()

    def set_name_format_str(self, lname, fname, pname):
        return '{0} {1} {2}'.format(str(lname), str(fname), str(pname))

    def push_reg_pushButton(self):

        if self.design_flag:
            if self.lastname_line.text() == '' or self.firstname_line.text() == '' or \
                    self.patron_line.text() == '' or self.login_line_reg.text() == '' or \
                    self.passw_or_mail_line_reg.text() == '' or self.passw2_line_reg.text() == '':
                Dialogs.MessageInfo("Все поля обязательны для заполнения")

            else:
                if self.passw_or_mail_line_reg.text() == self.passw2_line_reg.text():
                    new_user = UserClass.User()
                    new_user.Name = self.set_name_format_str(self.lastname_line.text(),
                                                             self.firstname_line.text(),
                                                             self.patron_line.text())
                    new_user.IdLevel = '3'
                    new_user.NameLevel = 'Пользователь'
                    new_user.Login = self.login_line_reg.text()
                    new_user.Password = hashlib.sha224(self.passw_or_mail_line_reg.text().encode('ascii')).hexdigest()

                    print(self.passw_or_mail_line_reg.text())
                    print('hash pass ' + new_user.Password)

                    # вставка в бд
                    r = self.insert_new_user_bd(new_user)
                    if (r == -2):
                        Dialogs.MessageInfo("Ошибка при регистрации")
                    else:
                        Dialogs.MessageInfo(
                            "Регистрация прошла успешно\nАвторизуйтесь, чтобы войти")
                    self.close()
                else:
                    Dialogs.MessageInfo("Повторно введенный пароль не совпадает\nПопробуйте снова")


        else:
            if self.lastname_line.text() == '' or self.firstname_line.text() == '' or \
                    self.patron_line.text() == '' or self.lev_acc_comboBox.currentText() == '':
                Dialogs.MessageInfo("Все поля обязательны для заполнения")

            else:
                new_user = UserClass.User()
                new_user.Name = self.set_name_format_str(self.lastname_line.text(),
                                                         self.firstname_line.text(),
                                                         self.patron_line.text())
                new_user.Login = 'newuser'
                new_user.Password = hashlib.sha224(b"12345").hexdigest()
                print("12345")
                print('hash pass ' + new_user.Password)

                # выгрузить значение id ур дост по self.lev_acc_comboBox.currentText()
                new_user.NameLevel = self.lev_acc_comboBox.currentText()

                some_mail = self.passw_or_mail_line_reg.text()

                # вставка в бд

                r = self.insert_new_user_bd(new_user)

                if some_mail != '':
                    self.send_msg_to_new_usr(new_user, some_mail)
                    Dialogs.MessageInfo("Регистрация прошла успешно\nПользователю отправлено сообщение")
                else:
                    if (r == -2):
                        Dialogs.MessageInfo("Пользователь с таким логином уже существует\nЗадайте другой логин")
                    else:
                        Dialogs.MessageInfo(
                        "Регистрация прошла успешно\nЛогин нового пользователя: newuser\nПароль: 12345")

                self.close()

        #self.successReg = True
        #self.close()

    def insert_new_user_bd(self, new_user):
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД

        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        # Оператор вызова хранимой процедуры проверки пароля на сервере
        stmt = "SELECT * FROM new_user('" + new_user.NameLevel + "','" + \
               new_user.Login + "','" + new_user.Password + "','" + new_user.Name + "')"

        # Вызов выполнения хранимой процедуры
        cursor.execute(stmt)
        self.UniskadConnection.commit()

        # Проверка результата регистрации
        for row in cursor:
            r = row[0]
            return r


    def send_msg_to_new_usr(self, user, user_mail):
        # create message object instance
        msg = MIMEMultipart()

        message = 'Здравствуйте, {0}.\n' \
                  'Вы были добавлены в систему систематизации и мониторинга методов обработки' \
                  ' данных в больших компьютерных диапазонах.\n\n' \
                  'Параметры для входа: \n' \
                  'Логин: {1}\n' \
                  'Пароль: 12345\n\n' \
                  'Настоятельно рекомендуем сменить параметры входа в личном кабинете на более ' \
                  'надежные.\n' \
                  'Успехов и приятного пользования!\n' \
                  'С уважением, администрация MethodsDBCH.'.format(str(user.Name), str(user.Login))

        # setup the parameters of the message
        password = "methods123*"
        #msg['From'] = "methodsdbch@yandex.ru"
        msg['From'] = "methodsdbch@gmail.com"
        msg['To'] = user_mail
        msg['Subject'] = "Регистрация в системе MethodsDBCH"

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # create server
        #server = smtplib.SMTP('smtp.yandex.ru: 465')
        server = smtplib.SMTP('smtp.gmail.com: 587')

        server.starttls()

        # Login Credentials for sending the mail
        server.login(msg['From'], password)

        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())

        server.quit()

        print("successfully sent email")



