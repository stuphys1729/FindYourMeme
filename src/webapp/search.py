from flask import Blueprint, g, render_template, request, url_for
from .index import test_results

bp = Blueprint('search', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/search', methods=('GET',))
def search():
    # return request.args.get('s')

    link_results = test_results()
    search_term = request.args.get('s')

    return render_template('index.html', results=link_results, search_term=search_term)
