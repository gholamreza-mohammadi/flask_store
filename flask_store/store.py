import json
from flask import Blueprint
from flask import request
from flask import render_template
from flask import current_app
from flask import url_for
from flask import redirect
from flask import session
from flask import abort

bp = Blueprint("store", __name__)


@bp.route("/", methods=["GET", "POST"])
def home():
    products = [{
        "category": "مواد غذایی / کالاهای اساسی و خوار و بار",
        "commodities": [{"id": 1000,
                         "image_link": "https://www.ibiar.com/images/6261107003705-256.jpg",
                         "commodity_name": "لوبیا قرمز 900 گرمی گلستان",
                         "price": 15000},
                        {"id": 1001,
                         "image_link": "https://onemarketco.ir/wp-content/uploads/8083FA0D-46D9-4EC1-B53C-3DD7E7365400.jpeg",
                         "commodity_name": "روغن مخصوص سرخ کردنی بدون پالم 2000 میلی لیتری اویلا",
                         "price": 40000},
                        {"id": 1002,
                         "image_link": "https://onemarketco.ir/wp-content/uploads/6EDDF87E-A388-4965-906D-3B63270AB958.jpeg",
                         "commodity_name": "روغن مایع آفتابگردان ویتامینه 1800 میلی لیتری غنچه",
                         "price": 38000},
                        {"id": 1003,
                         "image_link": "https://www.ibiar.com/images/6260063200845-256.jpg",
                         "commodity_name": "کره سنتی ۱۰۰ گرمی شکلی",
                         "price": 3500},
                        {"id": 1004,
                         "image_link": "https://www.ibiar.com/images/8000070018686-256.jpg",
                         "commodity_name": "پودر قهوه دم کردنی اسپرسو 250 گرمی لاواتزا",
                         "price": 50000}]
    }]
    return render_template("store/home_page.html", products=products)
