import json
from flask import Blueprint
from flask import request
from flask import render_template
from flask import current_app
from flask import url_for
from flask import redirect

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with open("flask_store/users.json") as user_file:
            users = json.load(user_file)
            for user in users:
                if username == user[0] and password == user[1]:
                    return redirect(url_for("hello"))
            return render_template("admin_panel/login.html", error="incorect username or password")
    else:
        return render_template("admin_panel/login.html", error=None)
