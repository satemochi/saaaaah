# -*- coding: utf-8 -*-
from datetime import datetime
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.font_manager import FontProperties

if len(sys.argv) != 2:
    sys.exit(0)
#df = pd.read_csv('dump_csv-20170218.csv', encoding='utf-8')
df = pd.read_csv(sys.argv[1], encoding='utf-8')
df = df[df['n_rev'] >= 12].sort_values(by=['stars', 'n_rev'], ascending=[1, 1])

fig, ax = plt.subplots(figsize=(8, 10), facecolor='white')
ax.set_ylim([-1, len(df)])
ax.set_yticks(range(len(df)))
ax.tick_params(axis='x', which='both', bottom='off', top='off',
               labelbottom='off')
ax.tick_params(axis='y', which='both', right='off')

titles = [t + " (" + str(v) + ")" for (t, v) in zip(df['title'], df['vol'])]
fp = FontProperties(fname=r'C:\WINDOWS\Fonts\DFJHSGW5.ttc', size=9)
ax.set_yticklabels(titles, fontproperties=fp)
ax.barh(range(len(df)), df['n_rev'], align='center', edgecolor='black',
        color=cm.hot(map(lambda c: float(c-1)/4.0, df['stars'])))

td = datetime.now()
for i, (r, s, p) in enumerate(zip(df['n_rev'], df['stars'], df['pub_date'])):
    ax.text(r+2.5, i-0.3, str(r) + u"/☆" + str(s),
            color='blue', fontsize=9, fontweight='bold', fontproperties=fp)
    pd = datetime.strptime(p, '%Y/%m/%d')
    if (td - pd).days < 7:
        ax.get_yticklabels()[i].set_color('r')
    elif (td - pd).days < 30:
        ax.get_yticklabels()[i].set_color('g')

fig.tight_layout()
#plt.savefig('nrev3b0218.png', bbox_inches='tight')
plt.savefig('nrev3b' + sys.argv[1][13:-3]+'png', bbox_inches='tight')
#plt.show()
