from enum import Enum


class DisciplineStatus(Enum):
    nothing = 1
    cursando = 2
    reprovado = 3
    passado = 4


class Discipline:
    list_objects = {}

    @staticmethod
    def get_object(name):
        return Discipline.list_objects[name]

    def __init__(self, name, semester):
        self.name = name
        self.semester = semester
        self.status = DisciplineStatus.nothing
        Discipline.list_objects[name] = self

    def set_status(self, status):
        self.status = status

    def __str__(self):
        return self.name
