# run the program
# menu_loop function
# add_product function (a)
# view_product by id function (v)
# backup function (b)
# OrderedDict for menu_loop

from sqlalchemy.sql.coercions import expect_col_expression_collection
from sqlalchemy.sql.expression import column
from models import (Base, session, Product, engine)
import csv
import datetime
import time
from collections import OrderedDict


if __name__== '__main__':
    Base.metadata.create_all(engine)
    