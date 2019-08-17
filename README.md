# storeinventory

StoreInventory is a simple product storage app. Products can be bulk loaded into a database via a csv file. Users can enter 
chacarteristics of a product (name, price, quantity) and then store the product in a database. Users can retrieve single 
products or a list of all products from the database. Users can also back up the database to a backup_csv.csv file.

<br/>

# requirements

The following requirements can be accessed via requirements.txt

* peewee==3.9.6
* prettytable==0.7.2


<br/>

# installation

1. cd into your directory of projects (or wherever you prefer to keep your clones)
2. git clone ```https://github.com/Marksparkyryan/storeinventory.git``` to clone the app
3. ```virtualenv .venv``` to create your virtual environment
4. ```source .venv/bin/activate``` to activate the virtual environment
5. ```pip install -r storeinventory/requirements.txt``` to install app requirements
6. cd into the storeinventory directory
7. ```python app.py``` to run the app!


<br/>

# inventory.csv

storeinventory ships with a pre-filled inventory.csv file. If you want to bulk load your own products, replace this file.
Don't forget to replace/include headers in your csv file. 

<br/>

# screenshots

<img width="637" alt="Screen Shot 2019-08-17 at 6 33 57 PM" src="https://user-images.githubusercontent.com/45185244/63217960-b9630f00-c11d-11e9-9a43-0d359eecf1e3.png">

<br/>

<img width="639" alt="Screen Shot 2019-08-17 at 6 36 56 PM" src="https://user-images.githubusercontent.com/45185244/63217971-0c3cc680-c11e-11e9-9636-080ccde507f8.png">

<br/>

<img width="638" alt="Screen Shot 2019-08-17 at 6 39 05 PM" src="https://user-images.githubusercontent.com/45185244/63217997-5b82f700-c11e-11e9-899e-14b2ee08245d.png">

<br/>

# credits

Treehouse Techdegree Project 4
