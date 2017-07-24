#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

with open('keys.config') as f:
  key = json.load(f)
  value = key['token']

import urllib.request
source = 'newsweek'
request = urllib.request.Request('https://newsapi.org/v1/articles?' + 'source=' + source + '&' + 'sortBy=' + 'top' + '&' + 'apikey=' + value)

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
  print (a['title'])
  print (a['author'])
  url = a['url']
  print(url)
  print()
  print()

print (articles[0]['url'])
from bs4 import BeautifulSoup
response = urllib.request.urlopen(urllib.request.Request(articles[0]['url']))
html= response.read()
soup = BeautifulSoup(html, 'html.parser')
body = soup.find('div', class_='article-body')
print (body)
