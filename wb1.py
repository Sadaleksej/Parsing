from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import json
import re
import urllib.parse

options = Options()
# Запуск браузера с развернутым экраном
options.add_argument('start-maximized')

url_list =['https://www.wildberries.ru/catalog/201951733/detail.aspx']
#driver.close()

driver2 = webdriver.Chrome(options=options)
wait2 = WebDriverWait(driver2, 3)
books_list = []



# Просматриваем все ссылки на книги
for url_item in url_list:
    books_dict = {}
    book_response = requests.get(url_item)
    book_soup = BeautifulSoup(book_response.text, "html.parser")


    driver2.get(url_item)
    # Заносим назание 
    time.sleep(10)
    books_dict['name'] = wait2.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="product-page__title"]'))).text
    print(books_dict['name'])
    
    while True:
        try:
            books_dict['name1'] = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="price-block__wallet-price red-price"]')))
            break    
        except Exception:
            time.sleep(2)
            driver2.refresh()

    
    print(books_dict['name1'])

    priceS=books_dict['name1'][3].text.strip()

    try:
        priceS=priceS.replace('&nbsp;','')
    except Exception:
        print(priceS)
    try:
        priceS=priceS.replace('\xa0','')
    except Exception:
        print(priceS)


    #Переводим цену книги в формат Float
    try:
        books_dict['price'] = float(priceS[:-1])  
    except Exception:
        books_dict['price'] = priceS

    print(repr(priceS))



