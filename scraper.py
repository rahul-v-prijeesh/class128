
from xml.dom.minidom import Element
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
import csv
#import pandas as pd
START_URL="https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser=webdriver.Chrome("Z:\chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

headers=["name","light_years_from_rearth","planet_mass",
"stellar_magnitude",
"discoverydate","hyperlink",
"planet_type","planetradius","orbitalradius","orbitalperiod","ECCENTRICITY"
]
planetdata=[]

def scrape():
    
    for i in range(0,428):
        soup=BeautifulSoup(browser.page_source,"html.parser")
        #check page number
        currentpagenumber=int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
        if currentpagenumber<1:
            browser.find_element(By.XPATH,value="//*[@id=primary_column]/footer/div/div/div/nav/span[2]/a").close
        elif currentpagenumber>1:
            browser.find_element(By.XPATH,value="//*[@id=primary_column]/footer/div/div/div/nav/span[1]/a").close
        else:
            break
        for ultag in soup.find_all("ul",attrs={"class","exoplanet"}):
            litags=ultag.find_all("li")
            templist=[]
            for index,litag in enumerate(litags):
                if index==0:
                    templist.append(litag.find_all("a")[0].contents[0])
                else:
                    try:
                        templist.append(litag.contents[0])
                    except:
                        templist.append("")
            #get hyperlink tag
            hyperlink_litag=litags[0]
            templist.append("https://exoplanets.nasa.gov"+hyperlink_litag.find_all("a",href=True)[0]["href"])
            planetdata.append(templist)
        browser.find_element_by_xpath("//*[@id=primary_column]/footer/div/div/div/nav/span[2]/a").click()
   # 

scrape()
newplanetdata=[]
def scrapemoredata(hyperlink):
    
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        templist=[]
        for trtag in soup.find_all("tr",attrs={"class":"fact_row"}):
            tdtags=trtag.find_all("td")
            for tdtag in tdtags:
                try:
                    templist.append(tdtag.find_all("div",attrs={"class","value"})[0].contents[0])
                except:
                    templist.append("")
        
        newplanetdata.append(templist)
    except:
        time.sleep(1)
        scrapemoredata(hyperlink)

#calling method
for index,data in enumerate(planetdata):
    scrapemoredata(data[5])
    print(f"scraping at hyperlink {index+1} completed")
print(newplanetdata[0:10])
finalplanetdata=[]
for index,data in enumerate(planetdata):
    newplanetdataelement=newplanetdata[index]
    newplanetdataelement=[elem.replace("\n","")for elem in newplanetdataelement]
    newplanetdataelement=newplanetdataelement[:7]
    finalplanetdata.append(data+newplanetdataelement)
with open("planet.csv",'w') as f:
        csvwriter=csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(finalplanetdata)