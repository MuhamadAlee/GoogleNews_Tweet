from bs4 import BeautifulSoup
import requests, urllib.parse, lxml

import warnings
warnings.filterwarnings("ignore")


class GoogleNews():

    def __init__(self):
      pass
      
    def get_latest_news(self,keyword):
        """
        this method just try to scrap latest news 
        from the google news based on the keyword.
        """

        all_news={'title': [],'date': [],'link': []}
        
        li_url="https://www.google.com/search?q="+keyword+"&tbas=0&tbs=qdr:h,sbd:1&tbm=nws&source=lnt&sa=X&ved=2ahUKEwiIka3ejM_2AhU-gs4BHeXEDpUQpwV6BAgBEB4&biw=1848&bih=980&dpr=1"
        
        page=requests.get(li_url, timeout=20)
        soup=BeautifulSoup(page.text,'lxml')
        links=soup.find_all('a')
        
        for link in links:
            if ("/url?q=http" in link['href']):
                lks=link['href'].replace("/url?q=","")
                lk=lks.split("&")[0]
                if lk not in all_news["link"]:
                    all_news["link"].append(lk)

        Titles=soup.find_all('h3')
        for title in Titles:
            if (title.text is not None):
                all_news["title"].append(title.text)

        Dates=soup.find_all('span')
        for date in Dates[8:-6]:
            if ("ago" in date.text):
                all_news["date"].append(date.text)

        all_news["link"]=all_news["link"][:-2]
        return all_news