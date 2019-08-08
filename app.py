from collections import OrderedDict
import csv
from datetime import datetime as dt
import os
from peewee import *
import re
import time


db = SqliteDatabase("inventory.db")
PRODUCT_LIST = []


class Product(Model):
    product_id = AutoField()
    product_name = CharField(max_length=255,
                             verbose_name="product name",
                             unique=True)
    product_price = IntegerField(null=False, verbose_name="product price")
    product_quantity = IntegerField(verbose_name="product quantity")
    date_updated = DateField(default=dt.now())

    class Meta:
        database = db


def detail_view():
    """View product detail by id"""
    os.system("cls" if os.system.__name__ == "nt" else "clear")
    print("Store Inventory - View Product")
    print("------------------------------")
    id = input("Enter id of product: ")
    try:
        query = Product.select().where(Product.product_id == id).get()
        price = query.product_price / 100
        date = query.date_updated.strftime("%B %-d, %Y")
        print(f"""
        Product Name: {query.product_name}
        Price: ${price}
        Quantity: {query.product_quantity}
        Date Updated: {date}
        """)
    except DoesNotExist:
        print(f"\nProduct with id={id} does not exist.")
    except ValueError:
        print("\nError: invalid entry.")


def add_product():
    """Add a new product"""
    context = {}
    os.system("cls" if os.system.__name__ == "nt" else "clear")
    print("Store Inventory - Add Product")
    print("-----------------------------")
    for key, value in Product._meta.fields.items():
        if key in ["product_id", "date_updated"]:
            continue
        field_value = input(f"enter {value.verbose_name}: ")
        context.update({key: field_value})
    print("")
    try:
        context["product_price"] = int(
            re.sub(r"[^\d]", "", context["product_price"]))
        product, created = Product.get_or_create(
            product_name=context["product_name"],
            product_price=context["product_price"],
            product_quantity=context["product_quantity"]
        )
        if not created:
            raise IntegrityError
        if created:
            print("Success: product added to database.")
    except ValueError:
        print("Error: One or more fields were incorrect data type.")
    except IntegrityError:
        print(f"""Error: Product "{product.product_name}" already exists.""")


def list_view():
    """List all products in database"""
    os.system("cls" if os.system.__name__ == "nt" else "clear")
    query = Product.select().order_by(Product.product_name)
    print("Store Inventory - Product List")
    print("------------------------------")
    for prod in query:
        print(prod.product_name,
              prod.product_price,
              prod.product_quantity,
              prod.date_updated)


def make_backup():
    """Make a backup of database"""
    backed_up = 0
    with open("inventory_backup.csv", "w", newline="") as csvfile:
        fieldnames = [
            "product_name",
            "product_price",
            "product_quantity",
            "date_updated"
        ]
        productwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        query = Product.select()
        productwriter.writeheader()
        for prod in query:
            productwriter.writerow({
                "product_name": prod.product_name,
                "product_price": prod.product_price,
                "product_quantity": prod.product_quantity,
                "date_updated": prod.date_updated
            })
            backed_up += 1
        print(
            f"\nSuccess: {backed_up} products backed up to inventory_backup.csv")


MENU = OrderedDict([
    ("v", detail_view),
    ("a", add_product),
    ("l", list_view),
    ("b", make_backup)
])


def menu_loop():
    choice = None
    while choice != "q":
        os.system("cls" if os.system.__name__ == "nt" else "clear")
        print("Store Inventory - Main Menu")
        print("---------------------------")
        print("q to Quit")
        for key, value in MENU.items():
            print(f"{key} to {value.__doc__}")
        choice = input("> ").lower().strip()

        if choice in MENU:
            MENU[choice]()
            print("")
            input("Press enter to continue ")


def csv_reader():
    with open("inventory.csv", newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        os.system("cls" if os.system.__name__ == "nt" else "clear")
        print("Store Inventory - Loading Data")
        print("------------------------------")
        for row in csv_reader:
            dict_cleaner(**row)


def dict_cleaner(product_name, product_price, product_quantity, date_updated):
    try:
        product_quantity = int(product_quantity)
        price = re.findall(r"\d", product_price)
        product_price = int("".join(price))
        date_updated = dt.strptime(date_updated, "%m/%d/%Y").date()

        dict_packer(product_name=product_name,
                    product_price=product_price,
                    product_quantity=product_quantity,
                    date_updated=date_updated)
    except ValueError:
        print(
            f"""Error: product "{product_name}" rejected due to invalid data type""")


def dict_packer(**kwargs):
    PRODUCT_LIST.append(kwargs)


def csv_to_product_model(PRODUCT_LIST):
    successful = 0
    exists = 0
    for product in PRODUCT_LIST:
        try:
            Product.create(**product)
            successful += 1
        except ValueError:
            invalid += 1
        except IntegrityError:
            exists += 1
    print(f"""
{exists} product(s) skipped, already exists in database
{successful} product(s) added successfully
    """)
    input("press enter to continue")


if __name__ == "__main__":
    db.connect()
    db.create_tables([Product], safe=True)
    csv_reader()
    csv_to_product_model(PRODUCT_LIST)
    menu_loop()
    db.close
