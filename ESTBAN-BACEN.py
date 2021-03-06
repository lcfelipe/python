from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

import re
import pandas as pd
from tabulate import tabulate
import os
from zipfile import ZipFile

def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = downloads.Manager.get().items_;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.file_url);
        """)

#launch url
url = "https://www4.bcb.gov.br/fis/cosif/estban.asp"

# create a new Chrome session
driver = webdriver.Chrome()
#driver.implicitly_wait(30)
driver.get(url)

selec = Select(driver.find_element_by_id('ESTBAN_MUNICIPIO'))
selec.select_by_index(0)
mesano = selec.first_selected_option
print (mesano.text)

baixar = driver.find_element_by_name('botCad')
baixar.click()

# waits for all the files to be completed and returns the paths
paths = WebDriverWait(driver, 120, 1).until(every_downloads_chrome)
print(paths)

driver.close()

a= str(paths)
caminho =a[12:-2]

# specifying the zip file name 
file_name = caminho
  
# opening the zip file in READ mode 
with ZipFile(file_name, 'r') as zip: 
    # printing all the contents of the zip file 
    zip.printdir()
    # extracting all the files 
    print('Extracting all the files now...') 
    zip.extractall(path='/Users/xxx/Downloads/') 
    print('Done!')