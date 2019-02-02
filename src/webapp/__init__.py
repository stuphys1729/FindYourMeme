from flask import Flask, url_for, request, render_template
from .index import test_results, solr_search, setup_collection, fetch_meme
import threading


app = Flask(__name__)

# threading.Thread(target=setup_collection).start()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=('GET',))
def search():
    search_term = request.args.get('s')
    link_results = solr_search(search_term)

    return render_template('index.html', results=link_results, search_term=search_term)

@app.route('/meme/<string:meme_id>')
def meme(meme_id):
    meme_result = fetch_meme(meme_id)
    return render_template('image.html', result=meme_result)
