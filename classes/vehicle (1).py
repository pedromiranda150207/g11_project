from gclass import Gclass
from company import Company

class Vehicle(Gclass):
    obj = {}
    lst = []
    pos = 0
    sortkey = ''

    att = ['_id', '_comment', '_company_id']
    header = 'Vehicle'
    des = ['Id', 'Comment', 'Company Id']

    def __init__(self, id, comment, company_id):
        super().__init__()
        company_id = int(company_id)
        if company_id not in Company.lst:
            raise ValueError(f'Company {company_id} not found')
        id = Vehicle.get_id(id)
        self._id = id
        self._comment = comment
        self._company_id = company_id
        Vehicle.obj[id] = self
        Vehicle.lst.append(id)

    @property
    def id(self):
        return self._id

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        self._comment = comment

    @property
    def company_id(self):
        return self._company_id
