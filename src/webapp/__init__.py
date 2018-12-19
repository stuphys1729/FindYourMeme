from flask import Flask, url_for, request, render_template

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return "Hello, world!"

    return app
