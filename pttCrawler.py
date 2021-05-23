from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import csv
import pymysql.cursors

# database connection
connection = pymysql.connect(host='localhost', user='root', password='ccdd1111', db='new_media', cursorclass=pymysql.cursors.DictCursor)

# Program to get PTT Data

# Today's date
from datetime import date
today = date.today()
search_date = today.strftime('%-m/%d')
file_date = today.strftime('%-m-%d')

options = Options()
driver = webdriver.Chrome(os.getcwd()+"/chromedriver", options=options)


# Web Crawler
try:
    with connection.cursor() as cursor:
        # Store data as a csv file
        with open(file_date + 'data.csv', 'w', newline='', encoding='utf_8_sig') as csvfile:
            # Get data page index
            driver.get('https://www.ptt.cc/bbs/Stock/index.html')
            page = BeautifulSoup(driver.page_source)
            button = page.select('a.btn.wide')[1]
            x = button['href'].find('x') 
            dot = button['href'].find('.')
            index = button['href'][x+1:dot]
            # Get information about each pages
            for i in range(int(index)+1, int(index)-6, -1):
                driver.get('https://www.ptt.cc/bbs/Stock/index' + str(i) + '.html')
                sourceCode = BeautifulSoup(driver.page_source)
                metaSection = sourceCode.select('div.r-list-container')[0]
                sections = metaSection.select('div.r-ent')
                for section in sections:
                    title = section.select('div.title')[0].text
                    num = section.select('div.nrec')[0].text
                    author = section.select('div.author')[0].text
                    date = section.select('div.date') [0].text

                    title.strip()
                    if (title.startswith('[公告]')):
                        continue
                    
                    if (num.find('爆') != -1):
                        num = 100

                    if(date.strip() == search_date):
                        print(title)
                        print(num)
                        print(author)
                        print(date)
                        writer = csv.writer(csvfile)
                        writer.writerow([num, title, author, date])
                        sql = '''
                        INSERT INTO `new_media`.`ptt` (`title`, `num`, `author`, `date`)
                        VALUES('{}', '{}', '{}', '{}')
                        '''.format(title, num, author, date)
                        print(sql)
                        cursor.execute(sql)
                        connection.commit()

    connection.close()           
    driver.close()
except Exception as e:
    print(e)
    connection.close()  
    driver.close()


