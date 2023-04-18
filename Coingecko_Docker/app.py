from bs4 import BeautifulSoup as bts
import requests
import pandas as pd
import numpy as np
from IPython.display import display


url = 'https://www.coingecko.com/'
result = requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
soup = bts(result.text, 'html.parser')

def getAndParseURL(url):
    result = requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
    soup = bts(result.text, 'html.parser')
    return soup

PAGE = []
for page_list in range(1,51):
    PAGE.append('https://www.coingecko.com/?page='+ str(page_list))
    TITLE= []
PRICE= []
HOUR1=[]
HOUR24=[]
SEVENDAY=[]
VOLUME24=[]
MARKETCAP=[]
for product in PAGE[::]:
    soup =getAndParseURL(product)
   
    for title_all_page in soup.find_all("span",{"class":"lg:tw-flex font-bold tw-items-center tw-justify-between"}):
        try:
            TITLE.append(title_all_page.text.replace('\n',''))
        except:
            TITLE.append(np.nan)
            
    for price_all_page in soup.find_all("span",{"no-wrap"}):
        try:
            PRICE.append(price_all_page.text.strip()[1::].replace('.',''))
        except:
            PRICE.append(np.nan)
            
    for hour1_all_page in soup.find_all("td",{"class":"td-change1h change1h stat-percent text-right col-market"}):
        try:
            HOUR1.append(hour1_all_page.text.replace('%','').replace('\n',''))
        except:
            HOUR1.append(np.nan)
    
    for hour24_all_page in soup.find_all("td",{"class":"td-change24h change24h stat-percent text-right col-market"}):
        try:
            HOUR24.append(hour24_all_page.text.replace('%','').replace('\n',''))
        except:
            HOUR24.append(np.nan)  
    
    for sevenday_all_page in soup.find_all("td",{"class":"td-change7d change7d stat-percent text-right col-market"}):
        try:
            SEVENDAY.append(sevenday_all_page.text.strip().replace('%','').replace(',',''))
        except:
            SEVENDAY.append(np.nan)
    
    for volume24_all_page in soup.find_all("td",{"class":"td-liquidity_score lit text-right col-market"}):
        try:
            VOLUME24.append(volume24_all_page.text.strip().replace('$',''))
        except:
            VOLUME24.append(np.nan)
                            
    for marketcap_all_page in soup.find_all("td",{"class":"td-liquidity_score lit text-right col-market"}):
        try:
            MARKETCAP.append(marketcap_all_page.text.strip().replace('$',''))
        except:
            MARKETCAP.append(np.nan)

print("prepring dataframe")

df=pd.DataFrame(list(zip(TITLE,PRICE,HOUR1,HOUR24,SEVENDAY,VOLUME24,MARKETCAP)),columns=['TITLE','PRICE','HOUR1','HOUR24','SEVENDAY','VOLUME24','MARKETCAP'])

display(df)
