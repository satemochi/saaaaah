import codecs
import json
import requests
from bs4 import BeautifulSoup


class suwalib():
    def __init__(self):
        self.__base_url = 'https://www.libnet-suwa.gr.jp'
        self.__login = '/Libsearch/Account/Login'
        self.__login += '?ReturnUrl=%2FLibsearch%2FMyPage%2FMyLendings%2FIndex'
        self.__logout = '/Libsearch/Account/Logout'

        self.__s = requests.Session()
        self.__data = self.__setup()

    def __setup(self):
        with open('id_pass.json', 'r') as f:
            data = json.load(f)
        r = self.__s.get(self.__base_url + self.__login)
        soup = BeautifulSoup(r.content, 'lxml')
        att = {'name': '__RequestVerificationToken'}
        data['__RequestVerificationToken'] = soup.find(attrs=att).get('value')
        return data

    def __logoff(self):
        self.__s.get(self.__base_url + self.__logout)

    def lendings(self, fname='suwa_lendings.txt'):
        print self.__s.cookies
        r = self.__s.post(self.__base_url + self.__login, self.__data)
        soup = BeautifulSoup(r.content, 'lxml')
        tab = soup.findAll("table", {"id": "ap-result-list"})[0].tbody
        with codecs.open(fname, 'w', 'shift_jis') as f:
            for row in tab.find_all('tr'):
                val = row.find_all('td')
                f.write(val[2].text[2:-3] + ': ' + val[6].text[20:-17] + '\n')
        self.__logoff()


if __name__ == '__main__':
    s = suwalib()
    s.lendings()
