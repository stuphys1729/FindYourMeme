import pysolr
import sqlite3

solr = pysolr.Solr("http://localhost:8983/solr/test_core_2", timeout=10)
