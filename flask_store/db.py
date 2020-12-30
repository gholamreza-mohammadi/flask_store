from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from flask import current_app

client = MongoClient('localhost', 27017)
db = client.store


# =============================products=============================
def get_products():
    products = list(db.products.find())
    for product in products:
        product['_id'] = str(product['_id'])
    return products


def add_product(data):
    if not (list(db.products.find({"commodity_name": data['product_name']}))):
        img_link = data['product_image_link']
        if not img_link:
            img_link = "https://appiranie.websites.co.in/e-store/img/defaults/product-default.png"
        db.products.insert_one({
            "image_link": img_link,
            "commodity_name": data['product_name'],
            "category": data['product_category'],
            "description": data['product_description']
        })


def delete_product(data):
    db.products.delete_one({"_id": ObjectId(data['product_id'])})


def edit_product(data):
    img_link = data['product_image_link']
    if not img_link:
        img_link = "https://appiranie.websites.co.in/e-store/img/defaults/product-default.png"
    last_name = list(db.products.find({"_id": ObjectId(data['product_id'])},{'commodity_name':1,'_id':0}))[0]['commodity_name']
    db.products.update_one(
        {"_id": ObjectId(data['product_id'])},
        {'$set': {
            "image_link": img_link,
            'commodity_name': data['product_name'],
            'category': data['product_category'],
            "description": data['product_description']
        }
        })
    update_inventory(data,img_link,last_name)


# =============================repositories=============================

def get_repositories():
    repositories = list(db.repositories.find())
    for repository in repositories:
        repository['_id'] = str(repository['_id'])
    return repositories


def add_repositories(data):
    if not (list(db.repositories.find({"repository_name": data['repository_name']}))):
        db.repositories.insert_one({
            "repository_name": data['repository_name']
        })


def delete_repositories(data):
    db.repositories.delete_one({"_id": ObjectId(data['repository_id'])})


def edit_repository(data):
    db.repositories.update_one({"_id": ObjectId(data['repository_id'])},
                               {'$set': {'repository_name': data['repository_name']}})


# =============================repositories=============================
def get_inventories():
    inventories = list(db.inventories.find())
    for inventory in inventories:
        inventory['_id'] = str(inventory['_id'])
    return inventories


def get_attr_product(product):
    return list(db.products.find(
        {"commodity_name": product},
        {'_id': 0, 'category': 1, 'image_link': 1,'description':1}))[0]


def add_inventory(data):
    exist = db.inventories.find({
        'commodity_name': data['inventory_product'],
        'repository_name': data['inventory_repository']})
    if not list(exist):
        product = data['inventory_product']
        db.inventories.insert_one({
            "commodity_name": product,
            "category": get_attr_product(product)["category"],
            "price": data['inventory_price'],
            "quantity": data['inventory_quantity'],
            "repository_name": data['inventory_repository'],
            "image_link": get_attr_product(product)["image_link"],
            "description": get_attr_product(product)["description"],
            "create_time": datetime.utcnow()
        })


def delete_inventory(data):
    db.inventories.delete_one({"_id": ObjectId(data['inventory_id'])})


def edit_inventory(data):
    product = data['inventory_product']
    db.inventories.update_one(
        {"_id": ObjectId(data['inventory_id'])},
        {'$set': {
            "commodity_name": product,
            "category": get_attr_product(product)["category"],
            "price": data['inventory_price'],
            "quantity": data['inventory_quantity'],
            "repository_name": data['inventory_repository'],
            "image_link": get_attr_product(product)["image_link"],
            "create_time": datetime.utcnow()
        }})

def update_inventory(data,img_link,last_name):
    id = list(db.inventories.find({'commodity_name':last_name}))[0]['_id']
    db.inventories.update_one(
        {"_id": ObjectId(id)},
        {'$set': {
            "image_link":img_link,
            "commodity_name": data['product_name'],
            "category": data['product_category'],
            "description": data["product_description"]
        }})

# =============================repositories=============================
def get_orders():
    orders = list(db.orders.find())
    for order in orders:
        order['_id'] = str(order['_id'])
    return orders
