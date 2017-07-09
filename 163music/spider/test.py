
def main(url):
    """爬取歌单
    从网易云音乐的歌单首页开始爬取
    :return: 
    """
    response = requests.get(url, headers={'user-agent': random.choice(USER_AGENTS)})
    #首页html内容
    text = response.text
    #设置只对歌单ul容器和分页进行解析
    only_wrap = SoupStrainer(id=re.compile('(m-pl-container)|(m-pl-pager)'))
    #歌单s
    soup_sheets = BeautifulSoup(text, 'lxml', parse_only=only_wrap)

    #sheets.find_all('li') == sheets('li')
    for li in soup_sheets('li'):

        sheet = {}
        sheet['profile_url'] = li(name='img', class_='j-flag')[0]['src'] if li(name='img', class_='j-flag') else None
        sheet['players'] = li(name='span', class_='nb')[0].string if li(name='span', class_='nb') else None
        temp_name = li(name='a', class_=sheet_name_pattern)[0] if li(name='a', class_=sheet_name_pattern) else None
        if temp_name:
            sheet['name'] = temp_name.string
            sheet['url'] = '%s%s' % (host, temp_name['href'])

        temp_author = li(name='a', class_=sheet_author_pattern)[0] if li(name='a', class_=sheet_author_pattern) else None
        if temp_author:
            sheet['author'] = temp_author.string
            sheet['author_url'] = '%s%s' % (host , temp_author['href'])
        sheets.append(sheet)

    #单独获取分页容器
    soup_pagination = soup_sheets(name='div', id='m-pl-pager')
    #获取当前页的下一页
    soup_next = soup_pagination[0](class_=current_page_pattern)[0].find_next()
    if 'js-disabled' not in soup_next['class']:
        next_url = host + soup_next['href']
        main(next_url)
