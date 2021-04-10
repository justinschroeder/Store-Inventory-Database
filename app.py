# run the program
# menu_loop function
# add_product function (a)
# view_product by id function (v)
# backup function (b)
# OrderedDict for menu_loop

from sqlalchemy.sql.coercions import expect_col_expression_collection
from sqlalchemy.sql.expression import column
from models import (Base, session, Product, engine)
from collections import OrderedDict
import csv
import datetime
import time
import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    """SHOW MENU"""
    choice = None

    while choice != 'q':
        clear()
        print('Enter "q" to quit.')
        for key, value in menu.items():
            print(f'{key}) {value.__doc__}')
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()
        else:
            print('\nThat is not a valid option.\nPlease try again.')
            time.sleep(2)


def view_product():
    """VIEW ENTRY BY ID"""
    pass


def add_product():
    """ADD PRODUCT TO INVENTORY"""
    pass


def backup():
    """BACKUP INVENTORY"""
    pass


menu = OrderedDict([
    ('a', add_product),
    ('v', view_product),
    ('b', backup),
])

if __name__== '__main__':
    Base.metadata.create_all(engine)
    menu_loop()
