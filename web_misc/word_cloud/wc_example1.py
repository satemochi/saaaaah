# -*- coding: utf-8 -*-
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def morphological_analysis(sentence):
    morphs = ""
    t = Tokenizer()
    for token in t.tokenize(sentence):
        if token.part_of_speech.split(',')[0] in u'名詞形容詞':
            morphs += ' ' + token.surface
    return morphs[1:]

def draw_wordcloud(morphemes):
    fp = r'C:\WINDOWS\Fonts\DFJHSGW5.ttc'
    wc = WordCloud(background_color='white', font_path=fp,
                   width=400, height=100).generate(morphemes)
    plt.imshow(wc)

if __name__ == '__main__':
    sentence = u'そこのイヌ。吾輩はネコである。すごいネコである。夏目漱石'
    morphemes = morphological_analysis(sentence)
    draw_wordcloud(morphemes)
    plt.savefig('wordcloud-neko.png', bbox_inches='tight')
    plt.show()
