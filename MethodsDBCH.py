import AuthWindow as win
import MainWindow
import sys
import os
from PyQt5 import (QtWidgets)
import Config as Config

workDir = ""  # Рабочая папка
paramDir = ""  # Папка конфиг файлов и параметров
ParamFile = ""  # Файл параметров

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    workDir = os.path.abspath(os.path.dirname(sys.argv[0]))  # Папка запуска программы
    paramDir = workDir + "\\Params"
    ParamFile = paramDir + "\\BDConnectParams.prm"
    postgreSqlConfig = Config.UniskadPostgreSqlConfig(ParamFile)
    postgreSqlConfig.read()
    postgreSqlConfig.postgreSQlConnect()

    log_window = win.AuthWindow(application=app,UniskadConnection=postgreSqlConfig.PostgreSql_Connection)
    log_window.exec()
    if log_window.successAuth:
        print('good')
        main_window = MainWindow.MainWindow(application=app, sessionUser=log_window.sessionUser, UniskadConnection=postgreSqlConfig.PostgreSql_Connection)

    else:
        print('no good')


    sys.exit(app.exec_())