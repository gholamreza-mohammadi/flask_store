import json
from datetime import datetime, timedelta
import pytz
from flask import Blueprint
from flask import request
from flask import render_template
from flask import current_app
from flask import url_for
from flask import redirect
from flask import session
from flask import abort
from flask import Markup
from pymongo import MongoClient, ASCENDING, DESCENDING
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
        products_inventory = db.inventories.aggregate([
            {"$match": {"$and": [{'category': {'$regex': category}}, {"quantity": {"$gt": 0}}]}},
            {"$sort": {"commodity_id": 1, "price": 1, "create_time": -1}},
            {"$group": {
                "_id": "$commodity_id",
                "tmp_id": {"$first": "$_id"},
                "commodity_name": {"$first": "$commodity_name"},
                "price": {"$first": "$price"},
                "image_link": {"$first": "$commodity_image_link"},
                "create_time": {"$first": "$create_time"}
            }},
            {"$project": {
                "_id": 0,
                "id": "$tmp_id",
                "commodity_name": 1,
                "price": 1,
                "image_link": 1,
                "create_time": 1
            }},
            {"$sort": {"create_time": -1}},
            {'$limit': 6}
        ])
        products_category.append({'category': category.split('-')[-1].strip(),
                                  'category_full': category,
                                  'commodities': products_inventory})
    return render_template("store/home_page.html", products=products_category)


@bp.route("/product/<id>/<product_name>", methods=["GET", "POST"])
def detail(id, product_name):
    client = MongoClient('localhost', 27017)
    db = client.store
    commodity = db.inventories.find_one({'_id': ObjectId(id)})
    if request.method == "POST":
        if 'shopping_list' not in session:
            session['shopping_list'] = {}
        session['shopping_list'][id] = request.form["quantity"]
        session.modified = True
        return redirect(url_for('store.detail', id=id))
    else:
        qty = 0
        if 'shopping_list' in session and id in session['shopping_list']:
            qty = session['shopping_list'][id]
        return render_template("store/detail_page.html", commodity=commodity, qty=qty)


@bp.route("/category/<category_name>")
def category(category_name):
    with open('flask_store/static/json_folder/categories.json', encoding='utf-8') as categories_json:
        categories_dict = json.load(categories_json)

    markup = categories_to_markup(categories_dict)

    client = MongoClient('localhost', 27017)
    db = client.store

    products_inventory = db.inventories.aggregate([
        {"$match": {"$and": [{'category': {'$regex': category_name}}, {"quantity": {"$gt": 0}}]}},
        {"$sort": {"commodity_id": 1, "price": 1, "create_time": -1}},
        {"$group": {
            "_id": "$commodity_id",
            "tmp_id": {"$first": "$_id"},
            "commodity_name": {"$first": "$commodity_name"},
            "price": {"$first": "$price"},
            "image_link": {"$first": "$commodity_image_link"},
            "create_time": {"$first": "$create_time"}
        }},
        {"$project": {
            "_id": 0,
            "id": "$tmp_id",
            "commodity_name": 1,
            "price": 1,
            "image_link": 1,
            "create_time": 1
        }},
        {"$sort": {"create_time": -1}}
    ])

    return render_template("store/category_page.html",
                           tree=Markup(markup),
                           category_name=category_name.split('-')[-1].strip(),
                           products=products_inventory)


@bp.route("/cart")
def cart():
    shopping_detail, shopping_list = [], session.get('shopping_list')
    if shopping_list:
        shopping_detail = db.get_shopping_inventories(shopping_list)
    total_price = sum(shop['price'] * shop['quantity'] for shop in shopping_detail)
    return render_template("store/cart.html", products=shopping_detail, total_price=total_price)


@bp.route("/final", methods=["GET", "POST"])
def finalize():
    if 'shopping_list' not in session:
        session['shopping_list'] = {}
    if request.method == "POST":
        client = MongoClient('localhost', 27017)
        database = client.store
        products = db.finalize_shopping(session.get('shopping_list'))
        total_price = sum(product['price'] * product['quantity'] for product in products)
        database.orders.insert_one({
            "user_name": request.form['user_name'],
            "total_price": total_price,
            "order_time": datetime.now().replace(tzinfo=pytz.UTC),
            "resive_time": datetime.strptime(request.form['resive_time'], '%Y-%m-%d').replace(
                tzinfo=pytz.UTC),
            "address": request.form['address'],
            "phone": request.form['phone'],
            "products": products
        })
        session.pop('shopping_list', None)
        return redirect(url_for('store.home'))
    else:
        today = datetime.now().date()
        my_date = []
        for i in range(1, 32):
            my_date.append(today + timedelta(days=i))
        return render_template("store/finalize.html", date=my_date,
                               disabled='' if session['shopping_list'] else 'disabled')


@bp.route("/change-shopping-list", methods=["POST", "GET"])
def change_shopping_list():
    if request.method == "POST":
        data = request.get_json()
        if data['id'] in session['shopping_list']:
            del session['shopping_list'][data['id']]
            session.modified = True
            return 'deleted'
        return 'fail'
    else:
        abort(404)
