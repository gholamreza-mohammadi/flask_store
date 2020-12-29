import json
from flask import Blueprint
from flask import request
from flask import render_template
from flask import current_app
from flask import url_for
from flask import redirect
from flask import session
from flask import abort
from cryptography.fernet import Fernet
from . import db


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with open('flask_store/static/json_folder/users.json') as user_file:
            users = json.load(user_file)
            cipher_suite = Fernet(current_app.config['CIPHER_KEY'])
            for user in users:
                unciphered_pass = (cipher_suite.decrypt(bytes(user[1], 'utf-8'))).decode("utf-8")
                if username == user[0] and password == unciphered_pass:
                    session['username'] = username
                    return redirect(url_for("admin.management"), code=307)
            return render_template("admin_panel/login.html", error="incorect username or password")
    else:
        return render_template("admin_panel/login.html", error=None)


@bp.route("/management", methods=["POST", "GET"])
def management():
    if request.method == "POST":
        return render_template("admin_panel/base_admin.html")
    else:
        abort(404)


@bp.route("/order-api", methods=["POST", "GET"])
def get_orders():
    if request.method == "POST":
        orders = {"column_names": ["id", "user_name", "total_price", "order_time"],
                  'data': [
                      {"id": 4000,
                       "user_name": "اکبر زمانی",
                       "total_price": 920000,
                       "order_time": '1399/01/05'},
                      {"id": 4001,
                       "user_name": "رامین رحیمی",
                       "total_price": 8764300,
                       "order_time": '1399/01/04'},
                      {"id": 4002,
                       "user_name": "ملیکا زارعی",
                       "total_price": 3324000,
                       "order_time": '1399/01/03'},
                      {"id": 4003,
                       "user_name": "نیکی کریمی",
                       "total_price": 1258000,
                       "order_time": '1399/01/02'},
                      {"id": 4004,
                       "user_name": "فریبرز عربنیا",
                       "total_price": 540000,
                       "order_time": '1399/01/01'}
                  ]}
        return orders
    else:
        abort(404)


@bp.route("/set-inventory", methods=["POST", "GET"])
def set_inventories():
    if request.method == "POST":
        data = request.get_json()
        if 'add_inventory' in data:
            db.add_inventory(data)
            current_app.logger.debug('add_inventory')
            current_app.logger.debug(data['inventory_repository'])
            current_app.logger.debug(data['inventory_product'])
            current_app.logger.debug(data['inventory_price'])
            current_app.logger.debug(data['inventory_quantity'])
            return 'add_repository'
        elif 'edit_inventory' in data:
            # db.edit_inventory(data)
            current_app.logger.debug('edit_inventory')
            current_app.logger.debug(data['inventory_id'])
            current_app.logger.debug(data['inventory_repository'])
            current_app.logger.debug(data['inventory_product'])
            current_app.logger.debug(data['inventory_price'])
            current_app.logger.debug(data['inventory_quantity'])
            return 'edit_inventory'
        elif 'delete_inventory' in data:
            # db.delete_inventory(data)
            current_app.logger.debug('delete_inventory')
            current_app.logger.debug(data['inventory_id'])
            return 'delete_inventory'
        else:
            return 'invalid request'
    else:
        abort(404)


@bp.route("/get-inventory", methods=["POST", "GET"])
def get_inventories():
    if request.method == "POST":
        inventories = {"column_names": ["id", "repository_name", "commodity_name", "price", "quantity"],
                       'data': db.get_inventories()
                       }
        # inventories = {"column_names": ["id", "repository_name", "commodity_name", "price", "quantity"],
        #                'data': [
        #                    {"id": 3000,
        #                     "repository_name": "انبار شماره ۱",
        #                     "commodity_name": "لوبیا قرمز 900 گرمی گلستان",
        #                     "price": 200000,
        #                     "quantity": 100},
        #                    {"id": 3001,
        #                     "repository_name": "انبار شماره ۱",
        #                     "commodity_name": "روغن مخصوص سرخ کردنی بدون پالم 2000 میلی لیتری اویلا",
        #                     "price": 10000,
        #                     "quantity": 200},
        #                    {"id": 3002,
        #                     "repository_name": "انبار شماره ۲",
        #                     "commodity_name": "روغن مایع آفتابگردان ویتامینه 1800 میلی لیتری غنچه",
        #                     "price": 150000,
        #                     "quantity": 300},
        #                    {"id": 3003,
        #                     "repository_name": "انبار شماره ۲",
        #                     "commodity_name": "کره سنتی ۱۰۰ گرمی شکلی",
        #                     "price": 25500,
        #                     "quantity": 400},
        #                    {"id": 3004,
        #                     "repository_name": "انبار شماره ۳",
        #                     "commodity_name": "پودر قهوه دم کردنی اسپرسو 250 گرمی لاواتزا",
        #                     "price": 1000000,
        #                     "quantity": 500}
        #                ]}
        return inventories
    else:
        abort(404)



