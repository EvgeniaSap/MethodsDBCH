from Design_py import new_val_wind
from PyQt5 import (QtWidgets, QtCore)
from PyQt5.QtWidgets import *
import Dialogs as Dialogs


class NewValWindow(QtWidgets.QDialog, new_val_wind.Ui_Form):
    def __init__(self, parent=None, flag=None, UniskadConnection=None, IdTheorem=None, IdMeth=None):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. файле design.ру
        QMainWindow.__init__(self)
        QWidget.__init__(self)
        super().__init__(parent)
        self.setupUi(self) # Это нужно для инициализации нашего дизайна
        self .setFixedSize(self.width(), self .height())

        self.design_flag = flag
        self.UniskadConnection = UniskadConnection
        self.IdTheorem = IdTheorem
        print(self.IdTheorem)
        self.IdMeth = IdMeth
        self.DescrStages = ""
        self.DescrCode = ""

        self.save_new_val_pushButton.clicked.connect(self.push_save_new_val_pushButton)
        self.choose_file_pushButton.clicked.connect(self.push_choose_file_pushButton)

        self.set_design()

    def set_design(self):
        _translate = QtCore.QCoreApplication.translate

        if self.design_flag == 'task_area':
            self.label_new_name.setText(_translate("Form",
                                                   "<html><head/><body><p><span style=\" font-size:10pt;\">Название новой области задач:</span></p></body></html>"))
            self.label_type.setText(_translate("Form",
                                               "<html><head/><body><p><span style=\" font-size:10pt;\">Выберите тип области задач:</span></p></body></html>"))
            self.label_new_type_or_file.setText(_translate("Form",
                                                           "<html><head/><body><p><span style=\" font-size:10pt;\">Или введите название нового:</span></p></body></html>"))

            self.label_new_name.setVisible(True)
            self.new_name_line.setVisible(True)
            self.comboBox.setVisible(True)
            self.label_type.setVisible(True)
            self.label_new_type_or_file.setVisible(True)
            self.new_type_or_file_line.setVisible(True)
            self.choose_file_pushButton.setVisible(False)

            self.set_all_type_task_area_comboBox()

        elif self.design_flag == 'appl_area':
            self.label_new_name.setText(_translate("Form",
                                                   "<html><head/><body><p><span style=\" font-size:10pt;\">Название новой практической задачи:</span></p></body></html>"))
            self.label_type.setText(_translate("Form",
                                               "<html><head/><body><p><span style=\" font-size:10pt;\">Выберите прикладную область:</span></p></body></html>"))
            self.label_new_type_or_file.setText(_translate("Form",
                                                           "<html><head/><body><p><span style=\" font-size:10pt;\">Или введите название новой:</span></p></body></html>"))

            self.label_new_name.setVisible(True)
            self.new_name_line.setVisible(True)
            self.comboBox.setVisible(True)
            self.label_type.setVisible(True)
            self.label_new_type_or_file.setVisible(True)
            self.new_type_or_file_line.setVisible(True)
            self.choose_file_pushButton.setVisible(False)

            self.set_all_applic_area_comboBox()

        elif self.design_flag == 'cl_comp':
            self.label_new_name.setText(_translate("Form",
                                                   "<html><head/><body><p><span style=\" font-size:10pt;\">Название нового класса сложности:</span></p></body></html>"))

            self.label_new_name.setVisible(True)
            self.new_name_line.setVisible(True)
            self.comboBox.setVisible(False)
            self.label_type.setVisible(False)
            self.label_new_type_or_file.setVisible(False)
            self.new_type_or_file_line.setVisible(False)
            self.choose_file_pushButton.setVisible(False)

        elif self.design_flag == 'cl_alg':
            self.label_new_name.setText(_translate("Form",
                                                   "<html><head/><body><p><span style=\" font-size:10pt;\">Название нового класса алгоритмов:</span></p></body></html>"))

            self.label_new_name.setVisible(True)
            self.new_name_line.setVisible(True)
            self.comboBox.setVisible(False)
            self.label_type.setVisible(False)
            self.label_new_type_or_file.setVisible(False)
            self.new_type_or_file_line.setVisible(False)
            self.choose_file_pushButton.setVisible(False)

        elif self.design_flag == 'theorem1':
            self.label_new_name.setText(_translate("Form",
                                                   "<html><head/><body><p><span style=\" font-size:10pt;\">Название новой теоремы:</span></p></body></html>"))
            self.label_new_type_or_file.setText(_translate("Form",
                                                           "<html><head/><body><p><span style=\" font-size:10pt;\">Выберите файл с формулировкой:</span></p></body></html>"))

            self.label_new_name.setVisible(True)
            self.new_name_line.setVisible(True)
            self.comboBox.setVisible(False)
            self.label_type.setVisible(False)
            self.label_new_type_or_file.setVisible(True)
            self.new_type_or_file_line.setVisible(True)
            self.choose_file_pushButton.setVisible(True)

        elif self.design_flag == 'theorem2':
            self.label_new_type_or_file.setText(_translate("Form",
                                                           "<html><head/><body><p><span style=\" font-size:10pt;\">Выберите файл с формулировкой:</span></p></body></html>"))

            self.label_new_name.setVisible(False)
            self.new_name_line.setVisible(False)
            self.comboBox.setVisible(False)
            self.label_type.setVisible(False)
            self.label_new_type_or_file.setVisible(True)
            self.new_type_or_file_line.setVisible(True)
            self.choose_file_pushButton.setVisible(True)

        elif self.design_flag == 'stages':
            self.label_new_type_or_file.setText(_translate("Form",
                                                           "<html><head/><body><p><span style=\" font-size:10pt;\">Выберите файл с описанием этапов:</span></p></body></html>"))

            self.label_new_name.setVisible(False)
            self.new_name_line.setVisible(False)
            self.comboBox.setVisible(False)
            self.label_type.setVisible(False)
            self.label_new_type_or_file.setVisible(True)
            self.new_type_or_file_line.setVisible(True)
            self.choose_file_pushButton.setVisible(True)

        elif self.design_flag == 'code':
            self.label_new_type_or_file.setText(_translate("Form",
                                                           "<html><head/><body><p><span style=\" font-size:10pt;\">Выберите файл с описанием кода:</span></p></body></html>"))

            self.label_new_name.setVisible(False)
            self.new_name_line.setVisible(False)
            self.comboBox.setVisible(False)
            self.label_type.setVisible(False)
            self.label_new_type_or_file.setVisible(True)
            self.new_type_or_file_line.setVisible(True)
            self.choose_file_pushButton.setVisible(True)

        else: # flag = constr
            self.label_new_name.setText(_translate("Form",
                                                   "<html><head/><body><p><span style=\" font-size:10pt;\">Новое ограничение:</span></p></body></html>"))

            self.label_new_name.setVisible(True)
            self.new_name_line.setVisible(True)
            self.comboBox.setVisible(False)
            self.label_type.setVisible(False)
            self.label_new_type_or_file.setVisible(False)
            self.new_type_or_file_line.setVisible(False)
            self.choose_file_pushButton.setVisible(False)

    def set_all_type_task_area_comboBox(self):
        # выгрузить типы областей задач из бд
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        temp = []
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД

        stmt = "SELECT * FROM get_type_task_area()"
        cursor.execute(stmt)

        for row in cursor:
            temp.append(row[0])

        self.comboBox.clear()
        self.comboBox.addItems(temp)

    def set_all_applic_area_comboBox(self):
        # выгрузить типы областей задач из бд
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        temp = []
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД

        stmt = "SELECT * FROM get_application_area()"
        cursor.execute(stmt)
        for row in cursor:
            temp.append(row[0])

        self.comboBox.clear()
        self.comboBox.addItems(temp)

    def push_save_new_val_pushButton(self):
        if self.design_flag == 'task_area':
            if self.new_name_line.text() == "" and (self.comboBox.currentText() == "" or
            self.new_type_or_file_line.text() == ""):
                Dialogs.MessageInfo("Заполните все необходимые поля")
                return
            r = 0
            if self.new_type_or_file_line.text() != "":
                if (self.UniskadConnection == None):
                    Dialogs.MessageInfo("Нет соединения с БД")
                    return  # Нет соединения с БД

                cursor = self.UniskadConnection.cursor()  # Получить курсор БД
                # Оператор вызова хранимой процедуры проверки пароля на сервере
                stmt = "SELECT * FROM new_type_task_area('" + self.new_type_or_file_line.text() + "')"

                # Вызов выполнения хранимой процедуры
                cursor.execute(stmt)
                self.UniskadConnection.commit()

                # Проверка результата регистрации
                for row in cursor:
                    r = row[0]

            name_type =""
            if self.new_type_or_file_line.text() != "":
                name_type = self.new_type_or_file_line.text()
            else:
                name_type = self.comboBox.currentText()

            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            # Оператор вызова хранимой процедуры проверки пароля на сервере
            stmt = "SELECT * FROM new_task_area('" + name_type + "','" + self.new_name_line.text() + "')"

            # Вызов выполнения хранимой процедуры
            cursor.execute(stmt)
            self.UniskadConnection.commit()

            # Проверка результата
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Добавление прошло успешно")
            else:
                Dialogs.MessageInfo("Ошибка добавления")

        elif self.design_flag == 'appl_area':
            if self.new_name_line.text() == "" and (self.comboBox.currentText() == "" or
                                                    self.new_type_or_file_line.text() == ""):
                Dialogs.MessageInfo("Заполните все необходимые поля")
                return
            r = 0
            if self.new_type_or_file_line.text() != "":
                if (self.UniskadConnection == None):
                    Dialogs.MessageInfo("Нет соединения с БД")
                    return  # Нет соединения с БД

                cursor = self.UniskadConnection.cursor()  # Получить курсор БД
                # Оператор вызова хранимой процедуры проверки пароля на сервере
                stmt = "SELECT * FROM new_application_area('" + self.new_type_or_file_line.text() + "')"

                # Вызов выполнения хранимой процедуры
                cursor.execute(stmt)
                self.UniskadConnection.commit()

                # Проверка результата регистрации
                for row in cursor:
                    r = row[0]

            name_type = ""
            if self.new_type_or_file_line.text() != "":
                name_type = self.new_type_or_file_line.text()
            else:
                name_type = self.comboBox.currentText()

            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            # Оператор вызова хранимой процедуры проверки пароля на сервере
            stmt = "SELECT * FROM new_practical_task('" + name_type + "','" + self.new_name_line.text() + "')"

            # Вызов выполнения хранимой процедуры
            cursor.execute(stmt)
            self.UniskadConnection.commit()

            # Проверка результата
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Добавление прошло успешно")
            else:
                Dialogs.MessageInfo("Ошибка добавления")

        elif self.design_flag == 'cl_comp':
            if self.new_name_line.text() == "":
                Dialogs.MessageInfo("Заполните все необходимые поля")
                return
            r = 0

            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            # Оператор вызова хранимой процедуры проверки пароля на сервере
            stmt = "SELECT * FROM new_complexity_class('" + self.new_name_line.text() + "')"

            # Вызов выполнения хранимой процедуры
            cursor.execute(stmt)
            self.UniskadConnection.commit()

            # Проверка результата регистрации
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Добавление прошло успешно")
            else:
                Dialogs.MessageInfo("Ошибка добавления")

        elif self.design_flag == 'cl_alg':
            if self.new_name_line.text() == "":
                Dialogs.MessageInfo("Заполните все необходимые поля")
                return
            r = 0

            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            # Оператор вызова хранимой процедуры проверки пароля на сервере
            stmt = "SELECT * FROM new_algorithm_class('" + self.new_name_line.text() + "')"

            # Вызов выполнения хранимой процедуры
            cursor.execute(stmt)
            self.UniskadConnection.commit()

            # Проверка результата
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Добавление прошло успешно")
            else:
                Dialogs.MessageInfo("Ошибка добавления")

        elif self.design_flag == 'theorem1': # Новая теорема
            if self.new_name_line.text() == "" or self.new_type_or_file_line.text() == "":
                Dialogs.MessageInfo("Заполните все необходимые поля")
                return
            r = 0

            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            f = open(self.new_type_or_file_line.text(), 'r')
            statement = f.read()
            f.close()

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            # Оператор вызова хранимой процедуры проверки пароля на сервере
            stmt = "SELECT * FROM new_theorem('" + self.new_name_line.text() +\
                   "','" + statement + "','')"

            # Вызов выполнения хранимой процедуры
            cursor.execute(stmt)
            self.UniskadConnection.commit()

            # Проверка результата
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Добавление прошло успешно")
            else:
                Dialogs.MessageInfo("Ошибка добавления")

        elif self.design_flag == 'theorem2': # Новая формулировка теоремы

            if self.new_type_or_file_line.text() == "":
                Dialogs.MessageInfo("Заполните все необходимые поля")
                return
            r = 0

            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            f = open(self.new_type_or_file_line.text(), 'r')
            statement = f.read()
            f.close()

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            # Оператор вызова хранимой процедуры проверки пароля на сервере
            stmt = "SELECT * FROM update_theorem(" + str(self.IdTheorem) +\
                   ",'" + statement + "')"
            print(stmt)

            # Вызов выполнения хранимой процедуры
            cursor.execute(stmt)
            self.UniskadConnection.commit()

            # Проверка результата
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Обновление прошло успешно")
            else:
                Dialogs.MessageInfo("Ошибка добавления")


        elif self.design_flag == 'stages':
            if self.new_type_or_file_line.text() == "":
                Dialogs.MessageInfo("Заполните все необходимые поля")
                return

            f = open(self.new_type_or_file_line.text(), 'r')
            self.DescrStages = f.read()
            f.close()

        elif self.design_flag == 'code':
            if self.new_type_or_file_line.text() == "":
                Dialogs.MessageInfo("Заполните все необходимые поля")
                return

            f = open(self.new_type_or_file_line.text(), 'r')
            self.DescrCode = f.read()
            f.close()

        else: # flag = constr
            if self.new_name_line.text() == "":
                Dialogs.MessageInfo("Заполните все необходимые поля")
                return
            r = 0

            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            # Оператор вызова хранимой процедуры проверки пароля на сервере
            stmt = "SELECT * FROM new_possib_constraint('" + self.new_name_line.text() + "')"

            # Вызов выполнения хранимой процедуры
            cursor.execute(stmt)
            self.UniskadConnection.commit()

            # Проверка результата
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Добавление прошло успешно")
            else:
                Dialogs.MessageInfo("Ошибка добавления")

        self.close()

    def push_choose_file_pushButton(self):
        folder = QFileDialog.getOpenFileNames(self, 'Project Data', '')
        if folder:
            self.new_type_or_file_line.setText(folder[0][0])
        else:
            return ()

