from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import pymysql.cursors
import urllib.request

# database connection
connection = pymysql.connect(host='localhost', user='root', password='ccdd1111', db='new_media', cursorclass=pymysql.cursors.DictCursor)

options = Options()
driver = webdriver.Chrome(os.getcwd()+"/chromedriver", options=options)

# Web Crawler
try:
    with connection.cursor() as cursor:
        driver.get('https://technews.tw/')
        sourceCode = BeautifulSoup(driver.page_source)
        page = sourceCode.select('div#content')[0]
        articles = page.select('article.post')
        # print(page)
        for article in articles:
            title = article.select('h1.entry-title')[0].text
            date = article.select('span.body')[1].text
            tags = article.select('span.body')[2].select('a')
            iframe = article.select('iframe')[1]
            # like number from facebook
            response = urllib.request.urlopen(iframe.attrs['src'])
            iframe_soap = BeautifulSoup(response)
            fb_like = iframe_soap.select('span._5n6h')[0].text
            tags_string = ''
            print(title)
            print(date)
            for tag in tags:
                tags_string += tag.text + ', '
            print(tags_string)
            print(fb_like)
            sql = '''
            INSERT INTO `new_media`.`technews` (`title`, `date`, `tags`, `fb_like`)
            VALUES('{}', '{}', '{}', '{}')
            '''.format(title, date, tags_string, fb_like)
            print(sql)
            cursor.execute(sql)
            connection.commit()



        # title
        # date
        # tags

      
    connection.close()           
    driver.close()
except Exception as e:
    print(e)
    connection.close()  
    driver.close()


