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


# @bp.before_app_request
# def load_logged_in_user():
#     """If a user id is stored in the session, load the user object from
#     the database into ``g.user``."""
#     user_id = session.get("user_id")
#
#     if user_id is None:
#         g.user = None
#     else:
#         g.user = (
#             get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
#         )


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


@bp.route("/product/<id>", methods=["GET", "POST"])
def detail(id):
    current_app.logger.debug(session.get('shopping_list'))
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


@bp.route("/cart")
def cart():
    shopping_detail = []
    shopping_list = session.get('shopping_list')
    if shopping_list:
        shopping_detail = db.get_shopping_inventories(shopping_list)
    total_price = sum([float(shop['price']) * float(shop['quantity']) for shop in shopping_detail])
    return render_template("store/cart.html", products=shopping_detail, total_price=total_price)


@bp.route("/final", methods=["GET", "POST"])
def finalize():
    current_app.logger.debug('finalll')
    if 'shopping_list' not in session:
        session['shopping_list'] = {}
    if request.method == "POST":
        current_app.logger.debug('in post')
        client = MongoClient('localhost', 27017)
        database = client.store
        database.orders.insert_one({
                "user_name": request.form['user_name'],
                "total_price": 540000,
                "order_time": "1399/01/01",
                "resive_time": request.form['resive_time'],
                "address": request.form['address'],
                "phone": request.form['phone'],
                "products": db.get_detail_finalize_shopping(session.get('shopping_list'))   
        })
        session.pop('shopping_list', None)
        return redirect(url_for('store.home'))
    else:
        current_app.logger.debug('in get')
        disabled = ""
        if not session['shopping_list']:
            disabled = 'disabled'
        return render_template("store/finalize.html",disabled=disabled)
#     if 'shopping_list' in session:
#         session.pop('shopping_list', None)
