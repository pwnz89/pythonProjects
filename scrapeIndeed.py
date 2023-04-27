from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time




options = Options()

#for rendering page strategy normal. no pictures, just structure normal eager none
options.page_load_strategy = 'normal'
#windowless browser
options.add_argument('--headless=new')
#no eventual logs like nedless errors
options.add_argument('--log-level=3')

service = Service(executable_path="/chromedriver.exe")
#sets driver with choosen options and Service, so path
driver = webdriver.Chrome(options=options, service=service)

listOfNames=[]
listOfLinks =[]
URL = 'https://de.indeed.com/Jobs?q=python&l=k%C3%B6ln&lang=en&vjk=f05a54abaec843a0'


count = 0
y = 0

def basicDataRetriever():
    global y 
    global url
    global count
    global soup
    
    #resets url to basic form(so addon wont repeat as[&start=10&start=20..30])
    url = URL
    #changes url as simple way for going to next page
    y = y+10
    addon = '&start='+str(y)
    url = url+addon
    count = count + 1


    #goes to site
    driver.get(url)
    time.sleep(3)
    #this works exacly like driver.page_content (gets whole site structure)
    pageSource = driver.execute_script('return document.documentElement.outerHTML')
    #parses page source
    soup = BeautifulSoup(pageSource, 'html.parser')
    
    #searches for all li elements
    for box in soup.find_all('li'):
        #searches for h2's with specified class
        for piece in box.find_all('h2', class_='jobTitle'):
            listOfNames.append(piece.text)
            #searches for links attached to choosen tags(h2)
            for link in piece.find_all('a', href=True):
                listOfLinks.append(link['href'])
        
    return soup
    return url




BigA = 0

#this should find how many pages there is and use number for x times to repeat code
def findAllPages():
    global BigA
    for thisDiv in soup.find_all('nav', class_="css-jbuxu0"):
        for everyA in thisDiv.find_all('a'):
            if len(everyA.text) > 0:
                everyA = int(everyA.text)
                if everyA > BigA:
                    BigA = everyA
                   
#to initialize whole code 
basicDataRetriever()
findAllPages()

#repeats code until last page scrapped 
while BigA > count:
    findAllPages()  
    basicDataRetriever()


    



driver.close()

#list of all job offers
#filtering available
q1 = 'python'
q2 = 'developer'
q3 = 'data'

for (a, b) in zip(listOfLinks, listOfNames):
    l = b.lower()
    # print(b,'link:','indeed.com'+a,'\n\n')
    if q1 in l or q2 in l or q3 in l:
        print(b,'link:','indeed.com'+a,'\n\n')
