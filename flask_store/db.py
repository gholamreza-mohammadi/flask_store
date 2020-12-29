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
        db.products.insert_one({
            "image_link": data['product_image_link'],
            "commodity_name": data['product_name'],
            "category": data['product_category'],
            "description": data['product_description']
        })


def delete_product(data):
    db.products.delete_one({"_id": ObjectId(data['product_id'])})


def edit_product(data):
    db.products.update_one(
        {"_id": ObjectId(data['product_id'])},
        {'$set': {
            "image_link": data['product_image_link'],
            'commodity_name': data['product_name'],
            'category': data['product_category'],
            "description": data['product_description']
        }
        })


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


def add_inventory(data):
    exist = db.inventories.find({
        'commodity_name': data['inventory_product'],
        'repository_name': data['inventory_repository']})
    if not list(exist):
        db.inventories.insert_one({
            "commodity_name": data['inventory_product'],
            "price": data['inventory_price'],
            "quantity": data['inventory_quantity'],
            "repository_name": data['inventory_repository'],
            "create_time": datetime.utcnow()
        })


def delete_inventory(data):
    db.inventories.delete_one({"_id": ObjectId(data['inventory_id'])})


def edit_inventory(data):
    db.inventories.update_one(
        {"_id": ObjectId(data['inventory_id'])},
        {'$set': {
            "commodity_name": data['inventory_product'],
            "price": data['inventory_price'],
            "quantity": data['inventory_quantity'],
            "repository_name": data['inventory_repository'],
            "create_time": datetime.utcnow()
        }})


# =============================repositories=============================
def get_orders():
    orders = list(db.orders.find())
    for order in orders:
        order['_id'] = str(order['_id'])
    return orders
