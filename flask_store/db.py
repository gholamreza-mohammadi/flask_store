from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

client = MongoClient('localhost', 27017)

#=============================products=============================
def get_products():
    db = client.store
    products = list(db.products.find())
    for p in products:
        p['_id'] = str(p['_id'])
    return products

def add_product(data):
    db = client.store
    if not (list(db.products.find({"commodity_name":data['product_name']}))):
        db.products.insert_one({
        "image_link": "",
        "commodity_name": data['product_name'],
        "category": data['product_category']
        })

def delete_product(data):
    db = client.store
    db.products.delete_one({"_id": ObjectId(data['product_id'])})
    
def edit_product(data):
    db = client.store
    db.products.update_one(
        {"_id":ObjectId(data['product_id'])},
        {'$set':{
            'commodity_name':data['product_name'],
            'category':data['product_category']
            }
        })
        

#=============================repositories=============================
def get_repositories():
    db = client.store
    repositories = list(db.repositories.find())
    for p in repositories:
        p['_id'] = str(p['_id'])
    return repositories

def add_repositories(data):
    db = client.store
    if not (list(db.repositories.find({"repository_name":data['repository_name']}))):
        db.repositories.insert_one({
        "repository_name": data['repository_name']
        })

def delete_repositories(data):
    db = client.store
    db.repositories.delete_one({"_id": ObjectId(data['repository_id'])})
   
def edit_repository(data):
    db = client.store
    db.repositories.update_one({"_id":ObjectId(data['repository_id'])},{'$set':{'repository_name':data['repository_name']}})