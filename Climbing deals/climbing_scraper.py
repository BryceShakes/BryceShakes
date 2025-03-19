import pandas as pd
import requests
import time
import sys
import re
from bs4 import BeautifulSoup as bs
from IPython.display import display, HTML
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import warnings
warnings.filterwarnings("ignore")

class scraper:
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    @staticmethod
    def dict_to_df(dict):
        new = pd.DataFrame(dict)
        new.sort_values('pecentage_off', inplace =True, ascending = False)
        new.reset_index(drop=True, inplace = True)
        new['previous_price'] = new['previous_price'].apply(lambda x: "£{:.2f}".format((x)))
        new['price'] = new['price'].apply(lambda x: "£{:.2f}".format((x)))
        new['pecentage_off'] = new['pecentage_off'].apply(lambda x: "{:.0f}%".format(x))

        return new
        
    @staticmethod
    def display(df, show = 50):

        def path_to_image_html(path):
            return '<img src="'+ path + '" width="150" >'

        def make_clickable(val):
            # target _blank to open new window
            return '<a target="_blank" href="{}">{}</a>'.format(val, val)
    
        if isinstance(df, dict):
            df = scraper.dict_to_df(df)
        
        show = min(show, len(df))
        format_dict = {'img_link':path_to_image_html, 'item_link':make_clickable}
        display(HTML(df.head(show).to_html(escape=False, formatters=format_dict, index = False)))
        
    @staticmethod
    def bananafingers(pages = 99,
                      display = False,
                      dict = {
                          'item_name':[],
                          'price':[],
                          'pecentage_off':[],
                          'previous_price':[],
                          'img_link':[],
                          'item_link':[]}
                     ):
            
        for pg in range(1, pages + 1):
            url = f'https://bananafingers.co.uk/outlet?p={pg}' # loop through each outlet page
            page = requests.get(url, headers = scraper.headers) # call website
            if page.status_code != 200:
                page = requests.get(url, headers = scraper.headers) # try again
            if page.status_code != 200:
                page = requests.get(url, headers = scraper.headers) # try again again
            if page.status_code != 200:
                break # give up
            soup = bs(page.text, 'html.parser') # parse html into text
            if soup.find('div', class_ ='message info empty'): #stop if the returned html contains an empty warning (ran out of sale items)
                break
            all = soup.findAll('li', class_ = 'item product product-item') # find html class for sale items, gather all classes into list
        
            for i in all: # each sale item, get relevant info from html 
                pecentage_off = float(i.find('span').get_text().strip().replace('%', ''))
                dict['pecentage_off'].append(pecentage_off)
                dict['img_link'].append( i.find('img')['src'])
                dict['item_name'].append(i.find(class_='product-item-link').get_text().strip())
                dict['item_link'].append( i.find(class_='product-item-link')['href'])
                price = float(i.find(class_='price').get_text().strip('£'))
                dict['price'].append(price)
                dict['previous_price'].append(price / (1-(pecentage_off/100)))

        if display:
            scraper.display(dict)
        
        return dict

    @staticmethod
    def rockrun(display = False,
                dict = {
                    'item_name':[],
                    'price':[],
                    'pecentage_off':[],
                    'previous_price':[],
                    'img_link':[],
                    'item_link':[]}
               ):
        
        browser = webdriver.Firefox(options=scraper.opts)
        
        browser.get('https://rockrun.com/collections/climbing-mountaineering-deals') # use selenium (via firefox instance) to connect to rockrun
        time.sleep(1)
        
        body = browser.find_element(By.CSS_SELECTOR, "body") # need to scroll down to access all sale items, so click somewhere that wont change the page, and scroll down
        no_of_pagedowns = 50
        
        while no_of_pagedowns:
            body.send_keys(Keys.PAGE_DOWN) # send pg_down key press to firefox instance
            time.sleep(1) #it loads new thingies so give it a mo
            no_of_pagedowns-=1
        
        soup = bs(browser.page_source) # convert html from selenium to parsed text
        browser.quit()
        
        all = soup.findAll('div', class_='product-wrap') # find html class for sale items, gather all classes into list
        
        for i in all: # each sale item, get relevant info from html 
            dict['item_name'].append(i.find(class_ ='product-thumbnail__title').get_text())
            price = float(i.find(class_ = 'money').get_text().strip().replace('£',''))
            dict['price'].append(price)
            previous_price = price if i.find(class_ = 'product-thumbnail__was-price compare-at-price') is None else float(i.find(class_ = 'product-thumbnail__was-price compare-at-price').get_text().strip().replace('£',''))
            dict['previous_price'].append(previous_price)
            dict['pecentage_off'].append((1 - (price/previous_price))*100)
            dict['item_link'].append(f"https://rockrun.com{i.find('a')['href']}")
            dict['img_link'].append(f"https://{i.find('img')['src'].strip('/')}")
        
        if display:
            scraper.display(dict)
    
        return dict

    def climbers_shop(display = False,
                      dict = {
                          'item_name':[],
                          'price':[],
                          'pecentage_off':[],
                          'previous_price':[],
                          'img_link':[],
                          'item_link':[]}
                     ):

        browser = webdriver.Firefox(options=scraper.opts)
        browser.get('https://www.climbers-shop.com/climbing-equipment/eol/instock')
        time.sleep(1)
        
        body = browser.find_element(By.CSS_SELECTOR, "body")
        no_of_pagedowns = 30
        
        while no_of_pagedowns:
            body.send_keys(Keys.PAGE_DOWN) 
            time.sleep(1)
            no_of_pagedowns-=1
        
        soup = bs(browser.page_source)
        browser.quit()
        
        pattern2 = re.compile(r'item col-facetItem ctrPad16$')
        all = soup.findAll('div', class_ = pattern2)
        
        for i in all:
            if i.find('div', class_ = re.compile(r'col-1 pricing$')).find(id='lblwas'): #some items arnt actually on sale idk, so just skip if i cant return a prev price
                dict['item_name'].append(i.find('a', class_ = re.compile(r'col-1 frItemName$')).get_text())
                dict['price'].append(float(i.find('div', class_ = re.compile(r'col-1 pricing$')).find(id='lblNow').get_text().strip().replace('£','')))
                dict['previous_price'].append(float(i.find('div', class_ = re.compile(r'col-1 pricing$')).find(id='lblwas').get_text().strip().replace('£','')))
                dict['pecentage_off'].append(float(i.find('div', class_ = re.compile(r'col-1 pricing$')).find(class_='percentOff-betterSearch').get_text().split(' ')[1].replace('%', '')))
                dict['item_link'].append(f"https://www.climbers-shop.com{i.find('a', class_ = re.compile(r'col-1 frItemName$'))['href']}")
                dict['img_link'].append(f"https://www.climbers-shop.com{i.find('img')['data-src']}")
        
        if display:
            scraper.display(dict)
    
        return dict
        
    def gooutdoors(pages = 99,
                   display = False,
                   dict = {
                       'item_name':[],
                       'price':[],
                       'pecentage_off':[],
                       'previous_price':[],
                       'img_link':[],
                       'item_link':[]}
                     ):
        browser = webdriver.Firefox(options=scraper.opts)
        pattern = re.compile(r'^product-item')
        
        for pg in range(1,pages + 1):
            url = f'https://www.gooutdoors.co.uk/climbing/sal:view/page{pg}.html'
            browser.get(url)
            time.sleep(1)
            soup = bs(browser.page_source)
            if soup.find(id='noPage'): #stop if the returned html contains an empty warning (ran out of sale items) or pgs >= 100 (just in case)
                break
            all = soup.find('div', class_ = 'productlist_grid').findAll('article', class_ = pattern)
        
            for i in all:
                sale_text = i.find(class_='offer-text').find().get_text()
                if '%' in sale_text:
                    off = float([i for i in sale_text.split(' ') if '%' in i][0].replace('%', ''))/100
                else:
                    off = 0
                dict['item_link'].append(f"https://www.gooutdoors.co.uk{i.find('a')['href']}")
                dict['img_link'].append(i.find('img')['src'])
                dict['item_name'].append(i.find('h2').get_text())
                price = float(i.find(class_='loyalty-price').get_text().partition('£')[2]) * (1-off)
                dict['price'].append(price)
                previous_price = float(i.find(class_='retail-price').get_text().partition('£')[2])
                dict['previous_price'].append(previous_price)
                dict['pecentage_off'].append((1 - (price/previous_price))*100)
            time.sleep(5) # gooutdoors doesnt like being called lots :(
        browser.quit()
        
        if display:
            scraper.display(dict)
    
        return dict

    @staticmethod
    def scrape(display = False):
        dict = scraper.bananafingers()
        dict = scraper.rockrun(dict = dict)
        dict = scraper.climbers_shop(dict = dict)
        dict = scraper.gooutdoors(dict = dict)
        
        df = scraper.dict_to_df(dict)
        
        if display:
            scraper.display(df)
            return
            
        return df