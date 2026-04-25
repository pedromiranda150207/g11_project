# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:01:30 2026

@author: vasco
"""
import sys
import os

diretorio_projeto = os.path.dirname(os.path.abspath(__file__))
diretorio_raiz = os.path.dirname(diretorio_projeto)

if diretorio_raiz not in sys.path:
    sys.path.append(diretorio_raiz)

from company import Company
from order import Order
from warehouse import Warehouse
from vehicle import Vehicle

c1 = Company(55, 'Tran LLC', '2022-01-03')
print('Company:')
print('Id:', c1.id)
print('Name:', c1.name)
print('Creation date:', c1.creation_date)
print('Age of the company:', c1.age_company(), 'years')
print(c1.order_count())
print(';')

o1 = Order(10, 500, '2024-08-23', 55)
o2 = Order(2, 600, '2023-06-12', 55)
o3 = Order(3, 400, '2025-10-18', 55)
o4 = Order(4, 700, '2023-03-31', 55)
o5 = Order(5, 300, '2024-06-15', 55)

print('Order:')
print('Id:', o1.id)
print('Cost:', o1.cost)
print('Order date:', o1.order_date)
print('Company id:', o1.company_id)
print('Order count:', c1.order_count())
print(';')

w1 = Warehouse(55, 'New York', 'Automated Warehouse')
print('Warehouse:')
print('Id:', w1.id)
print('Designation:', w1.designation)
print('Type:', w1.type)
print(';')

v1 = Vehicle(2, 'ok', 55)
print('Vehicle:')
print('Id:', v1.id)
print('Comment:', v1.comment)
print(';')

print('Orders sorted by cost:')
Order.sort('cost')
for id in Order.lst:
    print(Order.obj[id])