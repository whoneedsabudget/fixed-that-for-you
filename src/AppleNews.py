from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def replace_custom(url):
  '''Apple News embedded link extractor'''
  html_request = Request(url, headers={'User-Agent': 'Mozilla'})
  html_response = urlopen(html_request).read()

  html_soup = BeautifulSoup(html_response, 'html.parser')

  embedded_article_url = html_soup.find_all('span', class_="click-here")[0].parent.get('href')

  return f'{embedded_article_url}'
  

