import requests
from bs4 import BeautifulSoup, SoupStrainer
from bs4.element import Tag


response = requests.get('http://music.163.com/discover/playlist/?cat=%E5%8D%8E%E8%AF%AD')
# 首页html内容
text = response.text
only_new_wrap = SoupStrainer(name='a', attrs={'data-order': 'new'})
soup_new = BeautifulSoup(text, 'lxml', parse_only=only_new_wrap)

print(soup_new('a')[0].get('href'))

