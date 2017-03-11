import os
import sqlite3
from datetime import datetime
from operator import itemgetter
from bottle import route, run, template, request


@route('/comics')
@route('/comics/<no:int>')
def comics_list(no=0):
    conn = sqlite3.connect('comics.db')
    c = conn.cursor()
    sql = "SELECT id, title, volume, publish_date, publisher, stars, \
           reviewers, next_date, author, url_id, isbn, reviews FROM comics"
    c.execute(sql)
    result = c.fetchall()
    c.close()
    if no in [0, 1, 7]:
        result = sorted(result, key=itemgetter(no))
    else:
        result = sorted(result, key=itemgetter(no), reverse=True)
    fmt = '%Y/%m/%d %H:%M:%S'
    ld = datetime.fromtimestamp(os.stat('comics.db').st_mtime).strftime(fmt)
    return template('index', rows=result, last_update=ld, no=no)


@route('/sort_request', method='GET')
def sort_request():
    no = request.query.no
    return comics_list(int(no))


# run(debug=True, reloader=True)
run()
