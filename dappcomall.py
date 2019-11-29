from lxml import html
from selenium import webdriver
import time
import pandas as pd
import itertools

options = webdriver.ChromeOptions()
#options.binary_location = browserpath
options.add_argument('headless')
options.add_argument('window-size=1200x900')

driver = webdriver.Chrome("chromedriver", chrome_options=options)
driver.get("https://www.dapp.com/search")

time.sleep(5)

for i in itertools.count():
	print("load page", i)
	vms = driver.find_elements_by_xpath('.//section[@class="view-more"]')
	if not len(vms):
		break
	vm = vms[0]
	vm.click()
	time.sleep(5)

tree = html.fromstring(driver.page_source)
links = tree.xpath(".//div[@class='item item']/a/@href")
names = tree.xpath(".//div[@class='item item']/a/div[@class='name']/text()")
cats = tree.xpath(".//div[@class='item item']/a/div[@class='extra-info']/div[@class='extra-name']/text()")[::2]

df = pd.DataFrame()
df["links"] = links
df["names"] = names
df["cats"] = cats

df.to_csv("dappcomall.csv", index=False)
print("done", len(df), "entries")
