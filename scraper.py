#import requests
from bs4 import BeautifulSoup

#res = requests.get('https://iga.in.gov/search?q=h')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("https://iga.in.gov/search?q=woman")
#print("Headless Firefox Initialized")

driver.implicitly_wait(2)
driver.find_element(By.CLASS_NAME, 'PaginationSelect_select__4bc2b')

select_element = driver.find_element(By.CLASS_NAME, 'PaginationSelect_select__4bc2b')
select = Select(select_element)
select.select_by_visible_text('100')

driver.implicitly_wait(2)
try:
  driver.find_element(By.CLASS_NAME, 'BaseResult_resultContainer__pgT+s')
except:
  x = 1

soup = BeautifulSoup(driver.page_source, 'html.parser')
pretty = soup.prettify()
#print(soup.prettify())

res = soup.find_all('div', class_='BaseResult_resultContainer__pgT+s')
for r in res:
  print(r.find_all('h6')[0].text)
  pdflink = f"https://iga.in.gov{r.find_all('a')[0]['href']}"
  print(r.find_all('p')[0].text)

  # pdf request

  driver2 = webdriver.Firefox(options=options)
  driver2.get(pdflink)
  #print("Headless Firefox Initialized")

  soup2 = BeautifulSoup(driver2.page_source, 'html.parser')
  #print(soup2.prettify())
  driver.implicitly_wait(2)
  try:
    driver.find_element(By.CLASS_NAME, 'BaseResult_resultContainer__pgT+s')
  except:
    x = 1

  print(soup2.find('a', class_='Menu_menuItem__Y4JS+ Menu_primary__Dj7Gh')['href'])

  #print(res[0].prettify())

  #driver.find_element(By.CLASS_NAME, 'BaseResult_resultContainer__pgT+s')

  driver2.quit()

  #soup = BeautifulSoup(res.content, 'html.parser')
  #print(soup.prettify())
