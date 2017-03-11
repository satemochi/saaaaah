# -*- coding: utf-8 -*-
import os.path
import sqlite3

db_name = 'comics.db'
if not os.path.isfile(db_name):
    conn = sqlite3.connect(db_name)
    with conn:
        conn.execute('CREATE TABLE IF NOT EXISTS comics \
                      (id INTEGER PRIMARY KEY, \
                       title VERCHAR(255) NOT NULL, \
                       author VERCHAR(255) NOT NULL, \
                       volume INTEGER, \
                       publish_date VERCHAR(32), \
                       stars FLOAT, \
                       reviews VERCHAR(8192), \
                       next_date VERCHAR(32), \
                       reviewers INTEGER, \
                       url_id INTEGER, \
                       publisher VERCHAR(255), \
                       isbn VERCHAR(10), \
                       last_update VERCHAR(32), \
                       UNIQUE(title));')
    print "Succcessfully created %s" % db_name
else:
    print "%s already exists..." % db_name
