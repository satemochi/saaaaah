# -*- coding: utf-8 -*-
import calendar
from pprint import pprint
from datetime import datetime
import sqlite3
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, show
from bokeh.io import gridplot
import pandas as pd


class comic_cal:
    def __init__(self, year=2017, month=4):
        self.__date_range = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        self.__month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.__year = year
        self.__month = month
        self.__xpos, self.__ypos, w = self.__calendar_framework()
        self.__fig = self.__init_figure(w)
        self.__titles = self.__set_titles()
        self.__colors = self.__set_colors()
        self.__src = self.__set_src()

    def __calendar_framework(self):
        c = calendar.Calendar(firstweekday=6)
        date, week = 1, 0
        pos_x, pos_y = [], []
        for d, day_of_the_week in c.itermonthdays2(self.__year, self.__month):
            if d != date:
                continue
            pos_x.append(self.__date_range[(day_of_the_week + 1) % 7])
            pos_y.append(str(week))
            date += 1
            if day_of_the_week == 5:
                week += 1
        return (pos_x, pos_y, week)

    def __init_figure(self, week):
        week_range = [str(w) for w in range(0, week+1)]
        t = str(self.__year) + ' ' + self.__month_name[self.__month - 1]
        p = figure(title=t, tools='hover', x_axis_location='above',
                   plot_width=800, plot_height=400,
                   x_range=self.__date_range,
                   y_range=list(reversed(week_range)))
        p.select(HoverTool).tooltips = [('Titles', '@t')]
        p.toolbar_location = None
        p.title.text_font_size = '20pt'
        p.xaxis.major_label_text_font_size = '13pt'
        p.axis.axis_line_color = None
        p.axis.major_tick_line_color = None
        p.grid.grid_line_color = None
        return p

    def __set_titles(self):
        conn = sqlite3.connect('../comics.db')
        c = conn.cursor()
        sql = 'SELECT title, volume, next_date FROM comics'
        titles = [""] * calendar.monthrange(self.__year, self.__month)[1]
        for t, v, nd in c.execute(sql).fetchall():
            if nd and nd not in u'未定':
                dt = pd.to_datetime(nd)
                if dt.year == self.__year and dt.month == self.__month:
                    titles[dt.day - 1] += t + u'(' + unicode(v+1) + u'), '
        conn.close()
        return titles

    def __set_colors(self):
        colors = ['green'] * calendar.monthrange(self.__year, self.__month)[1]
        for i, t in enumerate(self.__titles):
            if t:
                colors[i] = 'red'
        if datetime.today().month == self.__month:
            colors[datetime.today().day - 1] = 'orange'
        return colors

    def __set_src(self):
        return ColumnDataSource(
                data=dict(x=self.__xpos, y=self.__ypos,
                          d=[str(i) for i in range(1, len(self.__xpos)+1)],
                          t=self.__titles, c=self.__colors))

    def draw(self):
        self.__fig.rect('x', 'y', 0.9, 0.9, source=self.__src,
                        fill_alpha=0.25, color='c')

        text_props = {"source": self.__src,
                      "angle": 0,
                      "color": "black",
                      "text_align": "right",
                      "text_baseline": "bottom"}
        self.__fig.text(x='x', y='y', text='d', text_font_size="16pt",
                        **text_props)
        show(self.__fig)


if __name__ == '__main__':
    cc = comic_cal(2017, 5)
    cc.draw()
