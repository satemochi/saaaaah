# -*- coding: utf-8 -*-
import pandas as pd
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import getFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm


def set_up(fname='address.pdf'):
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3', isVertical=True))
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
    pdf = canvas.Canvas(fname)
    pdf.setPageSize((10*cm, 14.8*cm))
    return pdf


def draw_sample(pdf):
    img = Image.open('letter.jpg')
    pdf.drawInlineImage(img, 0, 0, width=10*cm, height=14.8*cm)


def draw_family(pdf, family):
    pdf.setFont('HeiseiMin-W3', 24)
    pdf.drawString(5.1*cm, 11*cm, family)


def draw_name1(pdf, name1):
    pdf.setFont('HeiseiMin-W3', 24)
    pdf.drawString(5.1*cm, 8*cm, name1 + u' 様')


def draw_name2(pdf, name2):
    pdf.setFont('HeiseiMin-W3', 24)
    pdf.drawString(4.1*cm, 8*cm, name2 + u' 様')


def draw_post(pdf, post):
    pdf.setFont('HeiseiKakuGo-W5', 24)
    w = getFont('HeiseiKakuGo-W5').stringWidth(post[0], 24) + 0.2*cm
    offset = 0
    for i, c in enumerate(post):
        if '-' in c:
            w /= 1.20
            offset = -0.25*cm
            continue
        pdf.drawString(4.5*cm + i*w + offset, 13*cm, c)


def draw_address1(pdf, address1):
    pdf.setFont('HeiseiMin-W3', 16)
    pdf.drawString(9.0*cm, 12*cm, address1)


def chinese_numeral(s):
    convert_table = {ord(u'0'): u'〇', ord(u'1'): u'一', ord(u'2'): u'二',
                     ord(u'3'): u'三', ord(u'4'): u'四', ord(u'5'): u'五',
                     ord(u'6'): u'六', ord(u'7'): u'七', ord(u'8'): u'八',
                     ord(u'9'): u'九', ord(u'-'): u'の'}
    return s.translate(convert_table)


def draw_address2(pdf, address2):
    pdf.setFont('HeiseiMin-W3', 16)
    pdf.drawString(8.25*cm, 11.0*cm, address2)


def draw_address3(pdf, address3):
    pdf.setFont('HeiseiMin-W3', 16)
    pdf.drawString(7.50*cm, 9.5*cm, address3)


if __name__ == '__main__':
    pdf = set_up()
    df = pd.read_csv('personal_information.tsv',
                     delimiter='\t', encoding='utf-8')

    for i, row in df.iterrows():
        if 'x' in row['printable']:
            continue
        draw_sample(pdf)
        draw_family(pdf, row[u'family'])
        draw_name1(pdf, row[u'name1'])
        if not pd.isnull(row[u'name2']):
            draw_name2(pdf, row[u'name2'])
        draw_post(pdf, row[u'post'])
        draw_address1(pdf, row[u'address1'])
        draw_address2(pdf, chinese_numeral(row[u'address2']))
        if not pd.isnull(row[u'address3']):
            draw_address3(pdf, row[u'address3'])
        pdf.showPage()
    pdf.save()
