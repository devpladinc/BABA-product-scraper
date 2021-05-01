import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import os
import random
import re
from constant_store import uastrings as uas
from utils import logging as log
from datetime import date, time, timedelta

class AlibabaProductScraper():
    
    def __init__(self):
        ''' Initialize scraper '''
        self.uas = uas

    def rotate_UA(self):
        ''' rotation of UA to by-pass crawl error '''
        return random.choice(self.uas)


    def parse_url(self, url, headers=''):
        ''' get soup from url '''

        if headers == '':
            headers = {'User-Agent': self.rotate_UA()}
            content = None
        else:
            # coming from unit testing
            headers = headers    

        try:
            response = requests.get(url, headers=headers)
            ct = response.headers['Content-Type'].lower().strip()

            if 'text/html' in ct:
                content = response.content
                soup = BeautifulSoup(content, "html.parser")
            else:
                content = response.content
                soup = None
        except Exception as e:
            log.warning('Parsing error: %s', e)
            return False

        return content, soup, ct


    def get_data(self, url):
        
        content, soup, ct = self.parse_url(url)
        product_list, prod_name_l, prod_price_l, prod_minorder_l, prod_suppliers_l, prod_asin_l = [], [], [], [], [], []
    
        try:
            # dissect soup
            for soup_src in soup.find_all("div", {"class": "organic-offer-wrapper organic-gallery-offer-inner m-gallery-product-item-v2 img-switcher-parent"}):    
                                                    
                product_names = self.extract_text_vtags(soup_src, 'h4', prod_name_l)
                product_prices = self.extract_text_vattributes(soup_src, {"data-e2e-name":"price@@normal"}, prod_price_l)
                product_min_orders = self.extract_text_vattributes(soup_src, {"data-e2e-name":"minOrder"}, prod_minorder_l)
                product_suppliers = self.extract_text_vattributes(soup_src, {"flasher-type":"supplierName"}, prod_suppliers_l)

            #generating dict to csv output
            product_dict = {'Item Name': product_names,
                            'Price Range': product_prices,
                            'Minimum Order': product_min_orders,
                            'Supplier': product_suppliers
                        }

            log.info('Product List: %s', product_dict)
            
            try:
                df = pd.DataFrame(product_dict) 
            
                # saving the dataframe to csv
                file_name = 'outputs/extract_file_{}-{}.csv'.format(str(date.today()), str(random.randrange(0,999999)))
                df.to_csv(file_name)
            except Exception as e:
                log.warning('Generating csv report error: %s', e)
                # save to db
                return False

        except Exception as e:
            log.warning('Generating data error: %s', e)
            return False


    def extract_text_vtags(self, soup, tag, prod_list):
        ''' iterator for each tag. extract tag and text 
            params -    soup: html soup
                        tag: tag use to locate data
                        prod_list: list to contain extracted data
                        '''

        for item in soup.find(tag):
            item_extract = item.text
            if item_extract == None or item_extract == '':
                item_extract = 'N/A'
            prod_list.append(item_extract)
        return prod_list


    def extract_text_vattributes(self, soup, attrib, prod_list):
        ''' iterator for each tag. extract tag and text 
            params -    soup: html soup
                        attrib: dict; use to locate data
                        prod_list: list to contain extracted data
                        '''
            
        for item in soup.find_all(attrs=attrib):
            item_extract = item.text
            if item_extract == None or item_extract == '':
                item_extract = 'N/A'
            prod_list.append(item_extract)
        return prod_list    