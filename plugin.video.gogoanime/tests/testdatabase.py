# -*- coding: utf-8 -*-
import os
import sqlite3
from bs4 import BeautifulSoup
import re
import requests
import urlparse

class InternalDatabase:
    _connection = None
    _cursor = None
    _database = '../resources/data/anime.db'

    @classmethod
    def add(cls, values):
        cls._cursor.execute('INSERT INTO anime VALUES (?, ?, ?, ?, ?, ?, ?)', values)

    @classmethod
    def connect(cls):
        if cls._connection is None:
            cls._connection = sqlite3.connect(cls._database)
            cls._connection.text_factory = str
            cls._cursor = cls._connection.cursor()
            cls._cursor.row_factory = sqlite3.Row
            cls.create()

    @classmethod
    def close(cls):
        if cls._connection is None:
            return

        cls._connection.commit()
        cls._cursor.close()
        cls._connection.close()
        cls._connection = None

    @classmethod
    def create(cls):
        cls._cursor.execute('CREATE TABLE IF NOT EXISTS anime ('
                            'path TEXT PRIMARY KEY ON CONFLICT IGNORE, '
                            'poster TEXT, '
                            'title TEXT, '
                            'plot TEXT, '
                            'genre TEXT, '
                            'status TEXT, '
                            'year SMALLINT)')

    @classmethod
    def fetchone(cls, path):
        cls._cursor.execute('SELECT * FROM anime WHERE path = ?', (path,))
        result = cls._cursor.fetchone()

        if result is None:
            return None
        else:
            result = dict(result)
            result.pop('path')
            return result

def saveAnimeDetail(path):
    drama = InternalDatabase.fetchone(path)

    if drama is None:
        response = request(path)
        document = BeautifulSoup(response.content, 'html.parser')
        element = document.find('div', {'class': 'details'})
        year = document.find('span', text='Released:').find_next_sibling('a').text
        InternalDatabase.add((path,
                              element.find('img').attrs['src'],
                              element.find('h1').text,
                              element.find('span', text=re.compile('Description:?')).parent.find_next_sibling().text,
                              document.find('span', text=re.compile('Country: ?')).next_sibling.strip(),
                              document.find('span', text='Status:').find_next_sibling('a').text,
                              int(year) if year.isdigit() else None))
        drama = InternalDatabase.fetchone(path)

    return drama

page = 1
InternalDatabase.connect()
while page < 60:
    print ("Page: "+ str(page))
    response = requests.get("https://www2.gogoanime.video/anime-list.html?page="+str(page))
    document = BeautifulSoup(response.text, 'html.parser').find('div', class_="anime_list_body")
    for li in document.find_all('li'):
        document2 = BeautifulSoup(li['title'].encode('utf-8'), 'html.parser')
        img = document2.find('img')['src'].encode('utf-8').strip()
        title = document2.find('a', class_="bigChar").string.encode('utf-8').strip()
        print('Title: '+ title)
        pList = document2.find_all('p', class_="type")
        genre = ""
        for a in pList[0].find_all('a'):
            genre += a.string.encode('utf-8')
        try:
            year = pList[1].contents[1].encode('utf-8').strip()
            year = int(year) if year.isdigit() else None
        except IndexError:
            year = None
        
        status = pList[2].contents[1].encode('utf-8').strip()
        plot = document2.find('p', class_="sumer").contents[1].encode('utf-8').strip()
        path = li.find('a')['href']
        InternalDatabase.add((path, img, title, plot, genre, status, year))
    page += 1

InternalDatabase.close()