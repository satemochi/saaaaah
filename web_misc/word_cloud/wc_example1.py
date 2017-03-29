# -*- coding: utf-8 -*-
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def morphological_analysis(sentence):
    stop = [u'よう', u'こと', u'これ', u'それ', u'そこ', u'これ', u'ため',
            u'さん', u'もの', u'なり', u'みたい', u'ない', u'ここ', u'どこ',
            u'なに', u'たち', u'ただ', u'ところ', u'あと', u'とき', u'なく']
    morphs = ""
    t = Tokenizer()
    for token in t.tokenize(sentence):
        if token.part_of_speech.split(',')[0] in u'名詞形容詞':
            if token.surface not in stop:
                morphs += ' ' + token.surface
    return morphs[1:]

def draw_wordcloud(morphemes):
    fp = r'C:\WINDOWS\Fonts\DFJHSGW5.ttc'
    wc = WordCloud(background_color='white', font_path=fp, min_font_size=7,
                   width=800, height=200).generate(morphemes)
    plt.imshow(wc, interpolation='catrom')

if __name__ == '__main__':
    sentence = u'そこのイヌ。吾輩はネコである。すごいネコである。夏目漱石'
    morphemes = morphological_analysis(sentence)
    draw_wordcloud(morphemes)
    plt.savefig('wordcloud-neko.png', bbox_inches='tight')
    plt.show()
