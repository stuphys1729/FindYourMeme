from flask import Blueprint, g, render_template, request, url_for

bp = Blueprint('search', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/search', methods=('GET',))
def search():
    # return request.args.get('s')

    results = ["test1", "test2", "test3"]

    return render_template('index.html', results=results)
