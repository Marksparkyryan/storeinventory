from collections import OrderedDict
import csv
from datetime import datetime
from peewee import * 
import re


db = SqliteDatabase("inventory.db")
PRODUCT_LIST = []


class Product(Model):
    product_id = AutoField()
    product_name = CharField(max_length=255) 
    product_price = IntegerField(null=False) 
    product_quantity = IntegerField() 
    date_updated = DateField(default=datetime.now())

    class Meta:
        database = db


def detail_view():
    """View product details"""
        


def add_product():
    """Add a new product"""
    context = {}
    for field in Product._meta.fields:
        if field in ["product_id", "date_updated"]:
            continue
        field_value = input(f"enter {field}: ")    
        context.update({field: field_value})
    new = Product.create(**context)
    new.save()


def list_view():
    """List all products in database"""
    query = Product.select().order_by(Product.product_name)
    for prod in query:
        print(prod.product_name,
        prod.product_price,
        prod.product_quantity,
        prod.date_updated)


def make_backup():
    """Make a backup of database"""
    pass



MENU = OrderedDict([
    ("v", detail_view),
    ("a", add_product),
    ("l", list_view),
    ("b", make_backup)
])


def menu_loop():
    choice = None
    while choice != "q":
        print("q to quit")
        for key, value in MENU.items():
            print(f"{key} to {value.__doc__}")
        choice = input("> ").lower().strip()

        if choice in MENU:
            MENU[choice]()    


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
    PRODUCT_LIST.append(kwargs)


def csv_to_product_model(PRODUCT_LIST):
    with db.atomic():
        Product.insert_many(PRODUCT_LIST).execute()
 

# csv_reader()   
# csv_to_product_model(PRODUCT_LIST)
# query = Product.select().order_by(Product.product_name)
# for prod in query:
#     print(prod.product_name,
#           prod.product_price,
#           prod.product_quantity,
#           prod.date_updated)


if __name__ == "__main__":
    db.connect()
    db.create_tables([Product], safe=True)
    csv_reader()   
    csv_to_product_model(PRODUCT_LIST)
    menu_loop()
    db.close

