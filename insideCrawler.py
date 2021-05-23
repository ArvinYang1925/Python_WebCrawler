from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import pymysql.cursors

# database connection
connection = pymysql.connect(host='localhost', user='root', password='ccdd1111', db='new_media', cursorclass=pymysql.cursors.DictCursor)

options = Options()
driver = webdriver.Chrome(os.getcwd()+"/chromedriver", options=options)

# Web Crawler
try:
    with connection.cursor() as cursor:
        driver.get('https://www.inside.com.tw/')
        page = BeautifulSoup(driver.page_source)
        postSection = page.select('div.post_list')[0]
        articles = postSection.select('div.post_list_item ')

        # print(articles)

        for article in articles:
            tag = article.select('a.post_category')[0].text
            title = article.select('a.js-auto_break_title')[0].text
            date = article.select('li.post_date')[0].text
            author = article.select('span.post_author')[0].text
            slide_tags = article.select('a.hero_slide_tag')
            slide_tags_string = ''
            # print(tag)
            # print(title)
            # print(date)
            # print(author)
            for slide_tag in slide_tags:
                slide_tags_string += slide_tag.text + ', '
            # print(slide_tags_string)
            # print(len(slide_tags_string))
            # print('-----------------------------------------')
            sql = '''
            INSERT INTO `new_media`.`inside` (`title`, `author`, `tag`, `date`, `slide_tags`)
            VALUES('{}', '{}', '{}', '{}', '{}')
            '''.format(title, author, tag, date, slide_tags_string)
            print(sql)
            cursor.execute(sql)
            connection.commit()
      
    connection.close()           
    driver.close()
except Exception as e:
    print(e)
    connection.close()  
    driver.close()


