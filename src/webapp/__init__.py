from flask import Flask, url_for, request, render_template
from .index import test_results

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=('GET',))
def search():
    link_results = test_results()
    search_term = request.args.get('s')

    return render_template('index.html', results=link_results, search_term=search_term)

@app.route('/meme/<int:meme_id>')
def meme(meme_id):
    meme_result = test_results()[meme_id]
    return render_template('image.html', result=meme_result)
