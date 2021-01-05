from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from flask import current_app, url_for

client = MongoClient('localhost', 27017)
db = client.store


# =============================products=============================
def get_product(product_id):
    return db.products.find_one({"_id": ObjectId(product_id)})


def get_products():
    products = list(db.products.find())
    for product in products:
        product['_id'] = str(product['_id'])
    return products


def add_product(data):
    if not db.products.find_one({"commodity_name": data['product_name']}):
        img_link = data['product_image_link']
        if not img_link:
            img_link = url_for('static', filename='assets/images/product-default.png')
        db.products.insert_one({
            "image_link": img_link,
            "commodity_name": data['product_name'],
            "category": data['product_category'],
            "description": data['product_description']
        })


def delete_product(data):
    db.products.delete_one({"_id": ObjectId(data['product_id'])})
    db.inventories.delete_many({'commodity_id': data['product_id']})


def edit_product(data):
    img_link = data['product_image_link']
    if not img_link:
        img_link = url_for('static', filename='assets/images/product-default.png')
    db.products.update_one(
        {"_id": ObjectId(data['product_id'])},
        {'$set': {
            "image_link": img_link,
            'commodity_name': data['product_name'],
            'category': data['product_category'],
            "description": data['product_description']
        }})
    db.inventories.update_many(
        {'commodity_id': data['product_id']},
        {'$set': {
            "commodity_name": data['product_name'],
            "commodity_image_link": img_link,
            "commodity_description": data['product_description'],
            "category": data['product_category']
        }}
    )


# =============================repositories=============================
def get_repository(repository_id):
    return db.repositories.find_one({"_id": ObjectId(repository_id)})


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
    db.inventories.delete_many({'repository_id': data['repository_id']})


def edit_repository(data):
    db.repositories.update_one({"_id": ObjectId(data['repository_id'])},
                               {'$set': {'repository_name': data['repository_name']}})
    db.inventories.update_many({'repository_id': data['repository_id']},
                               {'$set': {"repository_name": data['repository_name']}})


# =============================inventories=============================
def get_inventory(inventory_id):
    return db.inventories.find_one({"_id": ObjectId(inventory_id)})


def get_inventories():
    inventories = list(db.inventories.find())
    for inventory in inventories:
        inventory['_id'] = str(inventory['_id'])
    return inventories


def get_shopping_inventories(shopping_list):
    shopping_detail = []
    if shopping_list:
        for key, value in shopping_list.items():
            inventory = db.inventories.find_one({"_id": ObjectId(key)})
            shopping_detail.append(
                {'inventory_id': str(inventory['_id']),
                 'name': inventory['commodity_name'],
                 'price': inventory['price'],
                 'quantity': value}
            )
        return shopping_detail


def get_detail_finalize_shopping(shopping_list):
    shopping_detail = []
    if shopping_list:
        for key, value in shopping_list.items():
            inventory = db.inventories.find_one({"_id": ObjectId(key)})
            shopping_detail.append({
                'inventory_id': key,
                'commodity_name': inventory['commodity_name'],
                'price': inventory['price'],
                'commodity_id': inventory['commodity_id'],
                'repository_id': inventory['repository_id'],
                'repository_name': inventory['repository_name'],
                'quantity': value
            })
        return shopping_detail


def add_inventory(data):
    exist = db.inventories.find_one({
        'commodity_id': data['inventory_product_id'],
        'repository_id': data['inventory_repository_id']
    })
    product = get_product(data['inventory_product_id'])
    repository = get_repository(data['inventory_repository_id'])
    if not exist and product and repository:
        db.inventories.insert_one({
            "commodity_id": data['inventory_product_id'],
            "commodity_name": product['commodity_name'],
            "commodity_image_link": product['image_link'],
            "commodity_description": product['description'],
            "category": product['category'],
            "price": data['inventory_price'],
            "quantity": data['inventory_quantity'],
            "repository_id": data['inventory_repository_id'],
            "repository_name": repository['repository_name'],
            "create_time": datetime.utcnow()
        })


def delete_inventory(data):
    db.inventories.delete_one({"_id": ObjectId(data['inventory_id'])})


def edit_inventory(data):
    inventory = get_inventory(data['inventory_id'])
    product = get_product(data['inventory_product_id'])
    repository = get_repository(data['inventory_repository_id'])
    if inventory and product and repository:
        db.inventories.update_one(
            {"_id": ObjectId(data['inventory_id'])},
            {'$set': {
                "commodity_id": data['inventory_product_id'],
                "commodity_name": product['commodity_name'],
                "commodity_image_link": product['image_link'],
                "commodity_description": product['description'],
                "category": product['category'],
                "price": data['inventory_price'],
                "quantity": data['inventory_quantity'],
                "repository_id": data['inventory_repository_id'],
                "repository_name": repository['repository_name'],
                "create_time": datetime.utcnow()
            }})


# =============================orders=============================
def get_orders():
    orders = list(db.orders.find({}, {
        "_id": 1,
        "user_name": 1,
        "total_price": 1,
        "order_time": 1
    }))
    for order in orders:
        order['_id'] = str(order['_id'])
    return orders


def get_order_details(order_id):
    return db.orders.find_one({"_id": ObjectId(order_id)}, {"_id": 0})
