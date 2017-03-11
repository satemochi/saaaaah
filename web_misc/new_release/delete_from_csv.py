# -*- coding: utf-8 -*-
import sqlite3
import csv

conn = sqlite3.connect('comics.db')
with conn:
    c = conn.cursor()
    sql = "DELETE FROM comics WHERE title=?;"
    with open('delete.csv', 'r') as f:
        reader = csv.reader(f)
        for title, in reader:
            c.execute(sql, (unicode(title, 'utf-8'), ))
