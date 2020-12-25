from pymongo import MongoClient


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