import datetime as dt
from company import Company
from warehouse import Warehouse
from gclass import Gclass


class Order(Gclass):
    obj = {}
    lst = []
    pos = 0
    sortkey = ''

    att = ['_id', '_cost', '_order_date', '_company_id', '_warehouse_id']
    header = 'Order'
    des = ['Id', 'Cost', 'Order Date', 'Company Id', 'Warehouse Id']

    def __init__(self, id, cost, order_date, company_id, warehouse_id):
        super().__init__()
        company_id = int(company_id)
        if company_id not in Company.lst:
            raise ValueError(f'Company {company_id} not found')
        warehouse_id = int(warehouse_id)
        if warehouse_id not in Warehouse.lst:
            raise ValueError(f'Warehouse {warehouse_id} not found')
        id = Order.get_id(id)
        self._id = id
        self._cost = int(cost)
        self._order_date = dt.date.fromisoformat(str(order_date))
        self._company_id = company_id
        self._warehouse_id = warehouse_id
        Order.obj[id] = self
        Order.lst.append(id)

    @property
    def id(self):
        return self._id

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, cost):
        self._cost = int(cost)

    @property
    def order_date(self):
        return self._order_date

    @order_date.setter
    def order_date(self, order_date):
        self._order_date = order_date

    @property
    def company_id(self):
        return self._company_id

    @property
    def warehouse_id(self):
        return self._warehouse_id