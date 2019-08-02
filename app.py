import csv
from datetime import datetime
from peewee import *
import re

db = peewee.SqliteDatabase("inventory.db")

class Product(Model):
    product_id = IntegerField(primary_key=True)
    product_name = CharField() 
    product_price = 
    product_quantity = 
    date_updated = 

    class Meta:
        database = db




product_list = []

def csv_reader():
    with open("inventory.csv", newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            dict_cleaner(**row)


def dict_cleaner(product_name, product_price, product_quantity, date_updated):
    product_quantity = int(product_quantity)
    price = re.findall(r"\d", product_price)
    product_price = int("".join(price))
    date_updated = datetime.strptime(date_updated, "%m/%d/%Y").date()

    dict_packer(product_name=product_name, 
                product_price=product_price, 
                product_quantity=product_quantity, 
                date_updated=date_updated)


def dict_packer(**kwargs):
    product_list.append(kwargs)


csv_reader()   
print(product_list)

#change
