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

Inn = str(input('Введите ИНН: '))
Begin = str(input('Введите начальную дату интервала: '))
End = str(input('Введите конечную дату интервала: '))




options = Options()
# Запуск браузера с развернутым экраном
options.add_argument('start-maximized')
# Будем использовать браузер Chrom
driver = webdriver.Chrome(options=options)



link = 'https://fedresurs.ru/entities?searchString=' + Inn
# Открываем ссылку
print(link)
driver.get(link)
time.sleep(4)
window_before = driver.window_handles[0]


try:
      
        cl = driver.find_element(By.CLASS_NAME, 'u-card-result__wrapper')
        cl.click()
except Exception:
    print("Error1")

window_after = driver.window_handles[1]
driver.switch_to.window(window_after)
ll  = driver.current_url + '/publications'
driver.get(ll)
time.sleep(3)

next = driver.find_element(By.XPATH, '//input[@class="datepicker-range-wrap__input-field datepicker-range-wrap__input-field_from ng-untouched ng-pristine ng-valid"]')
time.sleep(3)
next.send_keys(Begin)
next.send_keys('2'+End[0])
next.send_keys(End)
time.sleep(3)
next = driver.find_element(By.XPATH, '//button[@class="el-button"]')

next.click()

wait = WebDriverWait(driver, 3)
url_list=[]


while True:
            time.sleep(2)
            # Ожидаем появление объекта (html код) карточек товара
            driver.execute_script('window.scrollBy(0, 4000)')
            try:
      
                    next = driver.find_element(By.XPATH, '//div[@class = "more_btn"]')
                    next.click()
            except Exception:
                   break


cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="underlined card-link"]')))
          
    # На полностью загруженной странице соберём информацию
url_list_one = [card.get_attribute('href') for card in cards]
url_list.extend(url_list_one)
  

print(f'Всего получено: {len(url_list)} ссылок')
print(url_list)

time.sleep(2)

driver.close()

driver2 = webdriver.Chrome(options=options)
wait2 = WebDriverWait(driver2, 3)
books_list = []
n=0


# Просматриваем все ссылки на товары
for url_item in url_list:

    
    
    books_dict = {}
  #  book_response = requests.get(url_item)
   
    driver2.get(url_item)
    # Заносим назание 
    time.sleep(1)

    try:

        books_dict['name'] = wait2.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "headertext")]'))).text
        print(books_dict['name'])
    except Exception:
        books_dict['name'] = None 

    if books_dict['name'] != 'Заключение договора финансовой аренды (лизинга)':
        continue
    
    n+=1
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
    # Добавляем словарь в список товаров
    print(books_dict)
    
    
   
driver2.close()


#сохраняем в Excel
df = pd.DataFrame.from_dict(books_list)
print (df)
df.to_excel('ResultFedres.xlsx')

