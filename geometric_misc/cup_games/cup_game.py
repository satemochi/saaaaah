from math import log
from random import random, seed
from matplotlib import pyplot as plt
import pandas as pd


def greedy_strategy(df):
    print(df)
    plt.subplot()
    n, k = len(df), len(df.columns)
    ymax, cup_size, dt = log(n, 2) * 1.5, 0, 1e-2
    for i in range(k):
        cup_size = max(cup_size, df[ci(df, i)].sum(axis=1).max())
        if i > 0:
            draw(df, i, ymax, cup_size, dt)
            plt.savefig(f'cup_game_{str(i).zfill(2)}_1.png',
                        bbox_inches='tight')
        _process(df, i)
        # df = df.loc[:, ((df.columns == 0) | (df != 0).any(axis=0))]
        # Drop cols w/t all 0. https://stackoverflow.com/questions/21164910/
        if i > 0:
            draw(df, i, ymax, cup_size, dt)
            plt.savefig(f'cup_game_{str(i).zfill(2)}_2.png',
                        bbox_inches='tight')
    return cup_size


def ci(df, k):
    cols = list(df.columns)
    return cols[1:cols.index(k)+1] if k in cols else cols[1:]


def _process(df, k, epsilon=1e-2):
    remain, i = 1+epsilon, df[[0]+ci(df, k)].sum(axis=1).idxmax()
    for j in ci(df, k):
        if df.at[i, j] >= remain:
            df.at[i, j] -= remain
            remain = 0
        else:
            remain -= df.at[i, j]
            df.at[i, j] = 0
        if not remain:
            break


def draw(df, i, ymax, cup_size, dt):
    plt.cla()
    plt.gca().set_ylim(0, ymax)
    df[ci(df, i)].plot.bar(stacked=True, rot=True, legend=False, ax=plt.gca())
    plt.gca().plot([0-.5, len(df)+.5], [cup_size, cup_size], color='r')
    plt.gca().plot([0-.5, len(df)+.5], [(x:=log(len(df), 2)), x], color='g')
    plt.draw()
    plt.pause(dt)


def gen(k_rounds, n_cups, init_states=None):
    water = {0: [0]*n_cups} if init_states is None else {0: init_states}
    for i in range(k_rounds):
        d = sum(rv:=[random() for j in range(n_cups)])
        water[i+1] = [x / d for x in rv]
    return pd.DataFrame(water)


def _starting_states(n):
    return 


if __name__ == '__main__':
    print(pd.__version__)
    k, n, _ = 30, 10, seed(0)
    # df = gen(k, n)
    df = gen(k, n, [1-random() for i in range(n)])
    print(greedy_strategy(df))
    plt.show()
