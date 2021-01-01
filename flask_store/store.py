import json
from flask import Blueprint
from flask import request
from flask import render_template
from flask import current_app
from flask import url_for
from flask import redirect
from flask import session
from flask import abort
from flask import Markup
from pymongo import MongoClient
from bson import ObjectId
from . import db
from .functions import categories_to_markup


bp = Blueprint("store", __name__)


@bp.route("/", methods=["GET", "POST"])
def home():
    with open('flask_store/static/json_folder/categories.json', encoding='utf-8') as categories_json:
        categories_dict = json.load(categories_json)

    products_category = []
    categories = []

    for element in categories_dict:
        sub_categoies = element.get('subcategoies')
        if sub_categoies:
            for each in sub_categoies:
                categories.append(element['name'] + ' - ' + each['name'])
        else:
            categories.append(element['name'])

    client = MongoClient('localhost', 27017)
    db = client.store

    for category in categories:
        pp = list(db.inventories.find({'category': {'$regex': category}}))
        products = []
        for p in pp:
            products.append({"id": p['_id'],
                             "image_link": p['commodity_image_link'],
                             "commodity_name": p['commodity_name'],
                             "price": p['price']})
        products_category.append({'category': category.split('-')[-1].strip(),
                                  'category_full': category,
                                  'commodities': products})
    return render_template("store/home_page.html", products=products_category)


@bp.route("/product/<id>")
def detail(id):
    client = MongoClient('localhost', 27017)
    db = client.store
    commodity = list(db.inventories.find({'_id': ObjectId(id)}))[0]
    de_im = list(db.products.find(
        {"commodity_name": commodity['commodity_name']},
        {"_id": 0, 'description': 1, 'image_link': 1}))[0]
    return render_template("store/detail_page.html", commodity=commodity, de_im=de_im)


@bp.route("/category/<category_name>")
def category(category_name):
    with open('flask_store/static/json_folder/categories.json', encoding='utf-8') as categories_json:
        categories_dict = json.load(categories_json)

    markup = categories_to_markup(categories_dict)

    client = MongoClient('localhost', 27017)
    db = client.store

    products_inventory_list = list(db.inventories.find({'category': {'$regex': category_name}}))
    products = []

    for product_inventory in products_inventory_list:
        products.append({"id": product_inventory['_id'],
                         "image_link": product_inventory['commodity_image_link'],
                         "commodity_name": product_inventory['commodity_name'],
                         "price": product_inventory['price']})

    return render_template("store/category_page.html",
                           tree=Markup(markup),
                           category_name=category_name.split('-')[-1],
                           products=products)
