#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:05:43 2019

@author: elyhabaro
"""
import time
import requests
import csv
import pandas as pd


# Input request from the user to enter the project token and the starting URL
project_Tocken = input("Please enter project Token: ")
url = input("Please enter the start url: ")

#Prepare Project to run

params = {
  "api_key": "t6F8DkOTJP-N", # you can change the api key and use your api provided by the parsehub
  "start_url": url,
}

#run the project

r = requests.post("https://www.parsehub.com/api/v2/projects/"+project_Tocken+"/run", data=params) 
data = r.json()

#extract the run token
token = data['run_token']
print(token)

#Get the results of the running Project
#It takes sometime to fetch the results, thats why there sleep request

time.sleep(30) #The waiting time can be increased, it takes 40 minutes to scrape 200 pages
params = {
  "api_key": "t6F8DkOTJP-N",
  "format": "csv" #The format can be changed to JSON, change also the fileName veriable to JSON
}
#get the results
r = requests.get('https://www.parsehub.com/api/v2/runs/'+token+'/data', params=params)
print(r.text)
f = open('file.txt', 'w')
f.write(r.text)

#Save the extracted data to a CSV file 
fileName = input("Please enter the file name: ")
fileName=fileName+'.csv'
with open('file.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open(fileName, 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)
#Compare the extracted data with the previous Data (both in excel sheets)
fileCompare = input("\n \033[1m Please enter the file you want to compare with: \033[0m ")       
f2 = pd.read_csv(fileName,encoding = "ISO-8859-1")
f1 = pd.read_csv(fileCompare,encoding = "ISO-8859-1")
xf1=f2[~f2.Name.isin(f1.Name)]
xf2=f1[~f1.Name.isin(f2.Name)]
if xf1.Name.count() > 0:
    print("\n \033[1m The new dapps added: "+str(xf1.Name.count())+" Dapps\033[0m \n")
    print(xf1)
else :
     print("\n \033[1m There is no new Dapps\033[0m \n")
if xf2.Name.count() > 0:
    print("\n \033[1m The removed dapps: "+str(xf2.Name.count())+" Dapps \033[0m \n")
    print(xf2)
else :
     print("\n \033[1m There is no removed Dapps\033[0m \n")
