# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 23:18:04 2019

@author: nipa
"""

from bs4 import BeautifulSoup
import re
import requests
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

def create_sentences(text):
	pattern = r"[\।|\?|;]+"
	sentences = re.split(pattern, text.rstrip(pattern))
	sentences = "\n".join(sentence.strip() for sentence in sentences)
	if sentences[-1] != "\n":
		sentences += "\n"				
	return sentences

def crawl_prothom_alo(start_date_str, end_date_str):
	from datetime import datetime, timedelta
	base_url = "http://www.prothom-alo.com"
	archive_url = base_url+"/archive/"
	start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
	end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
	delta = end_date - start_date
	infile = open('NewsPaper/prothom_alo'+start_date_str+"_to_"+end_date_str+".txt", "a")
	for i in range(delta.days + 1):
		date = start_date + timedelta(days = i)
		url = archive_url+date.strftime("%Y-%m-%d")
		while url:
			print("reading url >>> "+url)
			html_content = requests.get(url, headers = headers).content
			soup = BeautifulSoup(html_content, "lxml")
			links = soup.findAll('a', {'class': 'link_overlay'}, href = True)
			for link in links:
				inner_html_content = requests.get(base_url+link['href'], headers = headers).content
				inner_soup = BeautifulSoup(inner_html_content, "lxml")
				articleBody = inner_soup.find('div', {'itemprop': 'articleBody'})
				if articleBody:
					headline = inner_soup.find('div', {'class': 'right_title'}).text
					print("headline >>> "+headline)
					infile.write(headline+"\n")
					infile.write(create_sentences(articleBody.text))
			
			pagination_div = soup.find('div', {'class': 'pagination'})
			url = None
			if pagination_div:
				next_page_link = pagination_div.find('a', {'class': 'next_page'}, href = True)
				if next_page_link:
					url = archive_url + next_page_link['href']
	infile.close()
		
if __name__ == '__main__':
	# crawl_prothom_alo("2017-03-08","2017-06-01")
	crawl_prothom_alo("2016-01-20","2016-06-01")
