from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import csv
import os
import time

driver_path = "chromedriver.exe"
service = Service(driver_path)

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

base_url = "https://rpkip.knf.gov.pl/"

num_pages = 6
if(os.path.isfile('data.csv')):
    fp = open('data.csv', 'w')
    fp.close()


driver.get(base_url)

time.sleep(4)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "maintable_length")))
select_element = driver.find_element(By.NAME, "maintable_length")
select = Select(select_element)
select.select_by_value("10000")
time.sleep(6)

for page_number in range(1, num_pages + 1):

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "page-link")))

    javascript_code = "document.querySelector('.next').click();"
    driver.execute_script(javascript_code)
    
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "maintable_paginate")))
    
    page_html = driver.page_source

    time.sleep(1)
    soup = BeautifulSoup(page_html, 'html.parser')
    
    data = []
    table = soup.find('table', attrs={'class':'table table-bordered table-striped table-hover dataTable no-footer'})
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])


    f = open("data.csv", "a", encoding="utf-8")
    writer = csv.writer(f)
    for item in data:
        writer.writerow(item)
        
    f.close()
   

driver.quit()