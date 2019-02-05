from flask import Flask, url_for, request, render_template
from .index import solr_search, setup_collection, fetch_meme, create_db
import threading


app = Flask(__name__)
create_db()

# TODO threading is a bitch at the best of times, we can look into celery if we
# really want but I suggest that for a project like this we just don't thread
# in the first place
# threading.Thread(target=setup_collection).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=('GET',))
def search():
    search_term = request.args.get('s')
    no_terms = int(request.args.get('n'))
    page_no = int(request.args.get('p'))

    if len(search_term) == 0:
        search_term = "*"

    link_results = solr_search(search_term, no_terms, page_no)

    return render_template('index.html' \
        , results=link_results \
        , search_term=search_term \
        , page_no=page_no \
        , no_terms=no_terms)

@app.route('/meme/<string:meme_id>')
def meme(meme_id):
    meme_result = fetch_meme(meme_id)
    return render_template('image.html', result=meme_result)

@app.route('/scrape')
def scrape():
    # TODO scrape from here
    # setup_collection()
    threading.Thread(target=setup_collection).start()
    return "Scraping"
