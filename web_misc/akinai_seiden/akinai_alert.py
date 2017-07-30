# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL as SMTP
import json
import sys
import time
import schedule
import akinai_check


def sending(content=u"hello world"):
    with open("email_conf.json") as f:
        conf = json.load(f)
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = Header(u'あきない世傳 新刊情報', 'utf-8')
        msg['From'] = conf['sender']

        c = SMTP(conf['smtp_server'])
        c.set_debuglevel(False)
        c.login(conf['smtp_user'], conf['smtp_passwd'])
        try:
            c.sendmail(conf['sender'], conf['destination'], msg.as_string())
        finally:
            c.quit()
    except Exception, exc:
        sys.exit("mail failed; %s" % str(exc))


def checking():
    title, pub_date = akinai_check.check(u'あきない世傳　金と銀')
    if title != "":
        print "sending alert"
        content = u'「あきない世傳 金と銀」の新刊情報\n\n'
        content += title + '\n\n' + pub_date + '\n\n\n\n'
        content += '\t\tfrom windows10 via python\n'
        sending(content)
    else:
        print "no alert..."

if __name__ == '__main__':
    checking()
    schedule.every().monday.at('16:00').do(checking)
    while True:
        schedule.run_pending()
        time.sleep(1)
