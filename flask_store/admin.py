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
                    return redirect(url_for("admin.product"), code=307)
            return render_template("admin_panel/login.html", error="incorect username or password")
    else:
        return render_template("admin_panel/login.html", error=None)


@bp.route("/product-api", methods=["POST", "GET"])
def get_products():
    if request.method == "POST":
        products = [
            {"name": "لوبیا قرمز 900 گرمی گلستان",
             "img_link": "https://www.ibiar.com/images/6261107003705-256.jpg",
             "category": "مواد غذایی / کالاهای اساسی و خوار و بار"},
            {"name": "روغن مخصوص سرخ کردنی بدون پالم 2000 میلی لیتری اویلا",
             "img_link": "https://onemarketco.ir/wp-content/uploads/8083FA0D-46D9-4EC1-B53C-3DD7E7365400.jpeg",
             "category": "مواد غذایی / کالاهای اساسی و خوار و بار"},
            {"name": "روغن مایع آفتابگردان ویتامینه 1800 میلی لیتری غنچه",
             "img_link": "https://onemarketco.ir/wp-content/uploads/6EDDF87E-A388-4965-906D-3B63270AB958.jpeg",
             "category": "مواد غذایی / کالاهای اساسی و خوار و بار"},
            {"name": "کره سنتی ۱۰۰ گرمی شکلی",
             "img_link": "https://www.ibiar.com/images/6260063200845-256.jpg",
             "category": "مواد غذایی / لبنیات"},
            {"name": "پودر قهوه دم کردنی اسپرسو 250 گرمی لاواتزا",
             "img_link": "https://www.ibiar.com/images/8000070018686-256.jpg",
             "category": "مواد غذایی / نوشیدنی"}
        ]
        return json.dumps(products, ensure_ascii=False).encode('utf-8')
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
