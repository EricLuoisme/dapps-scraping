#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:04:44 2019

@author: elyhabaro
"""

## TODO 25.07.2020: first entry (ad) appears sometimes but not always; needs to filter on rel="noopener external nofollow sponsored"; see workaround below

from common import *
import common

filename = common_get("dappRadar")
driver = common_start("https://dappradar.com/rankings")
tree, pagen = common_pagen(driver)
if pagen == -1:
  # CHANGE 24.11.2019
  #pagen = int(tree.xpath('//ul[@class="pagination-list"]/li[last()]')[0].text_content())
  pagen = int(tree.xpath('//ul[@class="pagination--list"]/li[last()]')[0].text_content())
  print("Crawl pages (auto):", pagen)

links = []
#time.sleep(5.0)

# FIXME: missing columns due to web page changes; requires one more click to find out?
#Volume7d= tree.xpath('.//div[@data-heading="Volume 7d"]/div/div[1]/text()')
#Txn7d= tree.xpath('.//div[@data-heading="Txs 7d"]/div/span/text()')

#Access each Dapp and extract more data
for x in range(-1, math.ceil(pagen) - 1):
  if x != -1:
    # CHANGE 24.11.2019
    nextpath = "//button[@class='pagination--next btn-primary']"
    #nextpath = "//button[@class='pagination-next']"
    #nextpathvisible = nextpath
    nextpathvisible = "//div[@data-heading='ID']/text()=" + str((x + 1) * 50 + 1)
    print("nextpage:", nextpathvisible)

    #nextp_button = driver.find_element_by_xpath(nextpath)
    try:
        nextp_button = WebDriverWait(driver, waittime).until(EC.element_to_be_clickable((By.XPATH, nextpath)))
    except:
        tree = html.fromstring(driver.page_source)
        print("nextpage: page load must have failed")
        print(tree.xpath("//div[@data-heading='ID']/text()"))
        exit(1)
    else:
        #print("nextpage: ok, clickable", nextp_button)
        print("nextpage: ok, clickable")
    driver.execute_script("arguments[0].scrollIntoView()", nextp_button)
    nextp_button.click()

    #actions = ActionChains(driver)
    #actions.move_to_element(nextp_button).click().perform()

    #try:
    #  nextp = driver.find_element_by_xpath(nextpath).click()
    #except:
    #  print("hickup")
    #  time.sleep(0.1)
    #  nextp = driver.find_element_by_xpath(nextpath).click()

    #element_present = EC.presence_of_element_located((By.XPATH, nextpathvisible))
    #try:
    #  WebDriverWait(driver, waittime).until(element_present)
    #except:
    #  tree = html.fromstring(driver.page_source)
    #  print("X", tree.xpath("//div[@data-heading='ID']/text()"))
    #  if tree.xpath(nextpathvisible):
    #    print("nextpage: assume page load succeeded")
    #  else:
    #    print("nextpage: page load must have failed")
    #    exit(1)
    #else:
    #  tree = html.fromstring(driver.page_source)
    r = 0.1
    rt = 0
    while r < 3:
      rt += r
      r *= 2
      time.sleep(r)
      tree = html.fromstring(driver.page_source)
      vis = tree.xpath(nextpathvisible)
      if vis:
        break
    print("nextpage status:", vis, "rt", rt)
    if not vis:
      print("nextpage: page load must have failed")
      driver.quit()
      exit(1)

  # CHANGE 05.11.2019
  #Name = tree.xpath('.//div[@class="column-flex column-name featured-dapp-name"]/@title')
  #Name.extend(tree.xpath('.//div[@class="table-dapp-name"]/text()'))
  #Category = tree.xpath('.//div[@class="column-flex column-category"]/a/span/text()')
  Name = []
  Name.extend(tree.xpath('.//span[@class="rankings-column__name--title"]/text()'))
  Category = tree.xpath('.//div[@class="rankings-column rankings-column__category"]/text()')
  Balance = tree.xpath('.//div[@data-heading="Balance"]/div/span[2]/text()')
  User = tree.xpath('.//div[@data-heading="Users 24h"]/span/text()')
  Volume24 = tree.xpath('.//div[@data-heading="Volume 24h"]/div[1]/text()')
  Txn24 = tree.xpath('.//div[@data-heading="Txs 24h"]/span/text()')

  # CHANGE 05.11.2019
  #platform = [x.split(" ")[1] for x in tree.xpath(".//div[@data-heading='Protocol']/text()")]
  platform = [x for x in tree.xpath(".//div[@data-heading='Protocol']/text()")]

  # CHANGE 05.11.2019
  #dapplinks = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//div[@class='column-flex column-name']/a")]
  # CHANGE 25.07.2020
  #dapplinks = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//a[@class='rankings-row']")]
  dapplinks = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//a[@class='rankings-row css-1p5cfpf']")]
  links.extend(dapplinks[0:])

  if len(Name) != len(Category) or len(Category) != len(Balance) or len(Balance) != len(User) or len(User) != len(Volume24) or len(Volume24) != len(Txn24) or len(Txn24) != len(platform):
    print("Crawl ERROR: lengths", len(Name), len(Category), len(Balance), len(User), len(Volume24), len(Txn24), len(platform))
    driver.quit()
    exit(1)

  dfpage = pd.DataFrame(list(zip(Name,Category,Balance,User,Volume24,Txn24,platform)), columns=['Name', 'category', 'Balance', 'User', 'Volume24', 'Txn24', 'platform'])
  print("Crawl DApps Index Length:", len(dfpage), "at index", x)

  if x == -1:
    df = pd.DataFrame()
  # 25.07.2020 workaround for random ads
  if len(dfpage) > len(dapplinks):
    df = df.append(dfpage[1:])
  else:
    df = df.append(dfpage[0:])

#dapplimit = int(50 * pagen / math.ceil(pagen))
dapplimit = int(50 * pagen)
print("Crawl DApps Total Length:", len(df), "capped at", dapplimit)
df = df[:dapplimit]
df.reset_index(inplace=True, drop=True)
## 25.07.2020 adjust limit
if dapplimit > len(df):
  dapplimit = len(df)
if not "nosocial" in sys.argv:
  print("Crawl DApps:", dapplimit, "with links", len(links))
  print("DApps:", df)
else:
  print("Skip crawling DApps.")

eachdapp = pd.DataFrame(columns=['github', 'facebook', 'twitter', 'telegram', 'medium', 'youtube', 'reddit', 'dappLink', 'smartContract'])
linkid = 0
backoff = 1
while linkid < dapplimit and not "nosocial" in sys.argv:
#for link in links[:dapplimit]:
    link = links[linkid]
    bailout = False
    print("DApp", link)
    driver.get(link)
    #WebDriverWait(driver, 1)
    tree = html.fromstring(driver.page_source)
    try:
        if is_element_present(driver, '//div[@data-original-title="GitHub"]'):
            Github = tree.xpath('//div[@data-original-title="GitHub"]/a/@href')[0]
        else:
            Github = 'null'
        if is_element_present(driver, '//div[@data-original-title="facebook"]'):
            facebook = tree.xpath('//div[@data-original-title="facebook"]/a/@href')[0]
        else:
            facebook = 'null'
        if is_element_present(driver, '//div[@data-original-title="twitter"]'):
            twitter = tree.xpath('//div[@data-original-title="twitter"]/a/@href')[0]
        else:
            twitter = 'null'   
        if is_element_present(driver, '//div[@data-original-title="telegram"]'):
            telegram = tree.xpath('//div[@data-original-title="telegram"]/a/@href')[0]
        else:
            telegram = 'null'  
        if is_element_present(driver, '//div[@data-original-title="medium"]'):
            medium = tree.xpath('//div[@data-original-title="medium"]/a/@href')[0]
        else:
            medium = 'null'   
        if is_element_present(driver, '//div[@data-original-title="reddit"]'):
            reddit = tree.xpath('//div[@data-original-title="reddit"]/a/@href')[0]
        else:
            reddit = 'null'  
        if is_element_present(driver, '//div[@data-original-title="youtube"]'):
            youtube = tree.xpath('//div[@data-original-title="youtube"]/a/@href')[0]
        else:
            youtube = 'null' 
    except:
        print("Bailout social:", link)
        Github = 'null'
        facebook = 'null'
        twitter = 'null'
        telegram = 'null'
        medium = 'null'
        reddit = 'null'
        youtube = 'null'
        bailout = True
    try:
        # CHANGE 05.11.2019
        #dappLink = tree.xpath('//div[@class="dapp-links"]/a/@href')[0]
        #smartContract = tree.xpath('//div[@class="card card-contracts"]/header/p/span/text()')[0]
        # CHANGE 25.07.2020
        #dappLink = tree.xpath('//a[@class="button is-primary article-page__cta"]/@href')[0]
        #smartContract = tree.xpath('//span[@class="tag"]/text()')[0]
        dappLink = tree.xpath('//a[@class="button article-page__cta"]/@href')[0]
        smartContract = tree.xpath('//div[@class="css-j0jyzn"]/text()')[0]
    except:
        print("Bailout smart contracts:", link)
        dappLink = ''
        smartContract = ''
        bailout = True

    if bailout and backoff < 10:
      print("Retry...")
      time.sleep(backoff)
      backoff *= 2
      continue
    linkid += 1
    backoff = 1
    eachdapp = eachdapp.append(pd.DataFrame([[Github,facebook,twitter,telegram,medium,youtube,reddit,dappLink,smartContract]], columns=eachdapp.columns))

eachdapp.reset_index(inplace=True, drop=True)
result = pd.concat([df, eachdapp], axis=1)
#print("DApps+Social:", result)

#Close and quit the chrome driver
driver.quit()

#Create folder to save figures and extracted data

os.mkdir(filename)
#os.makedirs(filename, exist_ok=True)

# A general describe of the extracted data

# TODO ERROR -- TypeError: unhashable type: 'list'
#result.describe(include=['object'])
#print(result) # alternative to the above

if "noplot" in sys.argv:
  print("Skip plotting.")
else:
  print("Plotting...")

  # number of DApps in each platform
  fig1 = plt.figure(1)
  result['platform'].value_counts().plot(kind='bar',title='number of DApps in each platform')
  fig1.tight_layout()
  fig1.savefig(filename+'/dappsPlatform.png',dpi=1000)
  plt.close(fig1)

  #number of DApps in each category
  fig2 = plt.figure(2)
  result['category'].value_counts().plot(kind='bar',title='number of DApps in each category')
  fig2.tight_layout()
  fig2.savefig(filename+'/dappsCategory.png',dpi=1000)
  plt.close(fig2)

  #Total DApps balance for each platform
  fig3 = plt.figure(3)
  result.Balance = (result.Balance.replace(r'[kMB]+$', '', regex=True).astype(float) * result.Balance.str.extract(r'[\d\.]+([kMB]+)', expand=False).fillna(1).replace(['k','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
  df1=result.groupby('platform', as_index=False)['Balance'].sum()
  plot = df1.plot(x='platform',kind='bar',title='Total DApps balance for each platform' )
  fig3 = plot.get_figure()
  fig3.tight_layout()
  fig3.savefig(filename+'/dappsBalance.png',dpi=1000)
  plt.close(fig3)

  #Active users per blockchain platform
  fig4 = plt.figure(4)
  result.User = (result.User.replace(r'[kMB]+$', '', regex=True).astype(float) * result.User.str.extract(r'[\d\.]+([kMB]+)', expand=False).fillna(1).replace(['k','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
  df2=result.groupby('platform', as_index=False)['User'].sum()
  plot= df2.plot(x='platform',kind='bar',title='Active users per blockchain platform' )
  fig4 = plot.get_figure()
  fig4.tight_layout()
  fig4.savefig(filename+'/dappsUsers.png',dpi=1000)
  plt.close(fig4)

  #Daily volume for each blockchain platform
  fig5 = plt.figure(5)
  result.Volume24 = (result.Volume24.replace(r'[kMB]+$', '', regex=True).astype(float) * result.Volume24.str.extract(r'[\d\.]+([kMB]+)', expand=False).fillna(1).replace(['k','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
  df3=result.groupby('platform', as_index=False)['Volume24'].sum()
  plot=df3.plot(x='platform',kind='bar',title='Daily volume for each blockchain platform' )
  fig5 = plot.get_figure()
  fig5.tight_layout()
  fig5.savefig(filename+'/dappsVolume24.png',dpi=1000)
  plt.close(fig5)

  #Weekly volume for each blockchain platform
  """
  fig6 = plt.figure(6)
  result.Volume7d = (result.Volume7d.replace(r'[kMB]+$', '', regex=True).astype(float) * result.Volume7d.str.extract(r'[\d\.]+([kMB]+)', expand=False).fillna(1).replace(['k','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
  df4=result.groupby('platform', as_index=False)['Volume7d'].sum()
  plot=df4.plot(x='platform',kind='bar',title='Weekly volume for each blockchain platform' )
  fig6 = plot.get_figure()
  fig6.tight_layout()
  fig6.savefig(filename+'/dappsVolume7d.png',dpi=1000)
  plt.close(fig6)
  """

  #Daily Txns for each blockchain platform
  fig7 = plt.figure(7)
  result.Txn24 = (result.Txn24.replace(r'[kMB]+$', '', regex=True).astype(float) * result.Txn24.str.extract(r'[\d\.]+([kMB]+)', expand=False).fillna(1).replace(['k','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
  df5=result.groupby('platform', as_index=False)['Txn24'].sum()
  plot=df5.plot(x='platform',kind='bar',title='Daily Txns for each blockchain platform' )
  fig7 = plot.get_figure()
  fig7.tight_layout()
  fig7.savefig(filename+'/dappsTxn24.png',dpi=1000)
  plt.close(fig7)

  #Weekly Txns for each blockchain platform
  """
  fig8 = plt.figure(8)
  result.Txn7d = (result.Txn7d.replace(r'[kMB]+$', '', regex=True).astype(float) * result.Txn7d.str.extract(r'[\d\.]+([kMB]+)', expand=False).fillna(1).replace(['k','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
  df6=result.groupby('platform', as_index=False)['Txn7d'].sum()
  plot=df6.plot(x='platform',kind='bar',title='Weekly Txns for each blockchain platform' )
  fig8 = plot.get_figure()
  fig8.tight_layout()
  fig8.savefig(filename+'/dappsTxn7d.png',dpi=1000)
  plt.close(fig8)
  """

  #Convert smart contracts column to integer 
  result['smartContract'] = result['smartContract'].astype(str)
  # 25.07.2020
  #result['smartContract'] = result['smartContract'].map(lambda x: x.lstrip("['").rstrip("']"))
  #result['smartContract'] = result['smartContract'].replace('', '0')
  result['smartContract'] = result['smartContract'].map(lambda x: x.split("\xa0")[0])
  result['smartContract'] = result['smartContract'].astype(int)

  #number of smart contracts for each blockchain platform
  fig9 = plt.figure(9)
  df7=result.groupby('platform', as_index=False)['smartContract'].sum()
  plot=df7.plot(x='platform',kind='bar',title='number of smart contracts for each blockchain platform' )
  fig9 = plot.get_figure()
  fig9.tight_layout()
  fig9.savefig(filename+'/smartcontracts.png',dpi=1000)
  plt.close(fig9)

#save the dataframe to spreadsheet file
#result.to_excel(filename+'/DappRadar.xlsx', index=False)
result.to_csv(filename+'/DappRadar.csv', index=False)

#compare the file with the previous file
today = date.today()
yesterday = today - timedelta(days=1)
yesterday=yesterday.strftime('%Y-%m-%d')
filepathY='dappRadar-'+yesterday
if os.path.exists(filepathY): 
    f2=pd.read_csv(filepathY+'/DappRadar.csv')
    #f2.columns=['Name','category','Balance','User','Volume24','Volume7d','Txn24','Txn7d','platform', 'github' ,'facebook','twitter','telegram','medium','youtube','reddit','dappLink', 'smartContract']
    f2.columns=['Name','category','Balance','User','Volume24','Txn24','platform', 'github' ,'facebook','twitter','telegram','medium','youtube','reddit','dappLink', 'smartContract']

    xf1=f2[~f2.Name.isin(result.Name)]
    xf2=result[~result.Name.isin(f2.Name)]
    if xf1.Name.count() > 0:
        print("\n \033[1m The new dapps added: "+str(xf1.Name.count())+" DApps\033[0m \n")
        print(xf1)
    else :
        print("\n \033[1m There is no new DApps\033[0m \n")
    if xf2.Name.count() > 0:
        print("\n \033[1m The removed dapps: "+str(xf2.Name.count())+" DApps \033[0m \n")
        print(xf2)
    else :
        print("\n \033[1m There is no removed DApps\033[0m \n")
else :
    print("There is no file to compare with")

print("Finished:", datetime.datetime.now().isoformat())
