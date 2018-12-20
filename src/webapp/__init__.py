from flask import Flask, url_for, request, render_template

from . import search

def create_app():
    app = Flask(__name__)

    @app.route('/test')
    def hello():
        return "Hello, world!"

    app.register_blueprint(search.bp)

    return app
