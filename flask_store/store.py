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
    return render_template("store/base_store.html")
