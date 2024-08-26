class Vacancies:
    def __init__(self, id_, salary, name):
        self.id_ = id_
        self.salary = salary
        self.name = name

    @classmethod
    def creat(cls, data_vac):
        list_vacanci = []
        for vac in data_vac:
            id_ = vac["id"]
            salary = vac["salary"]
            name = vac["name"]
            obg = cls(id_, salary, name)
            list_vacanci.append(obg)
        return list_vacanci

    def __str__(self):
        return f"Id {self.id_}, salary{self.salary}, name{self.name}."