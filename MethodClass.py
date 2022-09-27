import Dialogs
import TheoremClass
import TaskAreaClass

class Method:
    def __init__(self,Id=None, Name="", NumbStages=None, ValMemory="", ValComplex="", IdAlgCl=None, IdComplexCl=None,Status=None,UniskadConnection=None,NameAlgCl="",NameComplexCl=""):
            self.Id = Id
            self.Name = Name
            self.NumbStages = NumbStages
            self.ValMemory = ValMemory
            self.ValComplex = ValComplex
            self.IdAlgCl = IdAlgCl
            self.IdComplexCl = IdComplexCl
            self.Status = Status
            self.DescriptionStages = ""
            self.SimpCode = ""
            self.NameAlgCl = NameAlgCl
            self.NameComplexCl = NameComplexCl
            self.ListTheorems = []
            self.ListConstraint = []
            self.ListTaskArea = []
            self.ListPractTask = []

            self.UniskadConnection = UniskadConnection

    def set_names_classes(self):
        # поиск в бд польз по логину и паролю
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД

        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        stmt = "SELECT * FROM get_alg_class_by_id(" + str(self.IdAlgCl) + ")"
        cursor.execute(stmt)
        for row in cursor:
            self.NameAlgCl = row[0]

        stmt = "SELECT * FROM get_complex_class_by_id(" + str(self.IdComplexCl) + ")"
        cursor.execute(stmt)
        for row in cursor:
            self.NameComplexCl = row[0]

    def set_self_values(self):
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД

        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        stmt = "SELECT * FROM get_methods_by_id(" + str(self.Id) + ")"
        cursor.execute(stmt)
        for row in cursor:
            self.Name = row[0]
            self.NumbStages = row[1]
            self.ValMemory = row[2]
            self.DescriptionStages = row[3]
            self.SimpCode = row[4]
            self.ValComplex = row[5]
            self.IdAlgCl = row[6]
            self.IdComplexCl = row[7]
            self.Status = row[8]

        self.set_constraints()
        self.set_names_classes()
        self.set_theorems()
        self.set_list_task()

    def set_constraints(self):
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД

        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        stmt = "SELECT * FROM get_constraint_by_id_meth(" + str(self.Id) + ")"
        cursor.execute(stmt)
        self.ListConstraint.clear()
        for row in cursor:
            self.ListConstraint.append(row[0])

    def set_theorems(self):
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД

        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        stmt = "SELECT * FROM get_theorems_by_id_meth(" + str(self.Id) + ")"
        cursor.execute(stmt)
        self.ListTheorems.clear()
        for row in cursor:
            self.ListTheorems.append(TheoremClass.Theorem(Id=row[0], Name=row[1], Statement=row[2], Resource=row[3]))

    def set_list_task(self):
        if (self.UniskadConnection == None):
            Dialogs.MessageInfo("Нет соединения с БД")
            return  # Нет соединения с БД

        cursor = self.UniskadConnection.cursor()  # Получить курсор БД
        stmt = "SELECT * FROM get_methods_by_id(" + str(self.Id) + ")"
        cursor.execute(stmt)
        for row in cursor:
            self.set_list_task_area(TaskAreaClass.TaskArea(IdType=row[0], NameType=row[1],IdTaskArea=row[2],NameTaskArea=row[3]))
            self.set_list_prack_task(TaskAreaClass.PrackicTask(IdAppArea=row[4],NameAppArea=row[5],IdPractTask=row[6],NamePractTask=row[7]))

    def set_list_prack_task(self, elem):
        if elem in self.ListPractTask:
            return
        else:
            self.ListPractTask.append(elem)

    def set_list_task_area(self, elem):
        if elem in self.ListTaskArea:
            return
        else:
            self.ListTaskArea.append(elem)





