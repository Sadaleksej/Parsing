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
# Будем использовать браузер Chrom
driver = webdriver.Chrome(options=options)
# Открываем ссылку
url_list=[]

driver.get('https://www.wildberries.ru')
wait = WebDriverWait(driver, 3)

input = wait.until(EC.presence_of_element_located((By.ID, "searchInput")))
# Вводим фразу поиска и нажимаем Enter
input.send_keys('стеклорез')
input.send_keys(Keys.ENTER)


    # Количество карточек на странице
count = None
while True:
    while True:
            time.sleep(2)
            # Ожидаем появление объекта (html код) карточек товара
            cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@class, "product-card j-card-item j-analitics-item")]/div[1]')))
            # Выходим из цикла, если при прокрутке страницы, количество товаров не меняется
            if len(cards) == count:
                break
                # Вычисляем сколько карточек товара на странице
            count = len(cards)
            # Прокручиваем страницу выполняя JAVA Script
            driver.execute_script('window.scrollBy(0, 1800)')
            time.sleep(2)

    # На полностью загруженной странице соберём информацию
    url_list_one = [card.find_element(By.XPATH, './a').get_attribute('href') for card in cards]
    url_list.extend(url_list_one)


    # Проверяем есть ли кнопка next
    try:
      
            next = driver.find_element(By.XPATH, '//a[@class = "pagination-next pagination__next j-next-page"]')
            next.click()
    except Exception:
            break
    time.sleep(5)

print(f'Всего получено: {len(url_list)} ссылок')
print(url_list)

time.sleep(10)


driver.close()

driver2 = webdriver.Chrome(options=options)
wait2 = WebDriverWait(driver2, 3)
books_list = []
n=0


# Просматриваем все ссылки на товары
for url_item in url_list:
    n+=1
    t=0
    books_dict = {}
  #  book_response = requests.get(url_item)
   
    driver2.get(url_item)
    # Заносим назание 
    time.sleep(3)

    books_dict['N']=n


    try:
        books_dict['name'] = wait2.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="product-page__title"]'))).text
        print(books_dict['name'])
    except Exception:
        try:
            books_dict['name'] = wait2.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="product-page__title product-page__title--long"]'))).text
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
    
    
    try:
        priceS=S[3].text.strip()
    except Exception:
        pass
    try:
        priceS=priceS.replace('&nbsp;','')
    except Exception:
        pass
    try:
        priceS=priceS.replace('\xa0','')
    except Exception:
        pass
    try:
        priceS=priceS.replace(' ','')
    except Exception:
        pass
    
    #Переводим цену в формат Float
    try:
        books_dict['price'] = float(priceS[:-1])  
    except Exception:
        books_dict['price'] = priceS
    
    print(repr(books_dict['price']))
  
    
    books_dict['url'] = url_item
    
    #Парсим картинку и сохраняем ссылку на нее
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




    # Добавляем словарь в список товаров
    print(books_dict)
    books_list.append(books_dict)
    
   
driver2.close()

'''
 #сохраняем в JSON
with open('WBresult.json', 'w', encoding='utf-8') as json_file:
    json.dump(books_list, json_file, ensure_ascii=False, indent=4)
'''

#сохраняем в Excel
df = pd.DataFrame.from_dict(books_list)
print (df)
df.to_excel('ResultWB.xlsx')