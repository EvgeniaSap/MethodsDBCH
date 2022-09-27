# -*- coding: utf-8 -*-
# Модуль диалоговых окон
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox

# Сообщение: Фатальная ошибка. Продолжение выполнения невозможно
def MessageFatalError (ErrMessage):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(ErrMessage+"\nПродолжение выполнения программы невозможно.")
    msg.setWindowTitle("Фатальная ошибка")
    msg.setWindowIcon(QIcon('Images\GraphIcon.png'))
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
    sys.exit(1)

# Сообщение: Предупреждение. Только кнопка OK
def MessageWarning (WarnMessage):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(WarnMessage)
    msg.setWindowTitle("Предупреждение.")
    msg.setWindowIcon(QIcon('Images\GraphIcon.png'))
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()

# Сообщение: Информационное сообщение. Только кнопка ОК
def MessageInfo (InfoMessage):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(InfoMessage)
    msg.setWindowTitle("Информационное сообщение.")
    msg.setWindowIcon(QIcon('Images\GraphIcon.png'))
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()

# Сообщение: Вопрос. Только кнопки Да Нет
def MessageQuestionYesNo (QuestionMessage,Title="Запрос."):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setText(QuestionMessage)
    # msg.setInformativeText("This is additional information")
    msg.setWindowTitle(Title)
    msg.setWindowIcon(QIcon('Images\GraphIcon.png'))

    msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
    msg.buttons()[0].setText("Да")
    msg.buttons()[1].setText("Нет")
    tt = msg.exec_()
    if tt == QMessageBox.Yes:
        return True
    else:
        return False
