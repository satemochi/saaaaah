# -*- coding: utf-8 -*-
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.font_manager import FontProperties


def draw(df, title):
    df = df.replace({0: None})
    cols = [u'☆1', u'☆2', u'☆3', u'☆4', u'☆5']
    ax = df[cols].plot.bar(rot=0, stacked=True,
                           colormap='Greens', legend=False)
    ax2 = ax.twinx()
    ax2.plot(df[['a_ratings']].values, c='r', alpha=0.4, lw=1.2)

    xtic = [0] + range(4, len(df) + 1, 5)
    plt.xticks(xtic, [str(i + 1) for i in xtic])
    ax.grid(True)

    ax.set_ylim([0, ax.get_yticks()[-1]])
    ax2.set_ylim([7 - len(ax.get_yticks()), 6])
    ax2.set_yticks(range(6))

    fp = FontProperties(fname=r'C:\WINDOWS\Fonts\DFJHSGW5.ttc', size=12)
    plt.title(title, fontproperties=fp)


if __name__ == '__main__':
    titles = [u'ワンピース', u'ナルト', u'ブラッククローバー',
              u'それでも町は廻っている', u'鬼滅の刃']

    for t in titles:
        print t
        csvname, figname = t + '-a2.csv', t + '-a2.png'
        if not os.path.exists(csvname) or os.path.exists(figname):
            continue
        df = pd.read_csv(csvname, index_col='vol', encoding='utf-8')
        draw(df, t)
        plt.savefig(figname, bbox_inches='tight')
        plt.close()
