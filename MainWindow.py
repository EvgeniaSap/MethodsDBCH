from Design_py import main_wind
from PyQt5 import (QtCore)
from PyQt5.QtWidgets import *
import RegWindow
import MethodWindow
import Dialogs as Dialogs
import hashlib
from PyQt5.QtWidgets import QTableWidgetItem
import MethodClass
import copy

# <a href="http://www.google.com">methodsdbch@gmail.com</a>
class MainWindow(QMainWindow, main_wind.Ui_Form):
    def __init__(self, parent=None, application=None, sessionUser=None, UniskadConnection=None):
        QMainWindow.__init__(self)
        self.application = application
        QWidget.__init__(self)
        super().__init__(parent)
        self.setupUi(self)  # инициализация дизайна
        self.setFixedSize(self.width(), self.height())

        self.sessionUser = sessionUser
        self.UniskadConnection = UniskadConnection

        # Личный кабинет
        self.exit_pushButton.clicked.connect(self.push_exit_pushButton)
        self.change_user_inf_pushButton.clicked.connect(self.push_change_user_inf_pushButton)
        self.save_user_inf_pushButton.clicked.connect(self.push_save_user_inf_pushButton)
        self.cancel_save_user_inf_pushButton.clicked.connect(self.push_cancel_save_user_inf_pushButton)
        self.delete_self_user_pushButton.clicked.connect(self.push_delete_self_user_pushButton)
        self.rename_self_groupBox.setVisible(False)
        self.exit_pushButton.setEnabled(True)
        self.change_user_inf_pushButton.setEnabled(True)
        self.add_new_user_pushButton.setEnabled(True)
        self.delete_self_user_pushButton.setEnabled(True)
        self.fio_line_m.setText(self.sessionUser.Name)
        self.fio_line_m.setEnabled(False)
        self.stat_line_m.setText(self.sessionUser.NameLevel)
        self.stat_line_m.setEnabled(False)
        self.login_line_m.setText(self.sessionUser.Login)


        # Поиск методов
        self.new_meth_pushButton.clicked.connect(self.push_new_meth_pushButton)
        self.more_inf_meth_pushButton.clicked.connect(self.push_more_inf_meth_pushButton)
        self.search_meth_pushButton.clicked.connect(self.push_search_meth_pushButton)
        self.set_design_search()

        self.list_cl_comlexity = [] #список id классов сложности выбранных для поиска
        self.list_cl_algorithm = [] #список id классов алгоритмов
        self.list_task_area = []  # список id областей задач
        self.list_practic_task = []  # список id практических задач
        self.list_methods = [] # список id найденных методов

        # Журнал событий
        self.choose_fd_mag_pushButton.clicked.connect(self.push_choose_fd_mag_pushButton)
        self.choose_ld_mag_pushButton.clicked.connect(self.push_choose_ld_mag_pushButton)
        self.search_mag_pushButton.clicked.connect(self.push_search_mag_pushButton)
        self.clear_fd_mag_pushButton.clicked.connect(self.push_clear_fd_mag_pushButton)
        self.clear_ld_mag_pushButton.clicked.connect(self.push_clear_ld_mag_pushButton)
        self.info_d_mag_pushButton.clicked.connect(self.push_info_d_mag_pushButton)

        # Пользователи
        self.add_new_user_pushButton.clicked.connect(self.push_add_new_user_pushButton)
        self.search_users_pushButton.clicked.connect(self.push_search_users_pushButton)
        self.block_user_pushButton.clicked.connect(self.push_block_user_pushButton)
        self.unblock_user_pushButton.clicked.connect(self.push_unblock_user_pushButton)
        self.list_users = []  # список id найденных пользователей

        self.set_design()
        self.show()

    # ДИЗАЙН И ВЫГРУЗКА ДАННЫХ
    def set_design_search(self):
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

        #temp = ["Теория чисел"]
        self.type_task_area_comboBox.addItems(temp)
        self.type_task_area_comboBox.activated[str].connect(self.onActivated_type_task_area_comboBox)

        # выгрузить области применения из бд
        temp = []
        stmt = "SELECT * FROM get_application_area()"
        cursor.execute(stmt)
        for row in cursor:
            temp.append(row[0])
        #temp = ["Криптография", "Защита информации"]

        self.applic_area_comboBox.addItems(temp)
        self.applic_area_comboBox.activated[str].connect(self.onActivated_applic_area_comboBox)

        # выгрузить из бд классы сложности
        temp = []
        # temp = ["Экспоненциальный", "Субэкспоненциальный", "Квазиполиномиальный", "Полиномиальный"]
        stmt = "SELECT * FROM get_complexity_class()"
        cursor.execute(stmt)

        self.layout_coplexity = QGridLayout()
        i = 0
        for row in cursor:
            check_box = QCheckBox(row[1], self)
            check_box.Id_cl_compexity = row[0]
            self.layout_coplexity.addWidget(check_box, i, 0)
            check_box.toggled.connect(self.onClicked_cl_complexity)
            i += 1

        win_complexity = QWidget()
        win_complexity.setLayout(self.layout_coplexity)
        self.cl_complexity_scrollArea.setWidget(win_complexity)

        # выгрузить из бд классы алгоритмов
        #temp = ["Детерминированный", "Вероятностный"]
        stmt = "SELECT * FROM get_algorithm_class()"
        cursor.execute(stmt)

        self.layout_algorithm = QGridLayout()
        i = 0
        for row in cursor:
            check_box = QCheckBox(row[1], self)
            check_box.Id_cl_algorithm = row[0]
            self.layout_algorithm.addWidget(check_box, i, 0)
            check_box.toggled.connect(self.onClicked_cl_algorithm)
            i += 1

        win_algorithm = QWidget()
        win_algorithm.setLayout(self.layout_algorithm)
        self.cl_algorithm_scrollArea.setWidget(win_algorithm)

    def onActivated_type_task_area_comboBox(self):
        # выгрузить из бд области задач по выбранному типу self.lev_acc_comboBox.currentText()
        #temp = ["Тестирование на простоту", "Тестирование на простоту чисел специального вида"]
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД

        stmt = "SELECT * FROM get_task_area('" + self.type_task_area_comboBox.currentText() + "')"
        cursor.execute(stmt)

        self.layout_task_area = QGridLayout()
        i = 0
        for row in cursor:
            check_box = QCheckBox(row[1], self)
            check_box.Id_task_area = row[0]
            self.layout_task_area.addWidget(check_box, i, 0)
            check_box.toggled.connect(self.onClicked_task_area)
            i += 1

        win_task_area = QWidget()
        win_task_area.setLayout(self.layout_task_area)
        self.task_area_scrollArea.setWidget(win_task_area)

    def onActivated_applic_area_comboBox(self):
        # выгрузить из бд области задач по выбранному типу self.lev_acc_comboBox.currentText()
        #temp = ["RSA", "Цифровая подпись"]
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД

        stmt = "SELECT * FROM get_practical_task('" + self.applic_area_comboBox.currentText() + "')"
        cursor.execute(stmt)

        self.layout_practic_task = QGridLayout()
        i = 0
        for row in cursor:
            check_box = QCheckBox(row[1], self)
            check_box.Id_practic_task = row[0]
            self.layout_practic_task.addWidget(check_box, i, 0)
            check_box.toggled.connect(self.onClicked_practic_task)
            i += 1

        win_practic_task = QWidget()
        win_practic_task.setLayout(self.layout_practic_task)
        self.practic_task_scrollArea.setWidget(win_practic_task)

    def onClicked_cl_complexity(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.list_cl_comlexity.append(cbutton.Id_cl_compexity)
        else:
            self.list_cl_comlexity.remove(cbutton.Id_cl_compexity)
        #print(self.list_cl_comlexity)

    def onClicked_cl_algorithm(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.list_cl_algorithm.append(cbutton.Id_cl_algorithm)
        else:
            self.list_cl_algorithm.remove(cbutton.Id_cl_algorithm)
        #print(self.list_cl_algorithm)

    def onClicked_task_area(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.list_task_area.append(cbutton.Id_task_area)
        else:
            self.list_task_area.remove(cbutton.Id_task_area)
        #print(self.list_task_area)

    def onClicked_practic_task(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.list_practic_task.append(cbutton.Id_practic_task)
        else:
            self.list_practic_task.remove(cbutton.Id_practic_task)
        #print(self.list_practic_task)

    def set_design(self):
        _translate = QtCore.QCoreApplication.translate
        if self.sessionUser.IdLevel == 2:
            self.new_meth_pushButton.setVisible(True)
            self.add_new_user_pushButton.setVisible(True)
            self.set_acc_level_users_comboBox()
            self.date_first_line.setEnabled(False)
            self.date_last_line.setEnabled(False)
        elif self.sessionUser.IdLevel == 3:
            self.tabWidget.clear()
            self.tabWidget.addTab(self.tab_lk, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_lk),_translate("Form", "Личный кабинет"))
            self.tabWidget.addTab(self.tab_search, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_search), _translate("Form", "Поиск"))
            self.new_meth_pushButton.setVisible(True)
            #self.add_new_user_pushButton.setVisible(False)
        else:
            self.tabWidget.clear()
            self.tabWidget.addTab(self.tab_lk, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_lk), _translate("Form", "Личный кабинет"))
            self.tabWidget.addTab(self.tab_search, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_search), _translate("Form", "Поиск"))
            self.new_meth_pushButton.setVisible(False)
            #self.add_new_user_pushButton.setVisible(False)

    def set_acc_level_users_comboBox(self):
        # выгрузить типы областей задач из бд
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        temp = ['Не указано']
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД

        stmt = "SELECT * FROM get_accesslevels()"
        cursor.execute(stmt)
        for row in cursor:
            temp.append(row[0])
        self.acc_level_users_comboBox.addItems(temp)

    # ЛИЧНЫЙ КАБИНЕТ
    def push_exit_pushButton(self):
        if Dialogs.MessageQuestionYesNo("Вы уверены, что хотите выйти?"):
            self.close()
        else:
            print('Undo close')

    def push_change_user_inf_pushButton(self):
        self.rename_self_groupBox.setVisible(True)
        self.exit_pushButton.setEnabled(False)
        self.change_user_inf_pushButton.setEnabled(False)
        self.add_new_user_pushButton.setEnabled(False)
        self.delete_self_user_pushButton.setEnabled(False)
        self.fio_line_m.setEnabled(True)

    def push_delete_self_user_pushButton(self):

        if Dialogs.MessageQuestionYesNo("Вы уверены, что хотите удалить свой аккаунт?"):
            self.sessionUser.StatusAcc = 1

            # внесение новой инфы о пользователе в бд
            r = self.update_stat_user_bd(self.sessionUser.Id, self.sessionUser.StatusAcc)
            if (r == -2):
                Dialogs.MessageInfo("Ошибка удаления")
            else:
                Dialogs.MessageInfo("Аккаунт успешно удален")

            self.close()
        else:
            print('Undo deletion')

    def push_save_user_inf_pushButton(self):
        if self.fio_line_m.text() == '' or self.login_line_m.text() == '':
            Dialogs.MessageInfo("Все поля обязательны для заполнения")

        else:
            if self.passw_line_m.text() == self.passw2_line_m.text():
                self.sessionUser.Name = self.fio_line_m.text()
                self.sessionUser.Login = self.login_line_m.text()

                if self.passw_line_m.text() != '':
                    self.sessionUser.Password = hashlib.sha224(self.passw_line_m.text().encode('ascii')).hexdigest()

                # обновление инфы о пользователи в бд
                r = self.update_inf_user_bd()
                if (r == -2):
                    Dialogs.MessageInfo("Ошибка обновления данных")
                else:
                    Dialogs.MessageInfo("Изменения успешно сохранены")

                self.exit_pushButton.setEnabled(True)
                self.change_user_inf_pushButton.setEnabled(True)
                self.add_new_user_pushButton.setEnabled(True)
                self.delete_self_user_pushButton.setEnabled(True)
                self.rename_self_groupBox.setVisible(False)
                self.fio_line_m.setEnabled(False)
                self.passw_line_m.setText('')
                self.passw2_line_m.setText('')

            else:
                Dialogs.MessageInfo("Повторно введенный пароль не совпадает\nПопробуйте снова")

    def update_inf_user_bd(self):
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД

        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        # Оператор вызова хранимой процедуры проверки пароля на сервере
        stmt = "SELECT * FROM update_user_info(" + str(self.sessionUser.Id) + "," + \
               str(self.sessionUser.IdLevel) + ",'" + self.sessionUser.Login + "','" + self.sessionUser.Password + \
               "','" + self.sessionUser.Name + "'," + str(self.sessionUser.StatusAcc) + ")"
        print(stmt)
        # Вызов выполнения хранимой процедуры
        cursor.execute(stmt)
        self.UniskadConnection.commit()

        # Проверка результата регистрации
        for row in cursor:
            r = row[0]
        return r

    def update_stat_user_bd(self, idusr, stat_acc):
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД

        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        # Оператор вызова хранимой процедуры проверки пароля на сервере
        stmt = "SELECT * FROM update_user_status(" + str(idusr) + "," + \
                str(stat_acc) + ")"
        print(stmt)
        # Вызов выполнения хранимой процедуры
        cursor.execute(stmt)
        self.UniskadConnection.commit()

        for row in cursor:
            r = row[0]
        return r

    def push_cancel_save_user_inf_pushButton(self):
        self.exit_pushButton.setEnabled(True)
        self.change_user_inf_pushButton.setEnabled(True)
        self.add_new_user_pushButton.setEnabled(True)
        self.delete_self_user_pushButton.setEnabled(True)
        self.rename_self_groupBox.setVisible(False)

        self.fio_line_m.setText(self.sessionUser.Name)
        self.fio_line_m.setEnabled(False)
        self.stat_line_m.setText(self.sessionUser.NameLevel)
        self.stat_line_m.setEnabled(False)
        self.login_line_m.setText(self.sessionUser.Login)

    # ПОИСК МЕТОДА
    def push_new_meth_pushButton(self):
        self.math_win = MethodWindow.MethodWindow(flag='new', sessionUser=self.sessionUser, UniskadConnection=self.UniskadConnection)
        self.math_win.exec()
        #self.list_methods.clear()

    def push_more_inf_meth_pushButton(self):
        #indexes = self.find_meth_tableWidget.selectionModel().selectedRows()
        id_row = self.find_meth_tableWidget.currentRow()
        if id_row == -1:
            Dialogs.MessageInfo("Необходимо выбрать один метод")
        else:
            print(str(id_row))
            print(self.list_methods)
            id_meth = self.list_methods[id_row]
            flag = ''
            if self.sessionUser.IdLevel == 4:
                flag = 'info'
            else:
                flag = 'edit'
            self.math_win = MethodWindow.MethodWindow(flag=flag, IdMeth=id_meth, sessionUser=self.sessionUser, UniskadConnection=self.UniskadConnection)
            self.math_win.exec()

    def push_search_meth_pushButton(self):
        self.list_methods.clear()
        name_meth = self.search_name_meth_line.text()
        v_memory = self.search_v_memory_line.text()
        size_list_task_area = len(self.list_task_area)
        size_list_practic_task = len(self.list_practic_task)
        size_list_cl_comlexity = len(self.list_cl_comlexity)
        size_list_cl_algorithm = len(self.list_cl_algorithm)
        arr_meths = []

        # запрос в бд на поиск метода по критерия
        if size_list_task_area != 0 and size_list_practic_task != 0:
            Dialogs.MessageInfo("Выберите значения либо из области задач,\nлибо из прикладной области")
            return

        if size_list_task_area != 0:
            if size_list_cl_comlexity != 0 and size_list_cl_algorithm != 0:

                cursor = self.UniskadConnection.cursor()  # Получить курсор БД

                for id_task_area in self.list_task_area:
                    for id_alg_cl in self.list_cl_algorithm:
                        for id_compl_cl in self.list_cl_comlexity:
                            stmt = "SELECT * FROM get_methods_crit_tarea_cla_clc('%" +\
                                name_meth + "%'," + str(id_task_area) + "," + str(id_alg_cl) + "," + \
                                   str(id_compl_cl) + ",'%" + v_memory + "%')"
                            print(stmt)
                            cursor.execute(stmt)
                            for row in cursor:
                                arr_meths = copy.deepcopy(self.check_meth_in_list(arr_meths,
                                                        MethodClass.Method(Id=row[0],
                                                                           Name=row[1],
                                                                           ValMemory=row[5],
                                                                           ValComplex=row[4],
                                                                           NameAlgCl=row[2],
                                                                           NameComplexCl=row[3])))

            elif size_list_cl_comlexity != 0:
                cursor = self.UniskadConnection.cursor()  # Получить курсор БД

                for id_task_area in self.list_task_area:
                    for id_compl_cl in self.list_cl_comlexity:
                        stmt = "SELECT * FROM get_methods_crit_tarea_clc('%" + \
                                   name_meth + "%'," + str(id_task_area) + "," + \
                                   str(id_compl_cl) + ",'%" + v_memory + "%')"
                        print(stmt)
                        cursor.execute(stmt)
                        for row in cursor:
                            arr_meths = copy.deepcopy(self.check_meth_in_list(arr_meths,
                                                        MethodClass.Method(Id=row[0],
                                                                           Name=row[1],
                                                                           ValMemory=row[5],
                                                                           ValComplex=row[4],
                                                                           NameAlgCl=row[2],
                                                                           NameComplexCl=row[3])))

            elif size_list_cl_algorithm != 0:
                cursor = self.UniskadConnection.cursor()  # Получить курсор БД

                for id_task_area in self.list_task_area:
                    for id_alg_cl in self.list_cl_algorithm:
                        stmt = "SELECT * FROM get_methods_crit_tarea_cla('%" + \
                                   name_meth + "%'," + str(id_task_area) + "," + str(id_alg_cl) + ",'%" + v_memory + "%')"
                        print(stmt)
                        cursor.execute(stmt)
                        for row in cursor:
                            arr_meths = copy.deepcopy(self.check_meth_in_list(arr_meths,
                                                                                 MethodClass.Method(
                                                                                     Id=row[0],
                                                                                     Name=row[1],
                                                                                     ValMemory=row[5],
                                                                                     ValComplex=row[4],
                                                                                     NameAlgCl=row[2],
                                                                                     NameComplexCl=row[3])))

            else:
                cursor = self.UniskadConnection.cursor()  # Получить курсор БД

                for id_task_area in self.list_task_area:
                    stmt = "SELECT * FROM get_methods_crit_tarea('%" + \
                               name_meth + "%'," + str(id_task_area) + ",'%" + v_memory + "%')"
                    print(stmt)
                    cursor.execute(stmt)
                    for row in cursor:
                        arr_meths = copy.deepcopy(self.check_meth_in_list(arr_meths,
                                                                             MethodClass.Method(
                                                                                 Id=row[0],
                                                                                 Name=row[1],
                                                                                 ValMemory=row[5],
                                                                                 ValComplex=row[4],
                                                                                 NameAlgCl=row[2],
                                                                                 NameComplexCl=row[3])))

        elif size_list_practic_task != 0:
            if size_list_cl_comlexity != 0 and size_list_cl_algorithm != 0:
                cursor = self.UniskadConnection.cursor()  # Получить курсор БД

                for id_prac_task in self.list_practic_task:
                    for id_alg_cl in self.list_cl_algorithm:
                        for id_compl_cl in self.list_cl_comlexity:
                            stmt = "SELECT * FROM get_methods_crit_ptask_cla_clc('%" + \
                                   name_meth + "%'," + str(id_prac_task) + "," + str(id_alg_cl) + "," + \
                                   str(id_compl_cl) + ",'%" + v_memory + "%')"
                            print(stmt)
                            cursor.execute(stmt)
                            for row in cursor:
                                arr_meths = copy.deepcopy(self.check_meth_in_list(arr_meths,
                                                                                 MethodClass.Method(
                                                                                     Id=row[0],
                                                                                     Name=row[1],
                                                                                     ValMemory=row[5],
                                                                                     ValComplex=row[4],
                                                                                     NameAlgCl=row[2],
                                                                                     NameComplexCl=row[3])))

            elif size_list_cl_comlexity != 0:
                cursor = self.UniskadConnection.cursor()  # Получить курсор БД

                for id_prac_task in self.list_practic_task:
                    for id_compl_cl in self.list_cl_comlexity:
                        stmt = "SELECT * FROM get_methods_crit_ptask_clc('%" + \
                                   name_meth + "%'," + str(id_prac_task) + "," + \
                                   str(id_compl_cl) + ",'%" + v_memory + "%')"
                        print(stmt)
                        cursor.execute(stmt)
                        for row in cursor:
                            arr_meths = copy.deepcopy(self.check_meth_in_list(arr_meths,
                                                                                 MethodClass.Method(
                                                                                     Id=row[0],
                                                                                     Name=row[1],
                                                                                     ValMemory=row[5],
                                                                                     ValComplex=row[4],
                                                                                     NameAlgCl=row[2],
                                                                                     NameComplexCl=row[3])))

            elif size_list_cl_algorithm != 0:
                cursor = self.UniskadConnection.cursor()  # Получить курсор БД

                for id_prac_task in self.list_practic_task:
                    for id_alg_cl in self.list_cl_algorithm:
                        stmt = "SELECT * FROM get_methods_crit_ptask_cla('%" + \
                                   name_meth + "%'," + str(id_prac_task) + "," + str(id_alg_cl) + \
                                   ",'%" + v_memory + "%')"
                        print(stmt)
                        cursor.execute(stmt)
                        for row in cursor:
                            arr_meths = copy.deepcopy(self.check_meth_in_list(arr_meths,
                                                                                 MethodClass.Method(
                                                                                     Id=row[0],
                                                                                     Name=row[1],
                                                                                     ValMemory=row[5],
                                                                                     ValComplex=row[4],
                                                                                     NameAlgCl=row[2],
                                                                                     NameComplexCl=row[3])))
                print()
            else:
                cursor = self.UniskadConnection.cursor()  # Получить курсор БД

                for id_prac_task in self.list_practic_task:
                    stmt = "SELECT * FROM get_methods_crit_ptask('%" + \
                                   name_meth + "%'," + str(id_prac_task) + ",'%" + v_memory + "%')"
                    print(stmt)
                    cursor.execute(stmt)
                    for row in cursor:
                        arr_meths = copy.deepcopy(self.check_meth_in_list(arr_meths,
                                                                                 MethodClass.Method(
                                                                                     Id=row[0],
                                                                                     Name=row[1],
                                                                                     ValMemory=row[5],
                                                                                     ValComplex=row[4],
                                                                                     NameAlgCl=row[2],
                                                                                     NameComplexCl=row[3])))

        else:
            if size_list_cl_comlexity != 0 and size_list_cl_algorithm != 0:
                cursor = self.UniskadConnection.cursor()  # Получить курсор БД

                for id_alg_cl in self.list_cl_algorithm:
                    for id_compl_cl in self.list_cl_comlexity:
                        stmt = "SELECT * FROM get_methods_crit_cla_clc('%" + \
                                   name_meth + "%'," + str(id_alg_cl) + "," + \
                                   str(id_compl_cl) + ",'%" + v_memory + "%')"
                        print(stmt)
                        cursor.execute(stmt)
                        for row in cursor:
                            arr_meths = copy.deepcopy(self.check_meth_in_list(arr_meths,
                                                                                 MethodClass.Method(
                                                                                     Id=row[0],
                                                                                     Name=row[1],
                                                                                     ValMemory=row[5],
                                                                                     ValComplex=row[4],
                                                                                     NameAlgCl=row[2],
                                                                                     NameComplexCl=row[3])))

            elif size_list_cl_comlexity != 0:
                cursor = self.UniskadConnection.cursor()  # Получить курсор БД

                for id_compl_cl in self.list_cl_comlexity:
                    stmt = "SELECT * FROM get_methods_crit_clc('%" + \
                               name_meth + "%'," + str(id_compl_cl) + ",'%" + v_memory + "%')"
                    print(stmt)
                    cursor.execute(stmt)
                    for row in cursor:
                        arr_meths = copy.deepcopy(self.check_meth_in_list(arr_meths,
                                                                             MethodClass.Method(
                                                                                 Id=row[0],
                                                                                 Name=row[1],
                                                                                 ValMemory=row[5],
                                                                                 ValComplex=row[4],
                                                                                 NameAlgCl=row[2],
                                                                                 NameComplexCl=row[3])))

            elif size_list_cl_algorithm != 0:
                cursor = self.UniskadConnection.cursor()  # Получить курсор БД

                for id_alg_cl in self.list_cl_algorithm:
                    stmt = "SELECT * FROM get_methods_crit_cla('%" + \
                               name_meth + "%'," + str(id_alg_cl) + ",'%" + v_memory + "%')"
                    print(stmt)
                    cursor.execute(stmt)
                    for row in cursor:
                        arr_meths = copy.deepcopy(self.check_meth_in_list(arr_meths,
                                                                             MethodClass.Method(
                                                                                 Id=row[0],
                                                                                 Name=row[1],
                                                                                 ValMemory=row[5],
                                                                                 ValComplex=row[4],
                                                                                 NameAlgCl=row[2],
                                                                                 NameComplexCl=row[3])))

            else:
                cursor = self.UniskadConnection.cursor()  # Получить курсор БД

                stmt = "SELECT * FROM get_methods_crit_name_v('%" + \
                           name_meth + "%','%" + v_memory + "%')"
                print(stmt)
                cursor.execute(stmt)
                for row in cursor:
                    arr_meths = copy.deepcopy(self.check_meth_in_list(arr_meths,
                                                                         MethodClass.Method(
                                                                             Id=row[0],
                                                                             Name=row[1],
                                                                             ValMemory=row[5],
                                                                             ValComplex=row[4],
                                                                             NameAlgCl=row[2],
                                                                             NameComplexCl=row[3])))

        #arr_meths = ['1','2','3']
        size_table = len(arr_meths)

        self.find_meth_tableWidget.clear()
        self.find_meth_tableWidget.setColumnCount(5)
        self.find_meth_tableWidget.setRowCount(size_table)
        self.find_meth_tableWidget.setHorizontalHeaderLabels(["Название", "Класс алгоритма", "Класс сложности", "Сложность", "Объем памяти"])

        for i in range(0, size_table):
            self.find_meth_tableWidget.setItem(i, 0, QTableWidgetItem(arr_meths[i].Name))
            self.find_meth_tableWidget.setItem(i, 1, QTableWidgetItem(arr_meths[i].NameAlgCl))
            self.find_meth_tableWidget.setItem(i, 2, QTableWidgetItem(arr_meths[i].NameComplexCl))
            self.find_meth_tableWidget.setItem(i, 3, QTableWidgetItem(arr_meths[i].ValComplex))
            self.find_meth_tableWidget.setItem(i, 4, QTableWidgetItem(arr_meths[i].ValMemory))
            self.list_methods.append(arr_meths[i].Id)

    def check_meth_in_list(self, list_meth, meth):
        if meth in list_meth:
            return list_meth
        else:
            list_meth.append(meth)
            return list_meth

    # ЖУРНАЛ СОБЫТИЙ

    def push_choose_fd_mag_pushButton(self):
        some_date = self.calendarWidget.selectedDate()
        some_date = some_date.toString('yyyy-MM-dd')
        self.date_first_line.setText(some_date)

    def push_choose_ld_mag_pushButton(self):
        some_date = self.calendarWidget.selectedDate()
        some_date = some_date.toString('yyyy-MM-dd')
        self.date_last_line.setText(some_date)

    def push_clear_fd_mag_pushButton(self):
        self.date_first_line.clear()

    def push_clear_ld_mag_pushButton(self):
        self.date_last_line.clear()

    def push_info_d_mag_pushButton(self):
        Dialogs.MessageInfo("Для установки временного диапазона необходимо\n" +
                            "сначала выбрать дату в календаре, затем нажать кнопку 'Выбрать'\n" +
                            "у поля даты, куда Вы хотите установить значение из календаря.\n" +
                            "Для очистки поля даты воспользуйтесть кнопкой 'Х'.")

    def push_search_mag_pushButton(self):
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД

        name_meth = self.name_meth_mag_line.text()
        name_user = self.fio_mag_line.text()
        f_date = self.date_first_line.text()
        l_date = self.date_last_line.text()
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        stmp = ''
        temp = []

        if f_date == '' and l_date == '':
            stmt = "SELECT * FROM get_lookbook('%" + str(name_meth) + "%','%" + str(name_user) + "%')"
        elif f_date != '' and l_date == '':
            stmt = "SELECT * FROM get_lookbook_f_date('%" + str(name_meth) + "%','%" + str(name_user) + "%','"+\
                   str(f_date)+"')"
        elif f_date == '' and l_date != '':
            stmt = "SELECT * FROM get_lookbook_l_date('%" + str(name_meth) + "%','%" + str(
                name_user) + "%','" + str(l_date) + "')"
        else:
            stmt = "SELECT * FROM get_lookbook_two_date('%" + str(name_meth) + "%','%" + str(
                name_user) + "%','" + str(f_date) + "','" + str(l_date) + "')"

        print(stmt)
        cursor.execute(stmt)
        for row in cursor:
            temp.append(row)

        size_table = len(temp)
        self.mag_tableWidget.clear()
        self.mag_tableWidget.setColumnCount(5)
        self.mag_tableWidget.setRowCount(size_table)
        self.mag_tableWidget.setHorizontalHeaderLabels(
            ["Дата", "Событие", "Метод", "Пользователь", "Уровень доступа"])

        for i in range(0, size_table):
            self.mag_tableWidget.setItem(i, 0, QTableWidgetItem(str(temp[i][0])))
            self.mag_tableWidget.setItem(i, 1, QTableWidgetItem(temp[i][1]))
            self.mag_tableWidget.setItem(i, 2, QTableWidgetItem(temp[i][2]))
            self.mag_tableWidget.setItem(i, 3, QTableWidgetItem(temp[i][3]))
            self.mag_tableWidget.setItem(i, 4, QTableWidgetItem(temp[i][4]))


    # ПОЛЬЗОВАТЕЛИ
    def push_add_new_user_pushButton(self):
        self.registr = RegWindow.RegWindow(flag=False, UniskadConnection=self.UniskadConnection)
        self.registr.exec()

    def push_search_users_pushButton(self):
        self.list_users = []
        fio = self.search_fio_user_line.text()
        namelev = self.acc_level_users_comboBox.currentText()
        temp = []
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return

        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        stmt = ""
        if namelev == "Не указано":
            stmt = "SELECT * FROM get_users_by_name('%" + fio + "%')"
        else:
            stmt = "SELECT * FROM get_users_by_name_level('%" + fio + "%','" + namelev + "')"

        print(stmt)
        cursor.execute(stmt)
        for row in cursor:
            temp.append(row)

        size_table = len(temp)
        status_acc = ['Активен', 'Заблокирован']
        self.users_tableWidget.clear()
        self.users_tableWidget.setColumnCount(4)
        self.users_tableWidget.setRowCount(size_table)
        self.users_tableWidget.setHorizontalHeaderLabels(
            ["ФИО", "Уровень доступа", "Логин", "Статус аккаунта"])

        for i in range(0, size_table):
            self.users_tableWidget.setItem(i, 0, QTableWidgetItem(temp[i][3]))
            self.users_tableWidget.setItem(i, 1, QTableWidgetItem(temp[i][5]))
            self.users_tableWidget.setItem(i, 2, QTableWidgetItem(temp[i][2]))
            self.users_tableWidget.setItem(i, 3, QTableWidgetItem(status_acc[temp[i][4]]))
            self.list_users.append(temp[i][0])

    def push_block_user_pushButton(self):
        id_row = self.users_tableWidget.currentRow()
        if id_row == -1:
            Dialogs.MessageInfo("Необходимо выбрать одного пользователя")
        else:
            if Dialogs.MessageQuestionYesNo("Вы уверены, что хотите заблокировать пользователя?"):
                stat_acc = 1
                id_usr = self.list_users[id_row]

                # внесение новой инфы о пользователе в бд
                r = self.update_stat_user_bd(id_usr, stat_acc)
                if (r == -2):
                    Dialogs.MessageInfo("Ошибка блокировки")
                else:
                    Dialogs.MessageInfo("Аккаунт успешно заблокирован")
                    self.push_search_users_pushButton()

            else:
                print('Undo deletion')

    def push_unblock_user_pushButton(self):
        id_row = self.users_tableWidget.currentRow()
        if id_row == -1:
            Dialogs.MessageInfo("Необходимо выбрать одного пользователя")
        else:
            if Dialogs.MessageQuestionYesNo("Вы уверены, что хотите разблокировать пользователя?"):
                stat_acc = 0
                id_usr = self.list_users[id_row]

                # внесение новой инфы о пользователе в бд
                r = self.update_stat_user_bd(id_usr, stat_acc)
                if (r == -2):
                    Dialogs.MessageInfo("Ошибка разблокировки")
                else:
                    Dialogs.MessageInfo("Аккаунт успешно разблокирован")
                    self.push_search_users_pushButton()

            else:
                print('Undo deletion')