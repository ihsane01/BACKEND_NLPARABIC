from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
# selenium 3
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType


PATH="C:\Program Files (x86)\chromedriver.exe"
#driver = webdriver.Chrome(PATH)
driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

driver.get("https://www.nzraty.com/%D8%A7%D8%B3%D8%A6%D9%84%D8%A9-%D8%AA%D8%A7%D8%B1%D9%8A%D8%AE%D9%8A%D8%A9-%D8%B9%D9%86-%D8%A7%D9%84%D9%85%D8%BA%D8%B1%D8%A8/")

try:
    # element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "article-body"))
    # )
    element = driver.find_element(By.CLASS_NAME, "article-body")
  

   #find the ul element within the div using XPath
    ul_element = element.find_elements("xpath",'.//ul')
    p_element = element.find_elements("xpath",'.//p')
    
    ul_element1=ul_element[1:]
    p_element1 = p_element[3:]
    data=[]
    for i in range(len(ul_element1)):
        QR={}
        #li=ul.find_element("xpath",'.//li')
        #print(li.text)
        #questions.append(li.text)
        QR['question']=ul_element1[i].text
        QR['reponse']=ul_element1[i].find_element("xpath","following-sibling::*[1]").text
        data.append(QR)
finally:
    driver.quit()