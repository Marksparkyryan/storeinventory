from collections import OrderedDict
import csv
from datetime import datetime as dt
import os
from peewee import *
from prettytable import PrettyTable
import re


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
        table = PrettyTable(["Product ID", f"{query.product_id}"])
        table.add_row(["Product Name", query.product_name])
        table.add_row(["Product Price", "$%0.2f" % price])
        table.add_row(["Product Quantity", query.product_quantity])
        table.add_row(["Date Updated", date])
        print("")
        print(table)
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
        Product.create(
            product_name=context["product_name"],
            product_price=context["product_price"],
            product_quantity=context["product_quantity"]
        )
        print("Success: product added to database.")
    except ValueError:
        print("Error: One or more fields were empty/incorrect data type.")
    except IntegrityError:
        print(
            f"""Error: Product "{context["product_name"]}" already exists."""
        )


def list_view():
    """List all products in database"""
    os.system("cls" if os.system.__name__ == "nt" else "clear")
    query = Product.select().order_by(Product.product_name)
    print("Store Inventory - Product List")
    print("------------------------------")
    table = PrettyTable(["ID", "Name", "Price", "Quantity", "Date Updated"])
    for prod in query:
        price = float(prod.product_price) / float(100)
        price = "$%0.2f" % price
        date = prod.date_updated.strftime("%B %-d, %Y")
        table.add_row([prod.product_id,
                       prod.product_name,
                       price,
                       prod.product_quantity,
                       date])
    print("")
    print(table)


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
    while True:
        os.system("cls" if os.system.__name__ == "nt" else "clear")
        print("Store Inventory - Main Menu")
        print("---------------------------")
        print("q to Quit")
        for key, value in MENU.items():
            print(f"{key} to {value.__doc__}")
        choice = input("> ").lower().strip()
        if choice == "q":
            os.system("cls" if os.system.__name__ == "nt" else "clear")
            print("Goodbye!")
            print("")
            quit()
        if choice in MENU:
            MENU[choice]()
            input("\nPress enter to continue ")
        else:
            input("\nThat's not a choice! Press enter to try again")


def csv_reader():
    """Open csv file, read it, then push it as a dictionary to a cleaner 
    function"""
    with open("inventory.csv", newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        os.system("cls" if os.system.__name__ == "nt" else "clear")
        print("Store Inventory - Loading Data")
        print("------------------------------")
        for row in csv_reader:
            dict_cleaner(**row)


def dict_cleaner(product_name, product_price, product_quantity, date_updated):
    """Take in dictionary version of each row in csv file and 
    clean data."""
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
        print(f"""Error: product "{product_name}" rejected"""
              """ due to invalid data type""")


def dict_packer(**kwargs):
    """Take in cleaned row from cleaner function and re-pack as 
    dictionary and append to product list"""
    PRODUCT_LIST.append(kwargs)


def csv_to_product_model(PRODUCT_LIST):
    """Add each dictionary row in product list and push into object 
    model Product"""
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
