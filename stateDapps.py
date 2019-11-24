#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 12:26:27 2019

@author: elyhabaro
"""

from common import *
import common

filename = common_get("stateDapps")
driver = common_start('https://www.stateofthedapps.com/rankings')
tree, pagen = common_pagen(driver)
if pagen == -1:
  pnumber = tree.xpath('//button[@class="button number last"]/span/text()')
  pagen = int(pnumber[0])

links = []

for x in range(-1, math.ceil(pagen) - 1):
  if x != -1:
    nextpath = "//div[@class='last-wrapper']/button"
    nextpathvisible = nextpath
    #nextpathvisible = "//div[@data-heading='ID']/text()=" + str((x + 1) * 50 + 1)
    print("nextpage:", nextpathvisible)
    nextp = driver.find_element_by_xpath(nextpath).click()
    element_present = EC.presence_of_element_located((By.XPATH, nextpathvisible))
    try:
      WebDriverWait(driver, waittime).until(element_present)
    except:
      tree = html.fromstring(driver.page_source)
      if tree.xpath(nextpathvisible):
        print("nextpage: assume page load succeeded")
      else:
        exit(1)
    else:
      tree = html.fromstring(driver.page_source)

  dappNAme = tree.xpath('.//h4[@class="name"]/a/text()')
  category = tree.xpath('.//div[@class="RankingTableCategory"]/a/text()')
  users = tree.xpath('.//div[@class="table-data col-dau"]/div[1]/span[1]/text()')
  Platform = tree.xpath('.//div[@class="RankingTablePlatform"]/a/text()')
  Devact = tree.xpath('.//div[@class="table-data col-dev"]/div[1]/span[1]/text()')
  Volume7d = tree.xpath('.//div[@class="RankingTableVolume"]/span[2]/text()')

  dapplinks = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//h4[@class='name']/a")]
  links.extend(dapplinks)

  if len(dappNAme) != len(category) or len(category) != len(users) or len(users) != len(Platform) or len(Platform) != len(Devact) or len(Devact) != len(Volume7d):
    print("Crawl ERROR: lengths", len(dappNAme), len(category), len(users), len(Platform), len(Devact), len(Volume7d))
    exit(1)

  dfpage = pd.DataFrame(list(zip(dappNAme,category,users,Platform,Devact,Volume7d)), columns=['dappNAme','category','users','Platform','Devact','Volume7d'])
  print("Crawl DApps Index Length:", len(dfpage), "at index", x)

  if x == -1:
    df = pd.DataFrame()
  df = df.append(dfpage)

dapplimit = int(50 * pagen / math.ceil(pagen))
df = df[:dapplimit]
df.reset_index(inplace=True, drop=True)
if not "nosocial" in sys.argv:
  print("Crawl DApps:", dapplimit)
  #print("DApps:", df)
else:
  print("Skip crawling DApps.")

eachdapp = pd.DataFrame(columns=['dappLink','Txn24','Txn7d','github', 'chat','facebook','blog','twitter','reddit','status', 'Date', 'license'])
#for link in links:
linkid = 0
backoff = 1
while linkid < dapplimit and not "nosocial" in sys.argv:
    link = links[linkid]
    bailout = False
    print("DApp", link)
    driver.get(link)
    tree = html.fromstring(driver.page_source)
    try:
      if is_element_present(driver, '//a[@title="Github"]'):
      #driver.find_element_by_xpath('//a[@title="Github"]'):
        Github = tree.xpath('//a[@title="Github"]/@href')
        Github = Github[0]
      else:
        Github = 'null'
      if is_element_present(driver, '//a[@title="Reddit"]'):
        Reddit = tree.xpath('//a[@title="Reddit"]/@href')
        Reddit = Reddit[0]
      else:
        Reddit = 'null'
      if is_element_present(driver, '//a[@title="Twitter"]'):
        Twitter = tree.xpath('//a[@title="Twitter"]/@href')
        Twitter = Twitter[0]
      else:
        Twitter = 'null'        
      if is_element_present(driver, '//a[@title="Blog"]'):
        Blog = tree.xpath('//a[@title="Blog"]/@href')
        Blog = Blog[0]
      else:
        Blog = 'null'     
      if is_element_present(driver, '//a[@title="Facebook"]'):
        Facebook = tree.xpath('//a[@title="Facebook"]/@href')
        Facebook = Facebook[0]
      else:
        Facebook = 'null'    
      if is_element_present(driver, '//a[@title="Chat"]'):
        Chat = tree.xpath('//a[@title="Chat"]/@href')
        Chat = Chat[0]
      else:
        Chat = 'null' 
    except:
        print("Bailout social:", link)
        Github = 'null'
        Reddit = 'null'
        Twitter = 'null'
        Blog = 'null'
        Facebook = 'null'
        Chat = 'null'
        bailout = True
    try:
      dappLink = tree.xpath('//div[@class="DappDetailBodyContentCtas"]/div/div[2]/a/@href')
      Txn24 = tree.xpath('//div[@class="module-wrapper -tier-4"]/div[2]/div/ul/li[1]/span[2]/text()')
      Txn7d = tree.xpath('//div[@class="module-wrapper -tier-4"]/div[2]/div/ul/li[2]/span[2]/text()')
      status = tree.xpath('//div[@class="DappDetailBodyContentModulesStatus"]/strong/text()')
      Date = tree.xpath('//div[@class="DappDetailBodyContentModulesSubmitted"]/strong/text()')
      Slicense = tree.xpath('//p[@class="license-data"]/text()')
    except:
      print("Bailout smart contracts:", link)
      dappLink = ''
      Txn24 = ''
      Txn7d = ''
      status = ''
      Date = ''
      Slicense = ''
      bailout = True

    if bailout and backoff < 10:
      print("Retry...")
      time.sleep(backoff)
      backoff *= 2
      continue
    linkid += 1
    backoff = 1
    eachdapp = eachdapp.append(pd.DataFrame([[dappLink[0],Txn24[0],Txn7d[0],Github,Chat,Facebook,Blog,Twitter,Reddit,status[0],Date[0],Slicense[0]]], columns=eachdapp.columns))
#Go back to the previous ranking page
#driver.get(currenturl)

eachdapp.reset_index(inplace=True, drop=True)
result = pd.concat([df, eachdapp], axis=1)
#print("DApps+Social:", result)

#Close and quit the chrome driver
driver.quit()

#df.reset_index(inplace=True, drop=True)
#eachdapp.reset_index(inplace=True, drop=True)
#result = pd.concat([df, eachdapp], axis=1)
#print(result)
##Close and quit the chrome driver
#driver.quit()

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

  fig1 = plt.figure(1)
  result['Platform'].value_counts().plot(kind='bar',title='number of DApps in each platform')
  fig1.tight_layout()
  fig1.savefig(filename+'/dappsPlatform.png',dpi=1000)
  # add plt.close() after you've saved the figure
  plt.close(fig1)

  #number of DApps in each category
  fig2 = plt.figure(2)
  result['category'].value_counts().plot(kind='bar',title='number of DApps in each category')
  fig2.tight_layout()
  fig2.savefig(filename+'/dappsCategory.png',dpi=1000)
  plt.close(fig2)

  #Status of the DApps
  fig3 = plt.figure(3)
  result['status'].value_counts().plot(kind='bar',title='Status of the DApps')
  fig3.tight_layout()
  fig3.savefig(filename+'/dappsStatus.png',dpi=1000)
  plt.close(fig3)

  #Used software license
  fig4 = plt.figure(4)
  result['license'].value_counts().head(10).plot(kind='bar',title='Used software license')
  fig4.tight_layout()
  fig4.savefig(filename+'/dappslicense.png',dpi=1000)
  plt.close(fig4)

  #Active users per blockchain platform
  result['users'] = result['users'].str.replace('-', '0')
  result['users'] = result['users'].str.replace(',', '').astype(int)
  df1=result.groupby('Platform', as_index=False)['users'].sum()
  fig5 = plt.figure(5)
  plot=df1.plot(x='Platform',kind='bar',title='Active users per blockchain platform')
  fig5 = plot.get_figure()
  fig5.tight_layout()
  fig5.savefig(filename+'/dappsUsers.png',dpi=1000)
  plt.close(fig5)

  #Development activity of the DApps in each platform
  result['Devact'] = result['Devact'].str.replace('-', '0')
  result['Devact'] = result['Devact'].str.replace(',', '').astype(int)
  df2=result.groupby('Platform', as_index=False)['Devact'].sum()
  fig6 = plt.figure(6)
  plot=df2.plot(x='Platform',kind='bar',title='Development activity of the DApps in each platform' )
  fig6 = plot.get_figure()
  fig6.tight_layout()
  fig6.savefig(filename+'/dappsActivity.png',dpi=1000)
  plt.close(fig6)

  #Weekly volume for each blockchain platform
  result['Volume7d'] = result['Volume7d'].str.replace('USD', '')
  result['Volume7d'] = result['Volume7d'].str.replace('-', '0')
  result['Volume7d'] = result['Volume7d'].str.replace(',', '').astype(int)
  df3=result.groupby('Platform', as_index=False)['Volume7d'].sum()
  fig7 = plt.figure(7)
  plot=df3.plot(x='Platform',kind='bar',title='Weekly volume for each blockchain platform' )
  fig7 = plot.get_figure()
  fig7.tight_layout()
  fig7.savefig(filename+'/dappsVolume.png',dpi=1000)
  plt.close(fig7)

  result['date'] = pd.to_datetime(result.Date)

  #Platform EOS
  df4=result.loc[result['Platform'] == 'EOS']
  df4['count']=1
  agg1 = df4.resample('M', on='date').sum()

  #Platform Ethereum
  df5=result.loc[result['Platform'] == 'Ethereum']
  df5['count']=1
  agg2 = df5.resample('M', on='date').sum()

  #Platform POA
  df6=result.loc[result['Platform'] == 'POA']
  df6['count']=1
  agg3 = df6.resample('M', on='date').sum()

  # Platform Steem
  df7=result.loc[result['Platform'] == 'Steem']
  df7['count']=1
  agg4 = df7.resample('M', on='date').sum()

  #Plot
  agg1['date'] = agg1.index.values
  agg2['date'] = agg2.index.values
  agg3['date'] = agg3.index.values
  agg4['date'] = agg4.index.values
  fig8, ax1 = plt.subplots(figsize=(16, 9))
  ax1.set_xlabel('Date')
  ax1.set_ylabel('number of new Dapps', color='k')
  ax1.plot(agg2['date'], agg2['count'], color='r', label='Ethereum')
  ax1.plot(agg1['date'], agg1['count'], color='b', label='EOS')
  ax1.plot(agg3['date'], agg3['count'], color='g', label='POA')
  ax1.plot(agg4['date'], agg4['count'], color='y', label='Steem')
  ax1.tick_params(axis='y', labelcolor='k')
  plt.xticks(rotation=90) 
  fig8.tight_layout()  # otherwise the right y-label is slightly clipped
  #plt.title('Comparison between Ethereum new DApps and new smart contracts ')
  plt.legend()
  fig8.savefig(filename+'/newDapps.png',dpi=1000)
  plt.close(fig8)

#save the dataframe to spreadsheet file
#result.to_excel(filename+'/StateDapps.xlsx', index=False)
result.to_csv(filename+'/StateDapps.csv', index=False)

#compare the file with a previous file (from the day before)
today = date.today()
yesterday = today - timedelta(days=1)
yesterday=yesterday.strftime('%Y-%m-%d')
filepathY='stateofthedapp-'+yesterday
if os.path.exists(filepathY): 
    f2=pd.read_csv(filepathY+'/StateDapps.csv')
    f2.columns=['dappNAme', 'category', 'users', 'Platform', 'Devact', 'Volume7d','dappLink','Txn24','Txn7d','github', 'chat','facebook','blog','twitter','reddit','status', 'Date', 'license']
    xf1=f2[~f2.dappNAme.isin(result.dappNAme)]
    xf2=result[~result.dappNAme.isin(f2.dappNAme)]
    if xf1.dappNAme.count() > 0:
        print("\n \033[1m The new dapps added: "+str(xf1.dappNAme.count())+" DApps\033[0m \n")
        print(xf1)
    else :
        print("\n \033[1m There is no new DApps\033[0m \n")
    if xf2.dappNAme.count() > 0:
        print("\n \033[1m The removed dapps: "+str(xf2.dappNAme.count())+" DApps \033[0m \n")
        print(xf2)
    else :
        print("\n \033[1m There is no removed DApps\033[0m \n")
else :
    print("There is no file to compare with")     

print("Finished:", datetime.datetime.now().isoformat())
