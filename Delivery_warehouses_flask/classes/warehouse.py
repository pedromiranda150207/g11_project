from classes.gclass import Gclass


class Warehouse(Gclass):
    obj = {}
    lst = []
    pos = 0
    sortkey = ''

    att = ['_id', '_designation', '_type']
    header = 'Warehouses'
    des = ['Id', 'Designation', 'Type']

    def __init__(self, id, designation, type_):
        super().__init__()
        id = Warehouse.get_id(id)
        self._id = int(id) if id is not None and str(id).strip() != 'None' else 0
        self._designation = designation
        self._type = type_
        Warehouse.obj[self._id] = self
        Warehouse.lst.append(self._id)

    @property
    def id(self):
        return self._id

    @property
    def designation(self):
        return self._designation

    @designation.setter
    def designation(self, designation):
        self._designation = designation

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type_):
        self._type = type_

