#pip install selenium
#pip install webdriver-manager

# selenium 4
import os
import sys
import json
import html #html.escape(myHtml)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def google_search(kw):
    '''Input is any keyword, the function will return array of dict(title,link,des)'''
    RESULT_CONTENT_ID = 'rso'
    RESULT_TIMEOUT = 5
    
    rets = []
      
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://www.google.com/")
    
    driver.implicitly_wait(0.5)
    
    print("Put \"{}\" into search textbox and Enter...".format(kw))
    q = driver.find_element(by=By.XPATH,value="//input[@type='text']")
    if(not q):
      print("not found text {}".format(kw))
      return rets;
      
    q.send_keys(kw)
    q.send_keys(Keys.RETURN)
    try:
        element_present = EC.presence_of_element_located((By.ID, RESULT_CONTENT_ID))
        WebDriverWait(driver, RESULT_TIMEOUT).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")    
        
    print("query done form {}".format(kw))
    
   
    #waiting to get result 
    eparent = driver.find_element(by=By.ID,value=RESULT_CONTENT_ID)
    if(not eparent):
      print("not found id={}".format(RESULT_CONTENT_ID))
      return rets;    
      
    childrens = eparent.find_elements(By.XPATH,"./child::*")
    for erow in childrens:
      item = {}
     
      try:
        #find title from h3 below link
        eh3 = erow.find_element(By.XPATH,"descendant::a/h3")
        if(eh3):
          item['title'] = eh3.text.encode('utf-8')
            
          #link is h3's parent 
          ea = eh3.find_element(By.XPATH,"..")
          if(ea):
            item['link'] = ea.get_attribute('href')
            
            #find up 3 level check chilren more than 2 and this is short description :)
            #adiv = ea.find_element(By.XPATH,"../../..").find_elements(By.XPATH,"./child::*")
            ea = ea.find_element(By.XPATH,"..")
            for i in range(2):
              ea = ea.find_element(By.XPATH,"..")
              adiv = ea.find_elements(By.XPATH,"./child::*")
              if(len(adiv)>1):
                item['des'] = adiv[1].get_attribute("textContent").encode("utf-8")
                break
                
        rets.append(item)
            
      except Exception as err:
        #Some exception Unable to locate element: {"method":"xpath","selector":"descendant::a/h3"}
        #print(err) 
        continue
   
    #time.sleep(10)
    #driver.implicitly_wait(10)
    driver.quit()
    
    return rets


# entry  
args = sys.argv[1:]
rets = []
if(len(args)>0):
  rets = google_search(args[0])
else:
  rets = google_search('Chargebacks911')  

for item in rets:
  print(item)  