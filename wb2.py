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
import pandas as pd

options = Options()
# Запуск браузера с развернутым экраном
options.add_argument('start-maximized')

url_list =['https://www.wildberries.ru/catalog/116499448/detail.aspx']
#driver.close()

driver2 = webdriver.Chrome(options=options)
wait2 = WebDriverWait(driver2, 3)
books_list = []



# Просматриваем все ссылки на книги
for url_item in url_list:
    t=0
    books_dict = {}
    book_response = requests.get(url_item)
   
    driver2.get(url_item)
    # Заносим назание 
    time.sleep(10)
    try:
        books_dict['name'] = wait2.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="product-page__title"]'))).text
        print(books_dict['name'])
    except Exception:
        books_dict['name'] = None 
    
    while True:
        try:
            S = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//ins[@class="price-block__final-price red-price"]')))
            break    
        except Exception:
            try:
                S = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="price-block__wallet-price red-price"]')))
                break    
            except Exception:
                try:
                    S = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="price-block__wallet-price"]')))
                    break
                except Exception: 
                    try:
                        S = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//ins[@class="price-block__final-price"]')))
                        break
                    except Exception:  
                        if t == 12:
                            break
                        t+=1                    
                        time.sleep(2)
                        driver2.refresh()
    


    print(S)

    priceS=S[3].text.strip()

    try:
        priceS=priceS.replace('&nbsp;','')
    except Exception:
        print(priceS+'y1')
    try:
        priceS=priceS.replace('\xa0','')
    except Exception:
        print(priceS+'y2')
    try:
        priceS=priceS.replace(' ','')
    except Exception:
        print(priceS+'y3')
    
    #Переводим цену книги в формат Float
    try:
        books_dict['price'] = float(priceS[:-1])  
    except Exception:
        books_dict['price'] = priceS
    
    print(repr(books_dict['price']))
    
    n=777

    try:
        c = wait2.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "zoom-image-container")]')))
        image = c.find_element(By.XPATH, './img').get_attribute('src')
        print(image)
        img_data = requests.get(image)
        with open(f'C:/Users/rusla/OneDrive/Рабочий стол/GeekBrains/Parsing/Images/{n}.webp', 'wb') as handler:
            handler.write(img_data.content)
        books_dict['img_link'] = f'C:/Users/rusla/OneDrive/Рабочий стол/GeekBrains/Parsing/Images/{n}.webp'
        print(books_dict['img_link'])
    except Exception:
        image = None 
   
    books_list.append(books_dict)

df = pd.DataFrame.from_dict(books_list)
print (df)
df.to_excel('ResultWB.xlsx')
      