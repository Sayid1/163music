import re
import time
import redis
import random
import pymysql
import requests
import threading
import threadpool
from bs4.element import Tag
from datetime import datetime
from bs4 import BeautifulSoup, SoupStrainer

USER_AGENTS = [
  "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
  "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
  "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
  "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
  "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
  "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
  "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
  "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
  "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
host = 'http://music.163.com'
url = "http://music.163.com/discover/playlist"
sheets = []
sheet_name_pattern = re.compile(r'tit.*f-thide')
sheet_author_pattern = re.compile(r'nm.*nm-icn.*f-thide')
current_page_pattern = re.compile(r'js-selected')
#redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
#redis_conn = redis.Redis(connection_pool=redis_pool)
#mysql_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='zm123456', db='163music', charset='utf8')
#cursor = None
thread_pool = threadpool.ThreadPool()



class crawlSheet(threading.Thread):
    def __init__(self, url, type_id):
        threading.Thread.__init__(self)
        self.url = url
        self.type_id = type_id

    def run(self):
        #默认是爬取热门
        crawl(self.url, self.type_id)
        # 最新
        only_new_wrap = SoupStrainer(name='a', attrs={'data-order': 'new'})
        soup_new = BeautifulSoup(text, 'lxml', parse_only=only_new_wrap)


def crawl(url, type_id):
    response = requests.get(url, headers={'user-agent': random.choice(USER_AGENTS)})
    # 首页html内容
    text = response.text
    # 设置只对歌单ul容器和分页进行解析
    only_hot_wrap = SoupStrainer(id=re.compile('(m-pl-container)|(m-pl-pager)'))
    # 热门s
    soup_sheets = BeautifulSoup(text, 'lxml', parse_only=only_hot_wrap)

    # 最新
    only_new_wrap = SoupStrainer(name='a', attrs={'data-order': 'new'})
    soup_new = BeautifulSoup(text, 'lxml', parse_only=only_new_wrap)
    if soup_new('a'):
        new_url = soup_new('a')[0].get('href')
        thread = crawlSheet('%s%s' % (host, new_url), type_id)
        thread.start()
        thread.join()


    # sheets.find_all('li') == sheets('li')
    for li in soup_sheets('li'):

        sheet = {'type_id': type_id}
        sheet['profile_url'] = li(name='img', class_='j-flag')[0]['src'] if li(name='img', class_='j-flag') else None
        sheet['players'] = li(name='span', class_='nb')[0].string if li(name='span', class_='nb') else None
        temp_name = li(name='a', class_=sheet_name_pattern)[0] if li(name='a', class_=sheet_name_pattern) else None
        if temp_name:
            sheet['name'] = temp_name.string
            sheet['url'] = '%s%s' % (host, temp_name['href'])

        temp_author = li(name='a', class_=sheet_author_pattern)[0] if li(name='a',
                                                                         class_=sheet_author_pattern) else None
        if temp_author:
            sheet['author'] = temp_author.string
            sheet['author_url'] = '%s%s' % (host, temp_author['href'])
        sheets.append(sheet)

    # 单独获取分页容器
    soup_pagination = soup_sheets(name='div', id='m-pl-pager')
    # 获取当前页的下一页
    if soup_pagination:
        soup_next = soup_pagination[0](class_=current_page_pattern)[0].find_next() if soup_pagination[0](class_=current_page_pattern) else None
        if 'js-disabled' not in soup_next['class']:
            next_url = host + soup_next['href']
            crawl(next_url, type_id)


def has_not_class_and_has_not_id(tag):
    return not tag.has_attr('class') and not tag.has_attr('id')


class carwlerSheet(threading.Thread):

    """
        根据歌单url爬取
        url:歌单url
    """
    def __init__(self, url, sheet_id):
        threading.Thread.__init__(self)
        self.url = url
        self.sheet_id = sheet_id

    def run(self):
        response = requests.get(url)
        text = response.text
        only_wrap = SoupStrainer(name='textarea')
        soup = BeautifulSoup(text, 'lxml', parse_only=only_wrap)

        textarea = soup(has_not_class_and_has_not_id)

        soupTextarea = BeautifulSoup(str(textarea), 'lxml')
        musics_json = soupTextarea('textarea')



def insertToDB(sql, params):
    #cursor.execute(sql, params)
    #id = cursor.lastrowid
    return 1



def main(url):
    """
    解析歌曲风格和类型  启动每个类型线程爬取
    :param url: 
    :return: 
    """
    response = requests.get(url, headers={'user-agent': random.choice(USER_AGENTS)})

    text = response.text
    only_wrap = SoupStrainer(name='dl', class_='f-cb')
    soup = BeautifulSoup(text, 'lxml', parse_only=only_wrap)
    threads = []

    for s in soup:
        if isinstance(s, Tag):
            style_name = s('dt')[0].get_text()
            style_id = insertToDB(sql='insert into t_music_style (name) values (%s)', params=style_name)
            for link in s('a'):
                type_name = link.get_text()
                type_id = insertToDB(sql='insert into t_music_type (style_id, name) values (%s, %s)', params=(style_id, type_name))
                """
                sheet_thread = crawlSheet('%s%s' % (host, link.get('href')), type_id)
                threads.append(sheet_thread)
                sheet_thread.start()
                sheet_thread.setDaemon(True)

    for thread in threads:
        thread.join()
                """


if __name__ == '__main__':
    print("开始：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    start = datetime.now()
    #cursor = mysql_conn.cursor()
    main(url)

    threads = []
    for sheet in sheets:

        sheet_id = insertToDB(sql='insert into t_music_sheet (type_id, name, url, profile_url, players) values (%s, %s, %s, %s, %s)',\
                   params=(sheet['type_id'], sheet['name'], sheet['url'], sheet['profile_url'], sheet['players']))
        thread = carwlerSheet(url=sheet['url'], sheet_id=sheet_id)
        threads.append(thread)
        thread.start()
        thread.setDaemon(True)

    for thread in threads:
        thread.join()

    #mysql_conn.commit()
    #cursor.close()
    #mysql_conn.close()

    end = datetime.now()
    print("程序执行时间（秒）：" + str((end - start).seconds))
    print("结束：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print(len(sheets))