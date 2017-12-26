#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 17:30:54 2017

@author: gjacopo
"""

try: 
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

try:
    from urllib.parse import urljoin, urlparse
except:
    from urlparse import urljoin, urlparse

from bs4 import BeautifulSoup

from . import ESSpiderWarning, ESSpiderError
from . import settings

class Crawler():
	
    def __init__(self):
        return
		# self.all_links = [start_url]
    
    def parse_glossaries(self, **kwargs):
        url = "{}/{}".format(settings.SE_MAINURL, settings.GLOSSARIES_DOMAIN)
        print(url)
        
    def parse_themes(self, **kwargs):
        url = "{}/{}".format(settings.SE_MAINURL, settings.THEMES_DOMAIN)
        print("url={}".format(url))

class Spider():
	
	def __init__(self,start_url):
		self.all_links = [start_url]

	def parse_url(self, url, **kwargs):
		''' Parse url and turn to soup '''
		parser = kwargs.get('kwargs','html.parser') 
		if parser not in ('html.parser','html5lib','lxml'):
			raise ESSpiderError('unknown soup parser')        
		
		try:
			conn = urlopen(url)
			print("conn={}".format(conn))
			html = conn.read()
			print("html={}".format(html))
			soup = BeautifulSoup(html, parser)
			print("soup={}".format(soup))
			name = url.replace("/", "|")
			with open(name,"w") as f:
				f.write(html)
				f.close()
		except:
			print("Exception")
			soup = None
		
		return soup
		
	def extract_links(self,url,soup):
		"""Return a list of all urls for page
        """
		 
		parsed_uri = urlparse(url)
		domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

		good_links = []
		links = soup.find_all('a')
		for tag in links:
			link = tag.get('href',None)
			if link is not None:
				a = urljoin(url, link)		
				if domain in a:
					good_links.append(a)

		return good_links

	def remove_duplicates(self,x):
		
		no_dups = []
		for i in x:
			if i not in no_dups:
				no_dups.append(i)
				
		return no_dups

