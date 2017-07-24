#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

with open('keys.config') as f:
  key = json.load(f)
  value = key['token']

import urllib.request

request = urllib.request.Request('https://newsapi.org/v1/articles?' + 'source=' + 'the-next-web' + '&' + 'sortBy=' + 'latest' + '&' + 'apikey=' + value)

try:
  response = urllib.request.urlopen(request)
  news = json.loads(response.read().decode('utf-8'))
except URLError as e:
  print ('Error :', e)
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
