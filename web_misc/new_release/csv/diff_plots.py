# -*- coding: utf-8 -*-
from glob import glob
import itertools
import re
import pandas as pd
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.palettes import Category20 as palette


def test_header(df):
    header = [u'title', u'vol', u'pub_date', u'n_rev', u'stars']
    return list(df.columns) == header


def read_csv():
    r = re.compile('dump_csv-\d{8,8}\.csv')
    data_frames = []
    for f in glob('*.csv'):
        assert r.match(f), '[file name error]'

        df = pd.read_csv(f, encoding='utf-8')
        assert test_header(df), '[columns error]'

        df = df.set_index([[pd.to_datetime(f[9:-4])] * len(df)])
        data_frames.append(df)

    return pd.concat(data_frames)


def draw(df):
    colors = itertools.cycle(palette[20])
    tools = 'hover'
    p = figure(title='Differences of reveiw-counts: my favorite comic titles',
               tools=tools, x_axis_type='datetime',
               plot_width=800, plot_height=400)
    for t, color in itertools.izip(df['title'], colors):
        diffs = df[df.title == t]['n_rev'].diff()
        diffs[diffs < 2] = 0
        if all(diffs < 5):
            continue
        source = ColumnDataSource(
                data={'x': diffs.index, 'y': diffs,
                      'title': [t] * len(diffs),
                      'date': diffs.index.format(),
                      'rev': df[df.title == t]['n_rev'],
                      'pubd': df[df.title == t]['pub_date'].fillna('-'),
                      'star': df[df.title == t]['stars'].fillna(0.0),
                      'vol': df[df.title == t]['vol']})
        p.line('x', 'y', source=source, color=color)
        p.select(HoverTool).tooltips = [('Date', '@date'),
                                        ('Title', '@title'),
                                        ('Vol. ', '@vol'),
                                        ('Stars', '@star'),
                                        ('Review count', '@rev'),
                                        ('Publish Date', '@pubd')]
    p.toolbar_location = None
    show(p)


if __name__ == '__main__':
    df = read_csv()
    draw(df)
