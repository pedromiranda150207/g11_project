# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:01:30 2026

@author: vasco
"""
import sys
import os

diretorio_projeto = os.path.dirname(os.path.abspath(__file__))
diretorio_classes = os.path.join(diretorio_projeto, "classes")

if diretorio_classes not in sys.path:
    sys.path.append(diretorio_classes)

from company import Company
from order import Order
from warehouse import Warehouse
from vehicle import Vehicle

c1 = Company(103, 'Company 103', '2022-01-03')
c2 = Company(246, 'Company 246', '2022-01-03')
c3 = Company(66, 'Company 66', '2022-01-03')
c4 = Company(438, 'Company 438', '2022-01-03')
c5 = Company(302, 'Company 302', '2022-01-03')

w1 = Warehouse(58, 'Location 58', 'Automated Warehouse')
w2 = Warehouse(436, 'Location 436', 'Automated Warehouse')
w3 = Warehouse(20, 'Location 20', 'Automated Warehouse')
w4 = Warehouse(588, 'Location 588', 'Automated Warehouse')
w5 = Warehouse(936, 'Location 936', 'Automated Warehouse')

c1 = Company(55, 'Tran LLC', '2022-01-03')
print('Company:')
print('Id:', c1.id)
print('Name:', c1.name)
print('Creation date:', c1.creation_date)
print('Age of the company:', c1.age_company(), 'years')
print(c1.order_count())
print(';')

o1 = Order(1, 4797, '2023-08-01', 103, 58)
o2 = Order(2, 1585, '2024-10-09', 246, 436)
o3 = Order(3, 1010, '2023-10-29', 66, 20)
o4 = Order(4, 1240, '2025-04-06', 438, 588)
o5 = Order(5, 1286, '2021-07-20', 302, 936)

print('Order:')
print('Id:', o1.id)
print('Cost:', o1.cost)
print('Order date:', o1.order_date)
print('Company id:', o1.company_id)
print('Warehouse id:', o1.warehouse_id)
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
print('Company_id:', v1.company_id)
print(';')

print('Orders sorted by cost:')
Order.sort('cost')
for id in Order.lst:
    print(Order.obj[id])