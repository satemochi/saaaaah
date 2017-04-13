# -*- coding: utf-8 -*-
import sqlite3
import os
from datetime import datetime
import numpy as np
import pandas as pd


def get():
    sql = "SELECT title, volume, publish_date, reviewers, stars FROM comics"
    conn = sqlite3.connect('comics.db')
    c = conn.cursor()
    return c.execute(sql).fetchall()


def dump():
    mtime = os.stat('comics.db').st_mtime
    d = datetime.fromtimestamp(mtime).strftime('%Y%m%d')
    fname = 'dump_csv-' + d + '.csv'
    if not os.path.exists(fname):
        items = get()
        col = ('title', 'vol', 'pub_date', 'n_rev', 'stars')
        df = pd.DataFrame(index=np.arange(0, len(items)), columns=col)

        for i, v in enumerate(items):
            df.loc[i] = v

        df[['vol', 'n_rev']] = df[['vol', 'n_rev']].fillna(0).astype(int)
        df.to_csv(fname, index=False, encoding='utf-8')

if __name__ == '__main__':
    dump()
