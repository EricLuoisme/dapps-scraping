import time

from selenium import webdriver
import pandas as pd
import datetime
import os
import os.path

pd.set_option('display.width', 150)
pd.set_option('display.max_rows', 199)
wait_time = 4
browser_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def common_start(dapp_site):
    """
    Simulation by using the chrome driver doing the request
    """
    print("Crawl date:", datetime.datetime.now().isoformat())
    print("Crawl executable:", browser_path)

    # Start chrome driver and load the page
    driver_path = os.path.dirname(os.path.abspath(__file__))

    # please make sure that you have installed the driver and its in the same file as the python code, otherwise change
    # the specified path ## Headless
    options = webdriver.ChromeOptions()
    options.binary_location = browser_path
    options.add_argument('headless')
    options.add_argument('window-size=1200x900')
    ###
    driver = webdriver.Chrome(driver_path + '/chromedriver', chrome_options=options)

    print("Crawl site:", dapp_site)
    driver.get(dapp_site)
    return driver


def req_save_file(driver, filepath, baseReqUrl, cateMap):
    """
    Do all request in cateMap and store them as json into .html file
    """

    today = datetime.datetime.now()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")

    for k, v in cateMap.items():
        filename = filepath + "/" + k + "_" + year + "-" + month + "-" + day + ".json"
        driver.get(baseReqUrl + v)
        time.sleep(1)

        file = open(filename, 'w')
        file.write(driver.find_element_by_xpath("/html/body").text)
        file.close()
        print(">>> finish store file:" + filename)
    return
