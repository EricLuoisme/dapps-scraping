# import the libraries : Selenium, pandas, lxml
from lxml import html
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import matplotlib.pyplot as plt
import datetime 
import os
import os.path
from datetime import date, timedelta
import sys
import math
import time

pd.set_option('display.width', 150)
pd.set_option('display.max_rows', 199)

def common_get(sitename):
  today = datetime.datetime.now()
  year = today.strftime("%Y")
  month = today.strftime("%m")
  day = today.strftime("%d")
  basepath = os.path.dirname(os.path.abspath(__file__))
  filename = basepath + "/" + sitename + "-"  + year + "-" + month + "-" + day

  if os.path.isdir(filename):
    print("Crawl ERROR: Directory exists", filename)
    exit(1)

  return filename

#Below function check if a certin element is in the page or not (it used for social media links)
def is_element_present(driver, what):
    try:
        driver.find_element(By.XPATH, value=what)
    except NoSuchElementException as e:
        return False
    return True

waittime = 4
browserpath = "/opt/google/chrome/google-chrome"

def common_start(dappsite):
  print("Crawl date:", datetime.datetime.now().isoformat())
  print("Crawl executable:", browserpath)
  #Start chrome driver and load the page
  driverPath = os.path.dirname(os.path.abspath(__file__))
  #please make sure that you have installed the driver and its in the same file as the python code, otherwise change the specified path 
  ### Headless
  options = webdriver.ChromeOptions()
  options.binary_location = browserpath
  options.add_argument('headless')
  options.add_argument('window-size=1200x900')
  ###
  driver = webdriver.Chrome(driverPath + '/chromedriver', chrome_options=options) 

  print("Crawl site:", dappsite)
  driver.get(dappsite)

  return driver

def common_pagen(driver):
  actions = ActionChains(driver)
  #Access the source page of the loaded page and extrct the required data based on the xpath
  tree = html.fromstring(driver.page_source)
  #currenturl = driver.current_url
  if len(sys.argv) < 2:
      print("No Arguments :)")
      #pnumber=tree.xpath('//ul[@class="pagination-list"]/li[last()]/a/text()') # FIXME: This returns an empty list; it works with the expression below
      #pagen=int(pnumber[0])
      #!!!pagen = int(tree.xpath('//ul[@class="pagination-list"]/li[last()]')[0].text_content())
      return tree, -1
  else:
      pagen = float(sys.argv[1])
      if pagen < 0:
          pagen = 0

  print("Crawl pages:", pagen)
  return tree, pagen
