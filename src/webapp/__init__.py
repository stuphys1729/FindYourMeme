from flask import Flask, url_for, request, render_template
from .index import solr_search, setup_collection, fetch_meme, create_db, sync_solr_with_db
import threading
from collections import defaultdict
import string
import copy


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
    time_since = request.args.get('t')

    full_search = copy.copy(search_term)

    search_term, subreddits = extract_arg(search_term, "subreddit")
    search_term, nsfw = extract_arg(search_term, "nsfw")

    # Check params in GET request
    no_terms = search_param_check(no_terms)
    page_no = search_param_check(page_no)
    search_term = preprocess(search_term)

    link_results = solr_search(search_term, no_terms, page_no, time_since, nsfw, subreddits)

    return render_template('index.html' \
        , results=link_results \
        , search_term=full_search \
        , page_no=page_no \
        , no_terms=no_terms
        , time_since=time_since
        , nav=True)

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

@app.route('/sync')
def sync():
    sync_solr_with_db()
    return("Sync complete")

def extract_arg(input_string, arg):
    if arg in input_string:
        return input_string[len(arg):].split(" ", 1)[1], input_string.split(arg + ":", 1)[1].split(" ", 1)[0].split(",")
    else:
        return input_string, ""

def search_param_check(number):
    if number < 0:
        return 0
    elif number > 10000:
        return 10000
    else:
        return number

def preprocess(search_term):
    '''
    Steps:
        Remove punctuation
    '''
    search_term = search_term.translate(str.maketrans('', '', string.punctuation))

    if len(search_term) == 0:
        search_term = '*'

    return search_term
