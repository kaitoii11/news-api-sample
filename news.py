#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import json
import urllib.request
import psycopg2

class News():
  newslist = []
  source = 'newsweek'

  def __init__(self):
    if not os.path.exists('keys.config'):
      import sys
      sys.exit('keys.config is missing!')
    with open('keys.config') as f:
      key = json.load(f)
      self.apikey = key['token']
      self.DBIP = key['DBIP']
      self.DBNAME = key['DBNAME']
      self.DBPORT = key['DBPORT']
      self.DBUSER = key['DBUSER']
      self.DBPASSWORD = key['DBPASSWORD']
      self.TABLENAME = key['TABLENAME']

  def store2DB(self):
    s= 'dbname={} host={} user={}  password={}'.format(self.DBNAME,self.DBIP,self.DBUSER,self.DBPASSWORD)
    print (s)
    conn = psycopg2.connect(s)
    cur = conn.cursor()
    for n in self.newslist:
      s = 'INSERT INTO {} (title, url, body, date) VALUES({}, {}, {}, current_timestamp);'.format(self.TABLENAME, json.dumps(n['title']), json.dumps(n['url']), json.dumps(n['body']))
      print (s)
      #cur.execute(s)
      #cur.fetchone()
    cur.execute("insert into sample(title, url, body, date) values('hoge\'s;, 'https://google.com', 'body'; ,current_timestamp);")
    cur.fetchone()

  def getBody(self, url):
      from bs4 import BeautifulSoup
      response = urllib.request.urlopen(url)
      html= response.read()
      soup = BeautifulSoup(html, 'html.parser')
      body = soup.find('div', class_='article-body')
      if body is None:
        return ''
      from bs4.element import NavigableString
      paras = [x.contents[0] for x in body.findAllNext('p') if len(x.contents) > 0 and isinstance(x.contents[0], NavigableString)]
      return ('\n\n'.join(paras))


  def getNewsList(self):
      request = urllib.request.Request('https://newsapi.org/v1/articles?' + 'source=' + self.source + '&' + 'sortBy=' + 'top' + '&' + 'apikey=' + self.apikey)

      try:
        response = urllib.request.urlopen(request)
        news = json.loads(response.read().decode('utf-8'))
      except:
        import traceback
        traceback.print_exc()
        import sys
        sys.exit()

      articles = news['articles']
      for a in articles:
        n = {}
        n['title'] = a['title']
        n['url'] = a['url']
        n['body'] = self.getBody(a['url'])
        self.newslist.append(n)

      print(self.newslist)

if __name__ == '__main__':
  news = News()
  news.getNewsList()
  news.store2DB()
