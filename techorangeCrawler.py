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
        driver.get('https://buzzorange.com/techorange/')
        page = BeautifulSoup(driver.page_source)
        postSection = page.select('main.site-main')[0]
        articles = postSection.select('article.post')
        for article in articles:
            title = article.select('h4.entry-title')[0].text
            # title_name = title.select('a')[0]
            print(title)
      
    connection.close()           
    driver.close()
except Exception as e:
    print(e)
    connection.close()  
    driver.close()


