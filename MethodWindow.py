from Design_py import meth_info_wind
from PyQt5 import (QtWidgets, QtCore)
from PyQt5.QtWidgets import *
import NewValWindow
import Dialogs as Dialogs
import MethodClass
from datetime import datetime
import subprocess


class MethodWindow(QtWidgets.QDialog, meth_info_wind.Ui_Form):
    def __init__(self, parent=None, flag=None, IdMeth=None, sessionUser=None, UniskadConnection=None):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. файле design.ру
        QMainWindow.__init__(self)
        QWidget.__init__(self)
        super().__init__(parent)
        self.setupUi(self) # Это нужно для инициализации нашего дизайна
        self .setFixedSize(self.width(), self .height())

        self.design_flag = flag
        self.IdMeth = IdMeth
        self.sessionUser = sessionUser
        self.UniskadConnection = UniskadConnection

        # ДОБАВЛЕНИЕ
        self.save_changes_pushButton_inf.clicked.connect(self.push_save_changes_pushButton_inf)

        self.add_task_area_pushButton_inf.clicked.connect(self.push_add_task_area_pushButton_inf)
        self.add_appl_area_pushButton_inf.clicked.connect(self.push_add_appl_area_pushButton_inf)
        self.add_cl_complexity_pushButton_inf.clicked.connect(self.push_add_cl_complexity_pushButton_inf)
        self.add_cl_alg_pushButton_inf.clicked.connect(self.push_add_cl_alg_pushButton_inf)
        self.add_theorem_pushButton_inf.clicked.connect(self.push_add_theorem_pushButton_inf)
        self.add_constr_pushButton_inf.clicked.connect(self.push_add_constr_pushButton_inf)

        self.look_theorem_text_pushButton_inf.clicked.connect(self.push_look_theorem_text_pushButton_inf)
        self.look_stages_pushButton_inf.clicked.connect(self.push_look_stages_pushButton_inf)
        self.look_simp_code_pushButton_inf.clicked.connect(self.push_look_simp_code_pushButton_inf)
        self.bind_to_task_pushButton_inf.clicked.connect(self.push_bind_to_task_pushButton_inf)
        self.ref_bind_to_task_pushButton_inf.clicked.connect(self.push_ref_bind_to_task_pushButton_inf)

        # ПРОСМОТР ИНФОРМАЦИИ
        self.info_look_theorem_text_pushButton_inf.clicked.connect(self.push_look_theorem_text_pushButton_inf)
        self.info_look_stages_pushButton_inf.clicked.connect(self.push_look_stages_pushButton_inf)
        self.info_look_simp_code_pushButton_inf.clicked.connect(self.push_look_simp_code_pushButton_inf)

        # РЕДАКТИРОВАНИЕ
        self.edit_add_task_area_pushButton_inf.clicked.connect(self.push_add_task_area_pushButton_inf)
        self.edit_add_appl_area_pushButton_inf.clicked.connect(self.push_add_appl_area_pushButton_inf)
        self.edit_add_cl_complexity_pushButton_inf.clicked.connect(self.push_add_cl_complexity_pushButton_inf)
        self.edit_add_cl_alg_pushButton_inf.clicked.connect(self.push_add_cl_alg_pushButton_inf)
        self.edit_add_theorem_pushButton_inf.clicked.connect(self.push_add_theorem_pushButton_inf)
        self.edit_add_constr_pushButton_inf.clicked.connect(self.push_add_constr_pushButton_inf)

        self.edit_ref_bind_to_task_pushButton_inf.clicked.connect(self.push_ref_bind_to_task_pushButton_inf)
        self.edit_look_theorem_text_pushButton_inf.clicked.connect(self.push_look_theorem_text_pushButton_inf)
        self.edit_look_stages_pushButton_inf.clicked.connect(self.push_look_stages_pushButton_inf)
        self.edit_look_simp_code_pushButton_inf.clicked.connect(self.push_look_simp_code_pushButton_inf)
        self.edit_del_meth_pushButton_inf.clicked.connect(self.push_edit_del_meth_pushButton_inf)

        self.edit_add_task_for_meth_pushButton_inf.clicked.connect(self.push_edit_add_task_for_meth_pushButton_inf)
        self.edit_del_task_for_meth_pushButton_inf.clicked.connect(self.push_edit_del_task_for_meth_pushButton_inf)
        self.edit_bind_to_task_pushButton_inf.clicked.connect(self.push_edit_bind_to_task_pushButton_inf)
        self.edit_del_bind_to_task_pushButton_inf.clicked.connect(self.push_edit_del_bind_to_task_pushButton_inf)
        self.edit_bind_theorem_pushButton_inf.clicked.connect(self.push_edit_bind_theorem_pushButton_inf)
        self.edit_del_theorem_pushButton_inf.clicked.connect(self.push_edit_del_theorem_pushButton_inf)
        self.edit_bind_constr_pushButton_inf.clicked.connect(self.push_edit_bind_constr_pushButton_inf)
        self.edit_del_constr_pushButton_inf.clicked.connect(self.push_edit_del_constr_pushButton_inf)

        self.edit_save_changes_pushButton_inf.clicked.connect(self.push_edit_save_changes_pushButton_inf)

        self.list_task_area = []  # список id областей задач
        self.list_practic_task = []  # список id практических задач
        self.list_theorems = []  # список id теорем
        self.list_constr = []  # список id ограничений
        self.Method = MethodClass.Method(Id=IdMeth,UniskadConnection=self.UniskadConnection)
        self.name_file_theorem = 'C:/Users/PC/PycharmProjects/MethodsDBCH/theorem_file1.txt'
        self.name_file_stages = 'C:/Users/PC/PycharmProjects/MethodsDBCH/stages_file1.txt'
        self.name_file_code = 'C:/Users/PC/PycharmProjects/MethodsDBCH/code_file1.txt'

        self.set_design()

    # ДИЗАЙН И ВЫГРУЗКА ДАННЫХ
    def set_design(self):
        _translate = QtCore.QCoreApplication.translate

        if self.design_flag == 'new':
            self.tabWidget.clear()
            self.tabWidget.addTab(self.tab_new, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_new), _translate("Form", "Добавление нового метода"))

            self.set_design_for_new()

        elif self.design_flag == 'info':
            self.tabWidget.clear()
            self.tabWidget.addTab(self.tab_info, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_info), _translate("Form", "Информация о методе"))

            self.set_design_for_info()

        else:  # flag = edit
            self.tabWidget.clear()
            self.tabWidget.addTab(self.tab_edit, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_edit), _translate("Form", "Информация о методе с возможностью редактирования"))

            self.set_design_for_edit()

    # Для flag = new
    def set_design_for_new(self):
        # выгрузить типы областей задач из бд
        self.set_all_type_task_area_comboBox_inf()
        # выгрузить области применения из бд
        self.set_all_applic_area_comboBox_inf()
        # выгрузить из бд классы сложности
        self.set_all_cl_complexity_comboBox_inf()
        # выгрузить из бд классы алгоритмов
        self.set_all_cl_algorithm_comboBox_inf()
        self.set_all_theorems()
        self.set_all_constr()

    def set_all_type_task_area_comboBox_inf(self):
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

        # temp = ["Теория чисел"]
        self.type_task_area_comboBox_inf.clear()
        self.type_task_area_comboBox_inf.addItems(temp)
        self.type_task_area_comboBox_inf.activated[str].connect(
            self.onActivated_type_task_area_comboBox)

    def set_all_applic_area_comboBox_inf(self):
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
        # temp = ["Криптография", "Защита информации"]
        self.applic_area_comboBox_inf.clear()
        self.applic_area_comboBox_inf.addItems(temp)
        self.applic_area_comboBox_inf.activated[str].connect(self.onActivated_applic_area_comboBox)

    def set_all_cl_complexity_comboBox_inf(self):
        # выгрузить типы областей задач из бд
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        temp = []
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        # temp = ["Экспоненциальный", "Субэкспоненциальный", "Квазиполиномиальный", "Полиномиальный"]
        stmt = "SELECT * FROM get_complexity_class()"
        cursor.execute(stmt)

        cursor.execute(stmt)
        for row in cursor:
            temp.append(row[1])
        self.cl_complexity_comboBox_inf.clear()
        self.cl_complexity_comboBox_inf.addItems(temp)
        # self.cl_complexity_comboBox_inf.activated[str].connect(self.onActivated_applic_area_comboBox)

        if self.Method.NameAlgCl != "":
            self.cl_complexity_comboBox_inf.setCurrentText(self.Method.NameAlgCl)

    def set_all_cl_algorithm_comboBox_inf(self):
        # выгрузить типы областей задач из бд
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        temp = []
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        # temp = ["Детерминированный", "Вероятностный"]
        stmt = "SELECT * FROM get_algorithm_class()"
        cursor.execute(stmt)

        cursor.execute(stmt)
        for row in cursor:
            temp.append(row[1])
        self.cl_algorithm_comboBox_inf.clear()
        self.cl_algorithm_comboBox_inf.addItems(temp)
        # self.cl_algorithm_comboBox_inf.activated[str].connect(self.onActivated_applic_area_comboBox)
        if self.Method.NameComplexCl != "":
            self.cl_algorithm_comboBox_inf.setCurrentText(self.Method.NameComplexCl)

    def set_all_theorems(self):
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        self.list_theorems = []
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД

        stmt = "SELECT * FROM get_theorems()"
        cursor.execute(stmt)

        self.layout_theorems = QGridLayout()
        i = 0
        for row in cursor:
            check_box = QCheckBox(row[1], self)
            check_box.Id_theorem = row[0]
            self.layout_theorems.addWidget(check_box, i, 0)
            check_box.toggled.connect(self.onClicked_theorem)
            i += 1
            if len(self.Method.ListTheorems) != 0:
                for theor in self.Method.ListTheorems:
                    if theor.Name == row[1]:
                        check_box.checkStateSet()

        win_theorems= QWidget()
        win_theorems.setLayout(self.layout_theorems)
        self.theorems_scrollArea_inf.setWidget(win_theorems)

    def set_all_constr(self):
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        self.list_constr = []
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД

        stmt = "SELECT * FROM get_constraints()"
        cursor.execute(stmt)

        self.layout_constr = QGridLayout()
        i = 0
        for row in cursor:
            check_box = QCheckBox(row[1], self)
            check_box.Id_constr = row[0]
            self.layout_constr.addWidget(check_box, i, 0)
            check_box.toggled.connect(self.onClicked_constr)
            i += 1
            if len(self.Method.ListConstraint) != 0:
                for constr in self.Method.ListConstraint:
                    if constr == row[1]:
                        check_box.checkStateSet()

        win_constr= QWidget()
        win_constr.setLayout(self.layout_constr)
        self.constr_scrollArea_inf.setWidget(win_constr)

    def onActivated_type_task_area_comboBox(self):
        # выгрузить из бд области задач по выбранному типу self.lev_acc_comboBox.currentText()
        # temp = ["Тестирование на простоту", "Тестирование на простоту чисел специального вида"]
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД

        stmt = "SELECT * FROM get_task_area('" + self.type_task_area_comboBox_inf.currentText() + "')"
        cursor.execute(stmt)

        self.layout_task_area = QGridLayout()
        i = 0
        for row in cursor:
            check_box = QCheckBox(row[1], self)
            check_box.Id_task_area = row[0]
            self.layout_task_area.addWidget(check_box, i, 0)
            check_box.toggled.connect(self.onClicked_task_area)
            i += 1
            if len(self.Method.ListTaskArea) != 0:
                for tarea in self.Method.ListTaskArea:
                    if tarea.NameTaskArea == row[1]:
                        check_box.checkStateSet()

        win_task_area = QWidget()
        win_task_area.setLayout(self.layout_task_area)
        self.task_area_scrollArea_inf.setWidget(win_task_area)

    def onActivated_applic_area_comboBox(self):
        # выгрузить из бд области задач по выбранному типу self.lev_acc_comboBox.currentText()
        # temp = ["RSA", "Цифровая подпись"]
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД

        stmt = "SELECT * FROM get_practical_task('" + self.applic_area_comboBox_inf.currentText() + "')"
        cursor.execute(stmt)

        self.layout_practic_task = QGridLayout()
        i = 0
        for row in cursor:
            check_box = QCheckBox(row[1], self)
            check_box.Id_practic_task = row[0]
            self.layout_practic_task.addWidget(check_box, i, 0)
            check_box.toggled.connect(self.onClicked_practic_task)
            i += 1
            if len(self.Method.ListPractTask) != 0:
                for ptask in self.Method.ListPractTask:
                    if ptask.NamePractTask == row[1]:
                        check_box.checkStateSet()

        win_practic_task = QWidget()
        win_practic_task.setLayout(self.layout_practic_task)
        self.practic_task_scrollArea_inf.setWidget(win_practic_task)

    def onClicked_task_area(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.list_task_area.append(cbutton.Id_task_area)
        else:
            self.list_task_area.remove(cbutton.Id_task_area)
        # print(self.list_task_area)

    def onClicked_practic_task(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.list_practic_task.append(cbutton.Id_practic_task)
        else:
            self.list_practic_task.remove(cbutton.Id_practic_task)
        # print(self.list_practic_task)

    def onClicked_theorem(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.list_theorems.append(cbutton.Id_theorem)
        else:
            self.list_theorems.remove(cbutton.Id_theorem)
        print(self.list_theorems)

    def onClicked_constr(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.list_constr.append(cbutton.Id_constr)
        else:
            self.list_constr.remove(cbutton.Id_constr)
        print(self.list_constr)

    # Для flag = edit
    def set_design_for_edit(self):
        self.Method.set_self_values()

        self.edit_name_meth_line_inf.setText(self.Method.Name)
        self.edit_numb_stages_line_inf.setText(str(self.Method.NumbStages))
        self.edit_v_memory_line_onf.setText(self.Method.ValMemory)
        self.edit_complexity_line_inf.setText(self.Method.ValComplex)
        self.edit_cl_algorithm_line.setText(self.Method.NameAlgCl)
        self.edit_cl_complex_line.setText(self.Method.NameComplexCl)

        self.output_tasks_meth_table_edit()
        self.output_theorems_meth_table_edit()
        self.output_constr_meth_table_edit()

        # выгрузить типы областей задач из бд
        self.set_all_type_task_area_comboBox_inf_edit()
        # выгрузить области применения из бд
        self.set_all_applic_area_comboBox_inf_edit()
        # выгрузить из бд классы сложности
        self.set_all_cl_complexity_comboBox_inf_edit()
        # выгрузить из бд классы алгоритмов
        self.set_all_cl_algorithm_comboBox_inf_edit()
        self.set_all_theorems_edit()
        self.set_all_constr_edit()

        # для области задач

    def output_tasks_meth_table_edit(self):
        temp = self.get_tasks_meth_by_id() # выгрузить задачи решаемые методом
        size_table = len(temp)
        self.list_task_area.clear()
        self.edit_task_tableWidget.clear()
        self.edit_task_tableWidget.setColumnCount(4)
        self.edit_task_tableWidget.setRowCount(size_table)
        self.edit_task_tableWidget.setHorizontalHeaderLabels(
            ["Раздел математики", "Математическая задача", "Прикладная область", "Практическая задача"])

        for i in range(0, size_table):
            self.edit_task_tableWidget.setItem(i, 0, QTableWidgetItem(str(temp[i][1])))
            self.edit_task_tableWidget.setItem(i, 1, QTableWidgetItem(temp[i][2]))
            self.edit_task_tableWidget.setItem(i, 2, QTableWidgetItem(temp[i][3]))
            self.edit_task_tableWidget.setItem(i, 3, QTableWidgetItem(temp[i][4]))
            self.list_task_area.append(temp[i][0])

    def set_all_type_task_area_comboBox_inf_edit(self):
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

        self.edit_type_task_area_comboBox_inf.clear()
        self.edit_type_task_area_comboBox_inf.addItems(temp)
        self.edit_type_task_area_comboBox_inf.activated[str].connect(
            self.onActivated_edit_type_task_area_comboBox)

    def onActivated_edit_type_task_area_comboBox(self):
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД

        stmt = "SELECT * FROM get_task_area('" + self.edit_type_task_area_comboBox_inf.currentText() + "')"
        cursor.execute(stmt)
        temp = []
        for row in cursor:
            temp.append(row[1])

        self.edit_task_area_comboBox_inf.clear()
        self.edit_task_area_comboBox_inf.addItems(temp)

        # для области применения
    def set_all_applic_area_comboBox_inf_edit(self):
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

        self.edit_applic_area_comboBox_inf.clear()
        self.edit_applic_area_comboBox_inf.addItems(temp)
        self.edit_applic_area_comboBox_inf.activated[str].connect(self.onActivated_edit_applic_area_comboBox)

    def onActivated_edit_applic_area_comboBox(self):
        # выгрузить из бд области задач по выбранному типу self.lev_acc_comboBox.currentText()
        # temp = ["RSA", "Цифровая подпись"]
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД

        stmt = "SELECT * FROM get_practical_task('" + self.edit_applic_area_comboBox_inf.currentText() + "')"
        cursor.execute(stmt)
        temp = []
        for row in cursor:
            temp.append(row[1])

        self.edit_pract_task_comboBox_inf.clear()
        self.edit_pract_task_comboBox_inf.addItems(temp)

        # для классов сложности
    def set_all_cl_complexity_comboBox_inf_edit(self):
        # выгрузить типы областей задач из бд
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        temp = []
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        # temp = ["Экспоненциальный", "Субэкспоненциальный", "Квазиполиномиальный", "Полиномиальный"]
        stmt = "SELECT * FROM get_complexity_class()"
        cursor.execute(stmt)

        for row in cursor:
            temp.append(row[1])

        self.edit_cl_complexity_comboBox_inf.clear()
        self.edit_cl_complexity_comboBox_inf.addItems(temp)
        self.edit_cl_complexity_comboBox_inf.activated[str].connect(self.onActivated_edit_cl_complexity_comboBox)

    def onActivated_edit_cl_complexity_comboBox(self):
        self.edit_cl_complex_line.setText(self.edit_cl_complexity_comboBox_inf.currentText())

    def set_all_cl_algorithm_comboBox_inf_edit(self):
        # выгрузить типы областей задач из бд
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        temp = []
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        # temp = ["Детерминированный", "Вероятностный"]
        stmt = "SELECT * FROM get_algorithm_class()"
        cursor.execute(stmt)

        for row in cursor:
            temp.append(row[1])

        self.edit_cl_algorithm_comboBox_inf.clear()
        self.edit_cl_algorithm_comboBox_inf.addItems(temp)
        self.edit_cl_algorithm_comboBox_inf.activated[str].connect(self.onActivated_edit_cl_algorithm_comboBox)

    def onActivated_edit_cl_algorithm_comboBox(self):
        self.edit_cl_algorithm_line.setText(self.edit_cl_algorithm_comboBox_inf.currentText())

        # для тоерем и граничений
    def set_all_theorems_edit(self):
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД

        stmt = "SELECT * FROM get_theorems()"
        cursor.execute(stmt)

        temp = []
        for row in cursor:
            temp.append(row[1])

        self.edit_theorem_comboBox_inf.clear()
        self.edit_theorem_comboBox_inf.addItems(temp)
        #self.edit_theorem_comboBox_inf.activated[str].connect(
         #   self.onActivated_edit_type_task_area_comboBox)

    def output_theorems_meth_table_edit(self):
        size_table = len(self.Method.ListTheorems)
        self.edit_theorems_tableWidget.clear()
        self.edit_theorems_tableWidget.setColumnCount(1)
        self.edit_theorems_tableWidget.setRowCount(size_table)
        self.edit_theorems_tableWidget.setHorizontalHeaderLabels(["Название"])

        for i in range(0, size_table):
            self.edit_theorems_tableWidget.setItem(i, 0, QTableWidgetItem(self.Method.ListTheorems[i].Name))

    def set_all_constr_edit(self):
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД

        stmt = "SELECT * FROM get_constraints()"
        cursor.execute(stmt)
        temp = []
        for row in cursor:
            temp.append(row[1])

        self.edit_constr_comboBox_inf.clear()
        self.edit_constr_comboBox_inf.addItems(temp)
        # self.edit_constr_comboBox_inf.activated[str].connect(
        #   self.onActivated_edit_type_task_area_comboBox)

    def output_constr_meth_table_edit(self):
        size_table = len(self.Method.ListConstraint)
        self.edit_constr_tableWidget.clear()
        self.edit_constr_tableWidget.setColumnCount(1)
        self.edit_constr_tableWidget.setRowCount(size_table)
        self.edit_constr_tableWidget.setHorizontalHeaderLabels(["Формулировка"])

        for i in range(0, size_table):
            self.edit_constr_tableWidget.setItem(i, 0, QTableWidgetItem(self.Method.ListConstraint[i]))

    # Для flag = info
    def set_design_for_info(self):
        self.Method.set_self_values()

        self.info_name_meth_line_inf.setText(self.Method.Name)
        self.info_name_meth_line_inf.setEnabled(False)
        self.info_cl_complex_line.setText(self.Method.NameComplexCl)
        self.info_cl_complex_line.setEnabled(False)
        self.info_cl_algorithm_line.setText(self.Method.NameAlgCl)
        self.info_cl_algorithm_line.setEnabled(False)
        self.info_v_memory_line_onf.setText(self.Method.ValMemory)
        self.info_v_memory_line_onf.setEnabled(False)
        self.info_complexity_line_inf.setText(self.Method.ValComplex)
        self.info_complexity_line_inf.setEnabled(False)
        self.info_numb_stages_line_inf.setText(str(self.Method.NumbStages))
        self.info_numb_stages_line_inf.setEnabled(False)

        self.output_theorems_meth_table_info()
        self.output_constr_meth_table_info()
        self.output_tasks_meth_table_info()

    def output_theorems_meth_table_info(self):
        size_table = len(self.Method.ListTheorems)
        self.info_theorems_tableWidget.clear()
        self.info_theorems_tableWidget.setColumnCount(1)
        self.info_theorems_tableWidget.setRowCount(size_table)
        self.info_theorems_tableWidget.setHorizontalHeaderLabels(["Название"])

        for i in range(0, size_table):
            self.info_theorems_tableWidget.setItem(i, 0, QTableWidgetItem(self.Method.ListTheorems[i].Name))

    def output_constr_meth_table_info(self):
        size_table = len(self.Method.ListConstraint)
        self.info_constr_tableWidget.clear()
        self.info_constr_tableWidget.setColumnCount(1)
        self.info_constr_tableWidget.setRowCount(size_table)
        self.info_constr_tableWidget.setHorizontalHeaderLabels(["Формулировка"])

        for i in range(0, size_table):
            self.info_constr_tableWidget.setItem(i, 0, QTableWidgetItem(self.Method.ListConstraint[i]))

    def output_tasks_meth_table_info(self):
        temp = self.get_tasks_meth_by_id() # выгрузить задачи решаемые методом
        size_table = len(temp)
        self.inf_task_tableWidget.clear()
        self.inf_task_tableWidget.setColumnCount(4)
        self.inf_task_tableWidget.setRowCount(size_table)
        self.inf_task_tableWidget.setHorizontalHeaderLabels(
            ["Раздел математики", "Математическая задача", "Прикладная область", "Практическая задача"])

        for i in range(0, size_table):
            self.inf_task_tableWidget.setItem(i, 0, QTableWidgetItem(str(temp[i][1])))
            self.inf_task_tableWidget.setItem(i, 1, QTableWidgetItem(temp[i][2]))
            self.inf_task_tableWidget.setItem(i, 2, QTableWidgetItem(temp[i][3]))
            self.inf_task_tableWidget.setItem(i, 3, QTableWidgetItem(temp[i][4]))

    def get_tasks_meth_by_id(self): # выгрузить задачи решаемые методом
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД
        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        temp = []
        stmt = "SELECT * FROM get_tasks_method_by_id(" + str(self.Method.Id) + ")"
        print(stmt)
        cursor.execute(stmt)
        for row in cursor:
            temp.append(row)

        return temp

    # РАБОТА С КНОПКАМИ

    # ДОБАВЛЕНИЕ
    def push_save_changes_pushButton_inf(self):
        self.Method.Name = self.name_meth_line_inf.text()
        self.Method.NumbStages = self.numb_stages_line_inf.text()
        self.Method.ValMemory = self.v_memory_line_onf.text()
        self.Method.ValComplex = self.complexity_line_inf.text()
        self.Method.NameAlgCl = self.cl_algorithm_comboBox_inf.currentText()
        self.Method.NameComplexCl = self.cl_complexity_comboBox_inf.currentText()
        date_entry = datetime.now().date()

        if self.design_flag == 'new':
            if self.name_meth_line_inf.text() == "":
                Dialogs.MessageInfo("Заполните все необходимые поля")
                return
            r = 0

            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            # Оператор вызова хранимой процедуры проверки пароля на сервере
            stmt = "SELECT * FROM new_method_logbook('" + self.Method.Name +\
                   "'," + self.Method.NumbStages + ",'" + self.Method.ValMemory +\
                   "','" + self.Method.DescriptionStages + "','" + self.Method.SimpCode +\
                   "','" + self.Method.ValComplex + "','" + self.Method.NameAlgCl +\
                   "','" + self.Method.NameComplexCl + "'," + str(self.sessionUser.Id) + \
                   ",'" + str(date_entry) + "')"

            print(stmt)
            # Вызов выполнения хранимой процедуры
            cursor.execute(stmt)
            self.UniskadConnection.commit()

            # Проверка результата
            for row in cursor:
                r = row[0]

            if r != -2:
                for i in self.list_task_area:
                    stmt = "SELECT * FROM new_method_task_area(" + str(r) + "," + str(i) + ")"
                    print(stmt)
                    cursor.execute(stmt)
                    self.UniskadConnection.commit()

                for i in self.list_theorems:
                    stmt = "SELECT * FROM new_method_theorem(" + str(r) + "," + str(i) + ")"
                    print(stmt)
                    cursor.execute(stmt)
                    self.UniskadConnection.commit()

                for i in self.list_constr:
                    stmt = "SELECT * FROM new_method_constraint(" + str(r) + "," + str(i) + ")"
                    print(stmt)
                    cursor.execute(stmt)
                    self.UniskadConnection.commit()

                Dialogs.MessageInfo("Добавление прошло успешно")
            else:
                Dialogs.MessageInfo("Ошибка добавления")

        self.close()

    def push_add_task_area_pushButton_inf(self):
        self.newval = NewValWindow.NewValWindow(flag='task_area',UniskadConnection=self.UniskadConnection)
        self.newval.exec()
        if self.design_flag == 'new':
            self.set_all_type_task_area_comboBox_inf()

    def push_add_appl_area_pushButton_inf(self):
        self.newval = NewValWindow.NewValWindow(flag='appl_area',UniskadConnection=self.UniskadConnection)
        self.newval.exec()
        if self.design_flag == 'new':
            self.set_all_applic_area_comboBox_inf()

    def push_add_cl_complexity_pushButton_inf(self):
        self.newval = NewValWindow.NewValWindow(flag='cl_comp',UniskadConnection=self.UniskadConnection)
        self.newval.exec()
        if self.design_flag == 'new':
            self.set_all_cl_complexity_comboBox_inf()

    def push_add_cl_alg_pushButton_inf(self):
        self.newval = NewValWindow.NewValWindow(flag='cl_alg',UniskadConnection=self.UniskadConnection)
        self.newval.exec()
        if self.design_flag == 'new':
            self.set_all_cl_algorithm_comboBox_inf()

    def push_add_theorem_pushButton_inf(self):
        self.newval = NewValWindow.NewValWindow(flag='theorem1',UniskadConnection=self.UniskadConnection)
        self.newval.exec()
        if self.design_flag == 'new':
            self.set_all_theorems()

    def push_add_constr_pushButton_inf(self):
        self.newval = NewValWindow.NewValWindow(flag='constr',UniskadConnection=self.UniskadConnection)
        self.newval.exec()
        if self.design_flag == 'new':
            self.set_all_constr()

    def push_look_theorem_text_pushButton_inf(self):
        if self.design_flag != 'info':
            if Dialogs.MessageQuestionYesNo("Добавить новую формулировку теоремы?"):
                self.newval = NewValWindow.NewValWindow(flag='theorem2',UniskadConnection=self.UniskadConnection,IdTheorem=self.list_theorems[0])
                self.newval.exec()
            else:
                if self.design_flag == 'edit':
                    self.get_text_theorem_bd_table_edit()
                else:
                    self.get_text_theorem_bd_checkbox() #открытие файла с формулировкой теоремы
        else:
            self.get_text_theorem_bd_table()

    def get_text_theorem_bd_checkbox(self): #выгрузка и открытие файла с формулировкой теоремы
        if len(self.list_theorems) == 1:
            print('Open file theorem')
            id_theorem = self.list_theorems[0]
            statement = ""
            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД
            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            # выгрузить формулировку теоремы по id
            stmt = "SELECT * FROM get_theorems_by_id_theorem(" + str(id_theorem) + ")"
            cursor.execute(stmt)

            for row in cursor:
                statement = row[0]

            self.get_self_info_meth_file(self.name_file_theorem, statement)
        else:
            Dialogs.MessageInfo("Выберите одну теорему, чтобы посмотреть формулировку")

    def push_look_stages_pushButton_inf(self):
        if self.design_flag != 'info':
            if Dialogs.MessageQuestionYesNo("Добавить новое описание этапов?"):
                self.newval = NewValWindow.NewValWindow(flag='stages',UniskadConnection=self.UniskadConnection)
                self.newval.exec()
                self.Method.DescriptionStages = self.newval.DescrStages
            else:
                print('Open file stages')
                self.get_self_info_meth_file(self.name_file_stages, self.Method.DescriptionStages) #открытие файла с описанием шагов метода
        else:
            print('Open file stages')
            self.get_self_info_meth_file(self.name_file_stages, self.Method.DescriptionStages)

    def get_self_info_meth_file(self, name_file, info_meth): #открытие файла с описанием критерия метода (шаги, код)
        f = open(name_file, 'w+')
        f.write(info_meth)
        f.close()
        subprocess.call(['notepad.exe', name_file])

    def push_look_simp_code_pushButton_inf(self):
        if self.design_flag != 'info':
            if Dialogs.MessageQuestionYesNo("Добавить новый упрощенный код алгоритма?"):
                self.newval = NewValWindow.NewValWindow(flag='code',UniskadConnection=self.UniskadConnection)
                self.newval.exec()
                self.Method.SimpCode = self.newval.DescrCode
            else:
                print('Open file alg')
                self.get_self_info_meth_file(self.name_file_code, self.Method.SimpCode)
        else:
            print('Open file alg')
            self.get_self_info_meth_file(self.name_file_code, self.Method.SimpCode)

    def push_bind_to_task_pushButton_inf(self):
        if len(self.list_task_area) != 1 and len(self.list_practic_task) != 1:
            Dialogs.MessageInfo("Необходимо выбрать одну задачу из области задач\n" +
                                "и одну практическую задачу.")
        else:
            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            stmt = "SELECT * FROM new_pract_task_area(" + str(self.list_task_area[0]) +\
                   "," + str(self.list_practic_task[0]) + ")"
            cursor.execute(stmt)
            self.UniskadConnection.commit()
            # Проверка результата
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Связь задач успешно установлена")
            else:
                Dialogs.MessageInfo("Связь уже существует")

    # РЕДАКТИРОВАНИЕ
    def push_ref_bind_to_task_pushButton_inf(self):
            Dialogs.MessageInfo("Прикладная задача привязывается к математической.\n" + \
                            "Выберите одну математическую задачу и одну прикладную и добавьте связь.\n" + \
                            "Иначе отмеченные прикладные задачи не будут добавлены.")

    def get_text_theorem_bd_table_edit(self):
        id_row = self.edit_theorems_tableWidget.currentRow()
        if id_row == -1:
            Dialogs.MessageInfo("Необходимо выбрать одину теорему")
        else:
            self.get_self_info_meth_file(self.name_file_theorem,
                                         self.Method.ListTheorems[id_row].Statement)

    def push_edit_del_meth_pushButton_inf(self):
        if Dialogs.MessageQuestionYesNo("Вы уверены, что хотите удалить метод из реестра?"):
            new_stat = 1

            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            # Оператор вызова хранимой процедуры проверки пароля на сервере
            stmt = "SELECT * FROM update_method_status(" + str(self.Method.Id) + "," + str(new_stat) + ")"
            print(stmt)
            # Вызов выполнения хранимой процедуры
            cursor.execute(stmt)
            self.UniskadConnection.commit()

            # Проверка результата регистрации
            for row in cursor:
                r = row[0]
            if (r == -2):
                Dialogs.MessageInfo("Ошибка удаления")
            else:
                self.insert_new_lookbook_del()
                Dialogs.MessageInfo("Метод успешно удален")
            self.close()
        else:
            print('Undo deletion')

    def push_edit_save_changes_pushButton_inf(self):
        self.Method.Name = self.edit_name_meth_line_inf.text()
        self.Method.NumbStages = self.edit_numb_stages_line_inf.text()
        self.Method.ValMemory = self.edit_v_memory_line_onf.text()
        self.Method.ValComplex = self.edit_complexity_line_inf.text()
        self.Method.NameAlgCl = self.edit_cl_algorithm_line.text()
        self.Method.NameComplexCl = self.edit_cl_complex_line.text()
        date_entry = datetime.now().date()

        if self.edit_name_meth_line_inf.text() == "":
            Dialogs.MessageInfo("Заполните все необходимые поля")
            return
        r = 0

        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД

        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        # Оператор вызова хранимой процедуры проверки пароля на сервере
        stmt = "SELECT * FROM update_method_logbook(" + str(self.Method.Id) + ",'" + self.Method.Name + \
               "'," + self.Method.NumbStages + ",'" + self.Method.ValMemory + \
               "','" + self.Method.DescriptionStages + "','" + self.Method.SimpCode + \
               "','" + self.Method.ValComplex + "','" + self.Method.NameAlgCl + \
               "','" + self.Method.NameComplexCl + "'," + str(self.sessionUser.Id) + \
               ",'" + str(date_entry) + "')"

        print(stmt)
        # Вызов выполнения хранимой процедуры
        cursor.execute(stmt)
        self.UniskadConnection.commit()

        # Проверка результата
        for row in cursor:
            r = row[0]

        if r != -2:
            Dialogs.MessageInfo("Изменение прошло успешно")
        else:
            Dialogs.MessageInfo("Ошибка изменения")

        self.close()

    def push_edit_add_task_for_meth_pushButton_inf(self):
        name_task = self.edit_task_area_comboBox_inf.currentText()
        if name_task == "":
            Dialogs.MessageInfo("Необходимо выбрать математическую задачу")
        else:
            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            stmt = "SELECT * FROM new_method_task_area(" + str(self.Method.Id) + ",'" + str(name_task) + "')"
            print(stmt)
            cursor.execute(stmt)
            self.UniskadConnection.commit()
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Задача успешно добавлена к методу")
                self.output_tasks_meth_table_edit()
                self.insert_new_lookbook_update()
            else:
                Dialogs.MessageInfo("Математическая задача уже привязана к методу")

    def push_edit_del_task_for_meth_pushButton_inf(self):
        id_task = self.edit_task_tableWidget.currentRow()
        if id_task == -1:
            Dialogs.MessageInfo("Необходимо выбрать математическую задачу")
        else:
            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            stmt = "SELECT * FROM del_method_task_area(" + str(self.Method.Id) + "," + str(
                self.list_task_area[id_task]) + ")"
            print(stmt)
            cursor.execute(stmt)
            self.UniskadConnection.commit()
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Задача успешно отвязана от метода")
                self.output_tasks_meth_table_edit()
                self.insert_new_lookbook_update()
            else:
                Dialogs.MessageInfo("Ошибка удаления связи")

    def push_edit_bind_to_task_pushButton_inf(self):
        name_task = self.edit_task_area_comboBox_inf.currentText()
        name_pract = self.edit_pract_task_comboBox_inf.currentText()

        if name_task == "" or name_pract == "":
            Dialogs.MessageInfo("Необходимо выбрать математическую и практическую задачи")
        else:
            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            stmt = "SELECT * FROM new_pract_task_area('" + name_task + "','" + name_pract + "')"
            print(stmt)
            cursor.execute(stmt)
            self.UniskadConnection.commit()
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Задачи успешно связаны")
                self.output_tasks_meth_table_edit()
            else:
                Dialogs.MessageInfo("Такая связь уже существует")

    def push_edit_del_bind_to_task_pushButton_inf(self):
        name_task = self.edit_task_area_comboBox_inf.currentText()
        name_pract = self.edit_pract_task_comboBox_inf.currentText()

        if name_task == "" or name_pract == "":
            Dialogs.MessageInfo("Необходимо выбрать математическую и практическую задачи")
        else:
            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            stmt = "SELECT * FROM del_pract_task_area('" + name_task + "','" + name_pract + "')"
            print(stmt)
            cursor.execute(stmt)
            self.UniskadConnection.commit()
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Математическая задача успешно отвязана от практической")
                self.output_tasks_meth_table_edit()
            else:
                Dialogs.MessageInfo("Ошибка удаления связи")

    def push_edit_bind_theorem_pushButton_inf(self):
        name_theor = self.edit_theorem_comboBox_inf.currentText()
        if name_theor == "":
            Dialogs.MessageInfo("Необходимо выбрать теорему")
        else:
            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            stmt = "SELECT * FROM new_method_theorem(" + str(self.Method.Id) + ",'" + str(name_theor) + "')"
            print(stmt)
            cursor.execute(stmt)
            self.UniskadConnection.commit()
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Теорема успешно добавлена к методу")
                self.Method.set_theorems()
                self.output_theorems_meth_table_edit()
                self.insert_new_lookbook_update()
            else:
                Dialogs.MessageInfo("Связь уже существует")

    def push_edit_del_theorem_pushButton_inf(self):
        id_theor = self.edit_theorems_tableWidget.currentRow()
        if id_theor == -1:
            Dialogs.MessageInfo("Необходимо выбрать теорему")
        else:
            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            stmt = "SELECT * FROM del_method_theorem(" + str(self.Method.Id) + "," + str(
                self.Method.ListTheorems[id_theor].Id) + ")"
            print(stmt)
            cursor.execute(stmt)
            self.UniskadConnection.commit()
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Теорема успешно отвязана от метода")
                self.Method.set_theorems()
                self.output_theorems_meth_table_edit()
                self.insert_new_lookbook_update()
            else:
                Dialogs.MessageInfo("Ошибка удаления связи")

    def push_edit_bind_constr_pushButton_inf(self):
        name_const = self.edit_constr_comboBox_inf.currentText()
        if name_const == "":
            Dialogs.MessageInfo("Необходимо выбрать ограничение")
        else:
            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            stmt = "SELECT * FROM new_method_constraint(" + str(self.Method.Id) + ",'" + str(
                name_const) + "')"
            print(stmt)
            cursor.execute(stmt)
            self.UniskadConnection.commit()
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Ограничение успешно добавлено к методу")
                self.Method.set_constraints()
                self.output_constr_meth_table_edit()
                self.insert_new_lookbook_update()
            else:
                Dialogs.MessageInfo("Связь уже существует")

    def push_edit_del_constr_pushButton_inf(self):
        id_const = self.edit_constr_tableWidget.currentRow()
        if id_const == -1:
            Dialogs.MessageInfo("Необходимо выбрать ограничение")
        else:
            if (self.UniskadConnection == None):
                Dialogs.MessageInfo("Нет соединения с БД")
                return  # Нет соединения с БД

            cursor = self.UniskadConnection.cursor()  # Получить курсор БД
            stmt = "SELECT * FROM del_method_constraint(" + str(self.Method.Id) + ",'" + str(
                self.Method.ListConstraint[id_const]) + "')"
            print(stmt)
            cursor.execute(stmt)
            self.UniskadConnection.commit()
            for row in cursor:
                r = row[0]

            if r != -2:
                Dialogs.MessageInfo("Ограничение успешно отвязано от метода")
                self.Method.set_constraints()
                self.output_constr_meth_table_edit()
                self.insert_new_lookbook_update()
            else:
                Dialogs.MessageInfo("Ошибка удаления связи")

    def insert_new_lookbook_update(self):
        date_entry = datetime.now().date()
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД

        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        stmt = "SELECT * FROM update_method_logbook_simp(" + str(self.Method.Id) + "," + str(
            self.sessionUser.Id) + ",'" + str(date_entry) + "')"
        print(stmt)
        cursor.execute(stmt)
        self.UniskadConnection.commit()

    def insert_new_lookbook_del(self):
        date_entry = datetime.now().date()
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД

        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        stmt = "SELECT * FROM del_method_logbook_simp(" + str(self.Method.Id) + "," + str(
            self.sessionUser.Id) + ",'" + str(date_entry) + "')"
        print(stmt)
        cursor.execute(stmt)
        self.UniskadConnection.commit()

    # ПРОСМОТР ИНФОРМАЦИИ
    def get_text_theorem_bd_table(self):
        id_row = self.info_theorems_tableWidget.currentRow()
        if id_row == -1:
            Dialogs.MessageInfo("Необходимо выбрать одину теорему")
        else:
            self.get_self_info_meth_file(self.name_file_theorem,
                                         self.Method.ListTheorems[id_row].Statement)

   # def closeEvent(self, a0: QtGui.QCloseEvent):
    #    self.close()
