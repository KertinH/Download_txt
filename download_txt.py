import requests
import random
from urllib import parse
from lxml import etree
# from selenium import webdriver
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException#用来处理超时异常

user_agent = [
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
]


# def search_book(book_name):
#     '''输入需要搜索的书名，并返回搜索到的页面
#        （selenium版）'''
#
#     option = webdriver.ChromeOptions()
#     option.add_argument('headless')
#     prefs = {"profile.managed_default_content_settings.images": 2}
#     option.add_experimental_option("prefs", prefs)
#     browser = webdriver.Chrome(chrome_options=option)  # 启用静默模式（不显示界面），且不加载图片
#     waite = WebDriverWait(browser, 10)  # 设置等待时间
#     print('搜索中')
#     try:
#         browser.get('https://www.biquge5200.com')
#         # 用来输入搜索内容
#         input = waite.until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "#wd"))  # 用css_selector检索
#         )
#         # 用来点击搜索
#         submit = waite.until(
#             EC.element_to_be_clickable((By.XPATH, "//*[@id='sss']"))
#         )
#         time.sleep(1)  # 留一点反应时间，顺便做一个防ban措施
#         input.send_keys(book_name)
#         submit.click()
#         time.sleep(1)
#         url = browser.current_url
#         return requests.get(url)
#     except TimeoutException:
#         print('啊哦，网络出了点小问题，重新加载中...')
#         browser.close()
#         return


def search_book(book_name):
    '''搜书，返回搜索到的页面
       （requests版）'''

    url = 'https://www.biquge5200.com/modules/article/search.php?searchkey={}'
    response = requests.get(url.format(parse.quote_plus(book_name)), headers = {'User-Agent':random.choice(user_agent)}, timeout=10)
    return response


def choice_author(book_name):
    '''网站内有同名书籍，则返回同名书籍列表，并让用户选择作者（保证唯一性），返回书籍链接
       否则返回提示无此书籍，返回空值'''

    response = search_book(book_name)
    response = etree.HTML(response.content.decode('gbk'))
    list = response.xpath("//table/tr/td[@class='odd']/a[text()='%s']" % book_name)
    if list != []:
        for li in list:
            print(li.xpath("text()")[0],'          ',li.xpath("../../td[@class='odd'][2]/text()")[0])
        print('以上是为您搜索到的同名书籍')
        author = input('请输入作者名称 >')
        url = response.xpath("//table/tr/td[@class='odd'][text()='%s']/../td[@class='odd']/a[text()='%s']/@href" % (author, book_name))
        if url:
            return url[0]
        else:
            print('抱歉，笔趣阁内暂时找不到您搜索的书籍')
            exit()
    else:
        print('抱歉，笔趣阁内暂时找不到您搜索的书籍')
        exit()


def trim_article(url):
    '''修整书籍格式并下载'''

    count = 1
    res = requests.get(url, headers = {'User-Agent':random.choice(user_agent)}, timeout=10)
    res = etree.HTML(res.content.decode('gbk'))
    chapter_url = res.xpath("//*[@id='list']/dl/dd/a/@href")[9:]
    for u in chapter_url:
        response = requests.get(u, headers = {'User-Agent':random.choice(user_agent)}, timeout=10)
        response = etree.HTML(response.content.decode('gbk'))
        chapt_name = response.xpath("//div[@class='bookname']/h1/text()")
        if chapt_name:
            chapt_name = chapt_name[0]
            txt = response.xpath("//*[@id='content']/p/text()")
        else:
            chapt_name = response.xpath("//*[@id='content']/div[1]/text()")[0]
            txt = response.xpath("//div[@class='text']/text()")
        download_book(book_name, chapt_name, txt)
        if count == len(chapter_url):
            print('{} 100% 下载完毕'.format(book_name))
        else:
            print('已下载：',round(count / len(chapter_url) * 100,3),'%')
            count += 1


def download_book(book_name, chapt_name, txt):
    '''将书籍写入文本'''

    with open('book_list/{}.txt'.format(book_name), 'ab') as f:
        f.write(chapt_name.encode('utf-8'))
        f.write('\n\n'.encode('utf-8'))
        if '　　' in ''.join(txt):
            f.write(''.join(txt).replace('　　', '\n\n    ').encode('utf-8'))
        elif '    ' in ''.join(txt):
            f.write(''.join(txt).replace('    ', '\n\n    ').encode('utf-8'))
        f.close()


if  __name__ == '__main__':
    book_name = input('请输入书名 >')
    trim_article(choice_author(book_name))
