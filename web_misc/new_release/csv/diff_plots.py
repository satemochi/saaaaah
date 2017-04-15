# -*- coding: utf-8 -*-
from glob import glob
import itertools
import re
import pandas as pd
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models import HoverTool, Range1d
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


def figure_env():
    p = figure(tools='hover', x_axis_type='datetime',
               plot_width=800, plot_height=450)
    p.select(HoverTool).tooltips = [('Title', '@title'),
                                    ('Vol. ', '@vol'),
                                    ('Logging Date', '@date'), 
                                    ('Publish Date', '@pubd'),
                                    ('Review count', '@rev'),
                                    ('Diff of reviews', '@y'),
                                    ('Stars', '@star')]
    p.toolbar_location = None
    return p


def get_diffs(df, t):
    diffs = df[df.title == t].groupby('vol')['n_rev'].diff()
    diffs = diffs.fillna(df[df.title == t]['n_rev'])
    diffs.iloc[0] = 0
    diffs[diffs < 2] = 0
    return diffs


def get_src(df, diffs, t):
    return ColumnDataSource(
            data={'x': diffs.index,
                  'y': diffs,
                  'title': [t] * len(diffs),
                  'date': diffs.index.format(),
                  'rev': df[df.title == t]['n_rev'],
                  'pubd': df[df.title == t]['pub_date'].fillna('-'),
                  'star': df[df.title == t]['stars'].fillna(0.0),
                  'vol': df[df.title == t]['vol']})


def draw(df):
    p = figure_env()
    colors = itertools.cycle(palette[20])
    ymax = 0
    for t, color in itertools.izip(set(df['title']), colors):
        diffs = get_diffs(df, t)
        ymax = max(diffs) if ymax < max(diffs) else ymax
        if all(diffs < 5):
            continue
        p.line('x', 'y', source=get_src(df, diffs, t), color=color)
    p.y_range = Range1d(0, ymax * 1.5)
    show(p)


if __name__ == '__main__':
    df = read_csv()
    draw(df)
