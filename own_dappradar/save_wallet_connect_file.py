
options = webdriver.ChromeOptions()
options.binary_location = browserpath
options.add_argument('headless')
options.add_argument('window-size=1200x900')
driverPath = "/Users/pundix2022/Juypter Working Env" + '/chromedriver'
w_driver = webdriver.Chrome(driverPath, chrome_options=options)

base_url = "https://walletconnect.com/_next/data/aRXSWpAJWkU4OKVRaRxBv/registry.json?type=dapp"
base_file_name = "wallet_connect_page_"

for i in range(12):
    page_num = str(i + 1)
    req_url = base_url

    # concat when more than 1
    if i > 0:
        req_url = req_url + "&page=" + page_num

    # request
    w_driver.get(req_url)
    file = open(base_file_name + page_num + ".json", 'w')
    file.write(w_driver.find_element_by_xpath("/html/body").text)
    file.close()

print("<<< finished")

