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
        choice = input('\nAction: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()
        elif choice =='q':
            print('\nExiting...')
            time.sleep(1.5)
            clear()
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
        product_list = []
        next(data)
        product_id = 0
        for row in data:
            product_id = product_id + 1
            product_name = row[0]
            product_quantity = int(row[2])
            product_price = int(float(row[1][1:])*100)
            date_updated = clean_date(row[3])
            product_dict = {'Product ID':product_id, 'Product Name':product_name, 'Product Quantity':product_quantity, 'Price':product_price, 'Date Updated':date_updated}
            product_list.append(product_dict)
        for product in product_list:
            in_db = session.query(Product).filter(Product.product_name==product['Product Name']).one_or_none()
            if in_db == None:
                new_product = Product(product_id=product['Product ID'], product_name=product['Product Name'], product_price=product['Price'], product_quantity=product['Product Quantity'], date_updated=product['Date Updated'])
                session.add(new_product)
            elif in_db.date_updated < product['Date Updated']:
                in_db.product_price = product['Price']
                in_db.product_quantity = product['Product Quantity']
                in_db.date_updated = product['Date Updated']
        session.commit()


def view_product():
    """VIEW PRODUCT BY ID"""
    choice = None

    while choice != 'q':
        print('''VIEW PRODUCT BY ID
        \r------------------------
        \rSelect and option below.
        \rEnter 'q' to return to main menu.
        \n1) View Product by ID
        \r2) View all Products''')
        choice = input('\nAction: ').lower().strip()
        if choice == '1':
            ids = []
            for product in session.query(Product):
                ids.append(product.product_id)
            print(f'Product IDs: {ids}')
            loop = True
            while loop:
                id = input('\nEnter Product ID: ')
                product = session.query(Product).filter(Product.product_id == id).one_or_none()
                if product != None:
                    print(f'''\nProduct Name: {product.product_name}
                    \rProduct Quantity: {product.product_quantity}
                    \rPrice: ${float(product.product_price/100)}
                    \rDate Last Updated: {product.date_updated}''')
                    loop_choice = input("\nPress ENTER to view another Product.\nEnter 'q' to return.")
                    if loop_choice != 'q':
                        loop = True
                    else:
                        loop = False
                        clear()
                elif id == 'q':
                    loop = False
                    time.sleep(.5)
                    clear()
                else:
                    print('''\n***** ID ERROR *****
                    \rThat is not a valid Product ID.
                    \rPlease try again.''')        
        elif choice == '2':
            products = session.query(Product).all()
            for product in products:
                print(f'''\nID: {product.product_id}
                \rProduct Name: {product.product_name}
                \rProduct Quantity: {product.product_quantity}
                \rPrice: ${float(product.product_price/100)}
                \rDate Last Updated: {product.date_updated}''')
            input('\nPress ENTER to return to menu.')
            clear()
        elif choice == 'q':
            time.sleep(.5)
        else:
            print('''\n***** INPUT ERROR *****
            \rThat is not a valid option.
            \rPlease try again.''')
            time.sleep(1.5)
            clear()


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
    menu_loop()



