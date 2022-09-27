import Dialogs


class TaskArea:
    def __init__(self,IdType=None, NameType="",IdTaskArea=None,NameTaskArea="",UniskadConnection=None):
            self.IdType = IdType
            self.NameType = NameType
            self.IdTaskArea = IdTaskArea
            self.NameTaskArea = NameTaskArea
            self.ListTaskArea = []
            self.ListPractTask = []
            self.UniskadConnection = UniskadConnection

    def set_list_task(self, idmeth):
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД

        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        stmt = "SELECT * FROM get_methods_by_id(" + str(idmeth) + ")"
        cursor.execute(stmt)
        for row in cursor:
            self.IdType = row[0]
            self.NameType = row[1]
            self.ListTaskArea.append(row[3])
            self.set_list_prack_task(PrackicTask(IdAppArea=row[4],NameAppArea=row[5],IdPractTask=row[6],NamePractTask=row[7]))


    def set_list_prack_task(self, elem):
        if elem in self.ListPractTask:
            return
        else:
            self.ListPractTask.append(elem)


class PrackicTask:
    def __init__(self,IdAppArea=None, NameAppArea="",IdPractTask=None,NamePractTask=""):
            self.IdAppArea = IdAppArea
            self.NameAppArea = NameAppArea
            self.IdPractTask = IdPractTask
            self.NamePractTask = NamePractTask