@bp.route("/set-repository", methods=["POST", "GET"])
def set_repositories():
    if request.method == "POST":
        data = request.get_json()
        if 'add_repository' in data:
            db.add_repositories(data)
            current_app.logger.debug('add_repository')
            current_app.logger.debug(data['repository_name'])
            return 'add_repository'
        elif 'edit_repository' in data:
            db.edit_repository(data)
            current_app.logger.debug('edit_repository')
            current_app.logger.debug(data['repository_id'])
            current_app.logger.debug(data['repository_name'])
            return 'edit_repository'
        elif 'delete_repository' in data:
            db.delete_repositories(data)
            current_app.logger.debug('delete_repository')
            current_app.logger.debug(data['repository_id'])
            return 'delete_repository'
        else:
            return 'invalid request'
    else:
        abort(404)


@bp.route("/get-repository", methods=["POST", "GET"])
def get_repositories():
    if request.method == "POST":
        repositories = db.get_repositories()
        repositories = {"column_names": ["_id", "repository_name"],
                        'data': repositories
                            }
        # repositories = {"column_names": ["id", "repository_name"],
        #                 'data': [
        #                     {"id": 2000, "repository_name": "انبار شماره ۱"},
        #                     {"id": 2001, "repository_name": "انبار شماره ۲"},
        #                     {"id": 2002, "repository_name": "انبار شماره ۳"}
        #                 ]}
        return repositories
    else:
        abort(404)



@bp.route("/get-category", methods=["POST", "GET"])
def get_categories():
    if request.method == "POST":
        categories = {'data': [
            'مواد غذایی / کالاهای اساسی و خوار و بار',
            'مواد غذایی / لبنیات',
            'مواد غذایی / نوشیدنی'
        ]}
        return categories
    else:
        abort(404)


@bp.route("/set-product", methods=["POST", "GET"])
def set_products():
    if request.method == "POST":
        file = request.files.get('products_file')
        if file:
            # current_app.logger.debug(file.read())
            current_app.logger.debug(file)
            return 'add_products'
        else:
            data = request.get_json()
            if 'delete_product' in data:
                db.delete_product(data)
                current_app.logger.debug('delete_product')
                current_app.logger.debug(data['product_id'])
                return 'delete_product'
            elif 'edit_product' in data:
                db.edit_product(data)
                current_app.logger.debug('edit_product')
                current_app.logger.debug(data['product_id'])
                current_app.logger.debug(data['product_name'])
                current_app.logger.debug(data['product_category'])
                return 'edit_product'
            elif 'add_product' in data:
                db.add_product(data)
                current_app.logger.debug('add_product')
                current_app.logger.debug(data['product_name'])
                current_app.logger.debug(data['product_category'])
                return 'add_product'
            else:
                return 'invalid request'
    else:
        abort(404)


@bp.route("/get-products", methods=["POST", "GET"])
def get_products():

    if request.method == "POST":
        products = db.get_products()
        products = {
            "column_names": ["_id", "image_link", "commodity_name", "category"],
            "data": products
            }
        # products = {
        #     "column_names": ["id", "image_link", "commodity_name", "category"],
        #     "data": [{"id": 1000,
        #               "image_link": "https://www.ibiar.com/images/6261107003705-256.jpg",
        #               "commodity_name": "لوبیا قرمز 900 گرمی گلستان",
        #               "category": "مواد غذایی / کالاهای اساسی و خوار و بار"},
        #              {"id": 1001,
        #               "image_link": "https://onemarketco.ir/wp-content/uploads/8083FA0D-46D9-4EC1-B53C-3DD7E7365400.jpeg",
        #               "commodity_name": "روغن مخصوص سرخ کردنی بدون پالم 2000 میلی لیتری اویلا",
        #               "category": "مواد غذایی / کالاهای اساسی و خوار و بار"},
        #              {"id": 1002,
        #               "image_link": "https://onemarketco.ir/wp-content/uploads/6EDDF87E-A388-4965-906D-3B63270AB958.jpeg",
        #               "commodity_name": "روغن مایع آفتابگردان ویتامینه 1800 میلی لیتری غنچه",
        #               "category": "مواد غذایی / کالاهای اساسی و خوار و بار"},
        #              {"id": 1003,
        #               "image_link": "https://www.ibiar.com/images/6260063200845-256.jpg",
        #               "commodity_name": "کره سنتی ۱۰۰ گرمی شکلی",
        #               "category": "مواد غذایی / لبنیات"},
        #              {"id": 1004,
        #               "image_link": "https://www.ibiar.com/images/8000070018686-256.jpg",
        #               "commodity_name": "پودر قهوه دم کردنی اسپرسو 250 گرمی لاواتزا",
        #               "category": "مواد غذایی / نوشیدنی"}]
        # }
        return products
    else:
        abort(404)
