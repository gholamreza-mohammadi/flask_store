import os

from flask import Flask, render_template, current_app


def page_not_found(error):
    current_app.logger.debug(error)
    return render_template('404_page.html'), 404


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     # a default secret that should be overridden by instance config
    #     SECRET_KEY="dev",
    #     # store the database in the instance folder
    #     DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    # )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # @app.route("/hello/")
    # def hello():
    #     return "Hello, World!"

    # # register the database commands
    # from flasflask_storekr import db
    #
    # db.init_app(app)
    #
    # # apply the blueprints to the app
    from flask_store import admin, store

    app.register_blueprint(admin.bp)
    app.register_blueprint(store.bp)

    app.register_error_handler(404, page_not_found)

    # # make url_for('index') == url_for('blog.index')
    # # in another app, you might define a separate main index here with
    # # app.route, while giving the blog blueprint a url_prefix, but for
    # # the tutorial the blog will be the main index
    # app.add_url_rule("/", endpoint="index")
    app.add_url_rule("/", endpoint="home")

    return app
