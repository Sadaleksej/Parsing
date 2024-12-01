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
import pandas as pd

options = Options()
options.add_argument('start-maximized')
driver2 = webdriver.Chrome(options=options)
wait2 = WebDriverWait(driver2, 3)
books_list = []
n=0

url='https://fedresurs.ru/sfactmessages/3cb62f18-a408-4b20-a3ed-ac66fb645fe3'

# Просматриваем все ссылки на товары
while True:
    n+=1
    
    books_dict = {}
  #  book_response = requests.get(url_item)
   
    driver2.get(url)
    # Заносим назание 
    time.sleep(3)

   


    try:

        books_dict['name'] = wait2.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "headertext")]'))).text
        print(books_dict['name'])
    except Exception:
        books_dict['name'] = None 

    if books_dict['name'] != 'Заключение договора финансовой аренды (лизинга)':
        continue

    books_dict['N']=n
    try:
        books_dict['mess_num'] = wait2.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "d-flex align-items-center header-item")]/div[1]'))).text.split()[0]
        print(books_dict['mess_num'])
    except Exception:
        books_dict['mess_num'] = None    

    try:
        books_dict['mess_dat'] = wait2.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "d-flex align-items-center header-item")]/div[1]'))).text.split()[2]
        print(books_dict['mess_dat'])
    except Exception:
        books_dict['mess_dat'] = None    

    try:
        books_dict['contract'] = wait2.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "info-item-value")]'))).text
        print(books_dict['contract'])
    except Exception:
        books_dict['contract'] = None    

    try:
        total = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@class, "info-item-value")]')))
        books_dict['duration'] = total[1].text
        print(books_dict['duration'])
    except Exception:
        books_dict['duration'] = None 

    try:
        total = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@class, "info-item-value")]')))
        books_dict['client_name'] = total[3].text.split('\n')[0]
        books_dict['client_inn'] = total[3].text.split('\n')[2]
        print(books_dict['client_name'])
        print(books_dict['client_inn'])
    except Exception:
        books_dict['client_name'] = None
        books_dict['client_inn'] = None 

    books_list.append(books_dict)
    time.sleep(4000)        
'''    
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


#сохраняем в Excel
df = pd.DataFrame.from_dict(books_list)
print (df)
df.to_excel('ResultWB.xlsx')
'''