import datetime as dt
from classes.gclass import Gclass


class Company(Gclass):
    obj = {}
    lst = []
    pos = 0
    sortkey = ''

    att = ['_id', '_name', '_creation_date']
    header = 'Companies'
    des = ['Id','Name', 'Creation date']

    def __init__(self, id, name, creation_date, *args):
        super().__init__()
        self._id = int(id)
        self._name = name
        Company.obj[self._id] = self
        Company.lst.append(self._id)
        if isinstance(creation_date, str):
            self._creation_date = dt.datetime.strptime(creation_date[:10], '%d/%m/%Y').date()
        else:
            self._creation_date = creation_date
            
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        if isinstance(creation_date, str):
            creation_date = dt.datetime.strptime(creation_date, '%Y-%m-%d').date()
        self._creation_date = creation_date

    def age_company(self):
        today = dt.date.today()
        age = today.year - self._creation_date.year
        had_birthday = (today.month, today.day) >= (self._creation_date.month, self._creation_date.day)
        if not had_birthday:
            age -= 1
        return age

    def order_count(self):
        from order import Order
        return sum(1 for order in Order.obj.values() if order.company_id == self._id)
