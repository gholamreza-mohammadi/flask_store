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
from .functions import *

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
                             "image_link": "https://appiranie.websites.co.in/e-store/img/defaults/product-default.png",
                             "commodity_name": p['commodity_name'],
                             "price": p['price']})
        products_category.append({'category': category.split('-')[-1].strip(),
                                  'category_full': category,
                                  'commodities': products})
    # products = [{
    #     "category": "مواد غذایی / کالاهای اساسی و خوار و بار",
    #     "commodities": [{"id": 1000,
    #                      "image_link": "https://www.ibiar.com/images/6261107003705-256.jpg",
    #                      "commodity_name": "لوبیا قرمز 900 گرمی گلستان",
    #                      "price": 15000},
    #                     {"id": '5fe3906fbb251b36788f774f',
    #                      "image_link": "https://onemarketco.ir/wp-content/uploads/8083FA0D-46D9-4EC1-B53C-3DD7E7365400.jpeg",
    #                      "commodity_name": "روغن مخصوص سرخ کردنی بدون پالم 2000 میلی لیتری اویلا",
    #                      "price": 40000},
    #                     {"id": 1002,
    #                      "image_link": "https://onemarketco.ir/wp-content/uploads/6EDDF87E-A388-4965-906D-3B63270AB958.jpeg",
    #                      "commodity_name": "روغن مایع آفتابگردان ویتامینه 1800 میلی لیتری غنچه",
    #                      "price": 38000},
    #                     {"id": 1003,
    #                      "image_link": "https://www.ibiar.com/images/6260063200845-256.jpg",
    #                      "commodity_name": "کره سنتی ۱۰۰ گرمی شکلی",
    #                      "price": 3500},
    #                     {"id": 1004,
    #                      "image_link": "https://www.ibiar.com/images/8000070018686-256.jpg",
    #                      "commodity_name": "پودر قهوه دم کردنی اسپرسو 250 گرمی لاواتزا",
    #                      "price": 50000}]
    # }]
    # current_app.logger.debug(products_category)
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

    categories = hierarchical_category_list(categories_dict)
    # current_app.logger.debug(categories)

    def categories_to_markup(markup_str: str, _categories: list) -> str:
        markup_str += '<ul>'
        for element in _categories:
            markup_str += f'<li><a href="{url_for("store.category", category_name=element["name"][1])}">' + element['name'][0] + '</a></li>'
            if 'subcategoies' in element:
                markup_str = categories_to_markup(markup_str, element['subcategoies'])
        markup_str += '</ul>'
        return markup_str

    markup = ''
    markup = categories_to_markup(markup, categories)
    # current_app.logger.debug(markup)

    client = MongoClient('localhost', 27017)
    db = client.store

    products_inventory_list = list(db.inventories.find({'category': {'$regex': category_name}}))
    products = []

    for product_inventory in products_inventory_list:
        products.append({"id": product_inventory['_id'],
                         "image_link": "https://appiranie.websites.co.in/e-store/img/defaults/product-default.png",
                         "commodity_name": product_inventory['commodity_name'],
                         "price": product_inventory['price']})

    return render_template("store/category_page.html",
                           tree=Markup(markup),
                           category_name=category_name.split('-')[-1],
                           products=products)
