from pymongo import MongoClient
from bson import ObjectId


client = MongoClient('localhost', 27017)

def get_products():
    db = client.store
    products = list(db.products.find())
    for p in products:
        p['_id'] = str(p['_id'])
    return products

def get_repositories():
    db = client.store
    repositories = list(db.repositories.find())
    for p in repositories:
        p['_id'] = str(p['_id'])
    return repositories

def add_product(data):
    db = client.store
    if not (list(db.products.find({"commodity_name":data['product_name']}))):
        db.products.insert_one({
        "image_link": "",
        "commodity_name": data['product_name'],
        "category": data['product_category'],
        "price": 0
        })

def delete_product(data):
    db = client.store
    db.products.delete_one({"_id": ObjectId(data['product_id'])})