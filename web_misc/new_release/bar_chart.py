# -*- coding: utf-8 -*-
from datetime import datetime
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.font_manager import FontProperties


def get_df(fname):
    df = pd.read_csv(fname, encoding='utf-8')
    df = df[df['n_rev'] >= 12].sort_values(by=['stars', 'n_rev'],
                                           ascending=[1, 1])
    return df

def config(df):
    fig, ax = plt.subplots(figsize=(6, 9), facecolor='white')
    ax.set_xlim([0, max(df['n_rev'])+50])
    ax.set_ylim([-1, len(df)])
    ax.set_yticks(range(len(df)))
    ax.tick_params(axis='x', which='both', bottom='off', top='off',
                   labelbottom='off')
    ax.tick_params(axis='y', which='both', right='off')

def draw_titles(df):
    fp = FontProperties(fname=r'C:\WINDOWS\Fonts\DFJHSGW5.ttc',
                        size=8, weight='bold')
    titles = [t + " (" + str(v) + ")" for t, v in zip(df['title'], df['vol'])]
    plt.gca().set_yticklabels(titles, fontproperties=fp)
    td = datetime.now()
    for i, p in enumerate(df['pub_date']):
        pd = datetime.strptime(p, '%Y/%m/%d')
        if (td - pd).days < 7:
            plt.gca().get_yticklabels()[i].set_color('r')
        elif (td - pd).days < 30:
            plt.gca().get_yticklabels()[i].set_color('g')
        elif (td - pd).days > 360:
            plt.gca().get_yticklabels()[i].set_color('#777777')

def draw_bar(df):
    plt.gca().barh(range(len(df)), df['n_rev'], align='center', edgecolor='k',
                   color=cm.hot(map(lambda c: (c-1)/4.0, df['stars'])))

def draw_info(df):
    fp = FontProperties(fname=r'C:\WINDOWS\Fonts\DFJHSGW5.ttc', size=8)
    for i, (r, s) in enumerate(zip(df['n_rev'], df['stars'])):
        info = str(r) + u"/☆" + str(s)
        plt.gca().text(r+2.5, i-0.3, info, color='b', fontproperties=fp)


def draw(df):
    config(df)
    draw_titles(df)
    draw_bar(df)
    draw_info(df)
    fname = 'nrev3b' + sys.argv[1][13:-3]+'png'
    plt.savefig(fname, dpi=200, bbox_inches='tight')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(0)
    df = get_df(sys.argv[1])
    draw(df)
#    plt.gcf().tight_layout()
#    plt.show()
