# -*- coding: utf-8 -*-
import sqlite3
import csv

conn = sqlite3.connect('comics.db')
with conn:
    c = conn.cursor()
    sql = "INSERT OR IGNORE INTO comics (title, author) VALUES (?, ?);"
    with open('insert.csv', 'r') as f:
        reader = csv.reader(f)
        for title, author in reader:
            c.execute(sql, (unicode(title, 'cp932'), unicode(author, 'cp932')))
