# run the program
# menu_loop function
# add_product function (a)
# view_product by id function (v)
# backup function (b)
# OrderedDict for menu_loop

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
        welcome = 'PRODUCT INVENTORY MANAGEMENT'
        print(welcome)
        print('-'*len(welcome))
        print('Select an option below.')
        print('Enter "q" to quit.\n')
        for key, value in menu.items():
            print(f'{key}) {value.__doc__}')
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()
        else:
            print('''\n***** INPUT ERROR *****
            \rThat is not a valid option.
            \rPlease try again.''')
            time.sleep(2)


def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        print('''
        \n**********PRICE ERROR**********
        \rEnter price as number without currency symbol.
        \rEx: 10.99
        \rPress enter to try again.''')
        return
    else:
        return int(price_float * 100)


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        date = datetime.date(year,month,day)
    except ValueError:
        print('''
        \n**********DATE ERROR**********
        \rEnter Date as Month/Day/Year.
        \rEx: 4/26/2021.
        \rPress enter to try again.''')
        return
    else:
        return date


def add_csv():
    with open('inventory.csv') as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if in_db == None:
                product_name = row[0]
                product_price = int(float(row[1][1:])*100)
                product_quantity = int(row[2])
                date_updated = clean_date(row[3])
                new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated)
                session.add(new_product)
            elif in_db.date_updated < clean_date(row[3]):
                in_db.product_price = int(float(row[1][1:])*100)
                in_db.product_quantity = int(row[2])
                in_db.date_updated = clean_date(row[3])
        session.commit()


def view_product():
    """VIEW ENTRY BY ID"""
    pass


def add_product():
    """ADD PRODUCT"""
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
    add_csv()



