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

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with open("flask_store/users.json") as user_file:
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
                      {"id": None,
                       "user_name": "اکبر زمانی",
                       "total_price": 920000,
                       "order_time": '1399/01/05'},
                      {"id": None,
                       "user_name": "رامین رحیمی",
                       "total_price": 8764300,
                       "order_time": '1399/01/04'},
                      {"id": None,
                       "user_name": "ملیکا زارعی",
                       "total_price": 3324000,
                       "order_time": '1399/01/03'},
                      {"id": None,
                       "user_name": "نیکی کریمی",
                       "total_price": 1258000,
                       "order_time": '1399/01/02'},
                      {"id": None,
                       "user_name": "فریبرز عربنیا",
                       "total_price": 540000,
                       "order_time": '1399/01/01'}
                  ]}
        return orders
    else:
        abort(404)


@bp.route("/inventory-api", methods=["POST", "GET"])
def get_inventories():
    if request.method == "POST":
        inventories = {"column_names": ["id", "repository_name", "commodity_name", "price", "quantity"],
                       'data': [
                           {"id": None,
                            "repository_name": "انبار شماره ۱",
                            "commodity_name": "لوبیا قرمز 900 گرمی گلستان",
                            "price": 200000,
                            "quantity": 100},
                           {"id": None,
                            "repository_name": "انبار شماره ۱",
                            "commodity_name": "روغن مخصوص سرخ کردنی بدون پالم 2000 میلی لیتری اویلا",
                            "price": 10000,
                            "quantity": 200},
                           {"id": None,
                            "repository_name": "انبار شماره ۲",
                            "commodity_name": "روغن مایع آفتابگردان ویتامینه 1800 میلی لیتری غنچه",
                            "price": 150000,
                            "quantity": 300},
                           {"id": None,
                            "repository_name": "انبار شماره ۲",
                            "commodity_name": "کره سنتی ۱۰۰ گرمی شکلی",
                            "price": 25500,
                            "quantity": 400},
                           {"id": None,
                            "repository_name": "انبار شماره ۳",
                            "commodity_name": "پودر قهوه دم کردنی اسپرسو 250 گرمی لاواتزا",
                            "price": 1000000,
                            "quantity": 500}
                       ]}
        return inventories
    else:
        abort(404)


@bp.route("/repository-api", methods=["POST", "GET"])
def get_repositories():
    if request.method == "POST":
        repositories = {"column_names": ["id", "repository_name"],
                        'data': [
                            {"id": None, "repository_name": "انبار شماره ۱"},
                            {"id": None, "repository_name": "انبار شماره ۲"},
                            {"id": None, "repository_name": "انبار شماره ۳"}
                        ]}
        return repositories
    else:
        abort(404)


@bp.route("/category-api", methods=["POST", "GET"])
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


@bp.route("/product-api", methods=["POST", "GET"])
def get_products():
    if request.method == "POST":
        products = {
            "column_names": ["id", "image_link", "commodity_name", "category"],
            "data": [{"id": None,
                      "image_link": "https://www.ibiar.com/images/6261107003705-256.jpg",
                      "commodity_name": "لوبیا قرمز 900 گرمی گلستان",
                      "category": "مواد غذایی / کالاهای اساسی و خوار و بار"},
                     {"id": None,
                      "image_link": "https://onemarketco.ir/wp-content/uploads/8083FA0D-46D9-4EC1-B53C-3DD7E7365400.jpeg",
                      "commodity_name": "روغن مخصوص سرخ کردنی بدون پالم 2000 میلی لیتری اویلا",
                      "category": "مواد غذایی / کالاهای اساسی و خوار و بار"},
                     {"id": None,
                      "image_link": "https://onemarketco.ir/wp-content/uploads/6EDDF87E-A388-4965-906D-3B63270AB958.jpeg",
                      "commodity_name": "روغن مایع آفتابگردان ویتامینه 1800 میلی لیتری غنچه",
                      "category": "مواد غذایی / کالاهای اساسی و خوار و بار"},
                     {"id": None,
                      "image_link": "https://www.ibiar.com/images/6260063200845-256.jpg",
                      "commodity_name": "کره سنتی ۱۰۰ گرمی شکلی",
                      "category": "مواد غذایی / لبنیات"},
                     {"id": None,
                      "image_link": "https://www.ibiar.com/images/8000070018686-256.jpg",
                      "commodity_name": "پودر قهوه دم کردنی اسپرسو 250 گرمی لاواتزا",
                      "category": "مواد غذایی / نوشیدنی"}]
        }
        return products
    else:
        abort(404)


@bp.route("/product", methods=["POST", "GET"])
def product():
    if request.method == "POST":
        products = [
            ("https://www.ibiar.com/images/6261107003705-256.jpg",
             "لوبیا قرمز 900 گرمی گلستان",
             "مواد غذایی / کالاهای اساسی و خوار و بار"),
            ("https://onemarketco.ir/wp-content/uploads/8083FA0D-46D9-4EC1-B53C-3DD7E7365400.jpeg",
             "روغن مخصوص سرخ کردنی بدون پالم 2000 میلی لیتری اویلا",
             "مواد غذایی / کالاهای اساسی و خوار و بار"),
            ("https://onemarketco.ir/wp-content/uploads/6EDDF87E-A388-4965-906D-3B63270AB958.jpeg",
             "روغن مایع آفتابگردان ویتامینه 1800 میلی لیتری غنچه",
             "مواد غذایی / کالاهای اساسی و خوار و بار"),
            ("https://www.ibiar.com/images/6260063200845-256.jpg",
             "کره سنتی ۱۰۰ گرمی شکلی",
             "مواد غذایی / لبنیات"),
            ("https://www.ibiar.com/images/8000070018686-256.jpg",
             "پودر قهوه دم کردنی اسپرسو 250 گرمی لاواتزا",
             "مواد غذایی / نوشیدنی")
        ]
        return render_template("admin_panel/product.html", products=products)
    else:
        abort(404)


@bp.route("/repository")
def repository():
    repositorys = [("انبار شماره 1"),
                   ("انبار شماره 2"),
                   ("انبار شماره 3")]
    return render_template("admin_panel/repository.html", repositorys=repositorys)
