import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import random
from Constants import uastrings as uas
from utils import logging as log
from datetime import date, time, timedelta

class AlibabaProductScraper():
    
    def __init__(self):
        ''' Initialize scraper '''
        self.uas = uas

    def rotate_UA(self):
        ''' rotation of UA to by-pass crawl error '''
        return random.choice(self.uas)


    def parse_url(self, url):
        ''' get soup from url '''
        headers = {'User-Agent': self.rotate_UA()}
        content = None

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
            print("Parsing error:", str(e))
        
        return content, soup, ct


    def get_data(self):

        content, soup, ct = self.parse_url('https://www.alibaba.com/catalog/paintings_cid')
        product_list, prod_name_l, prod_price_l, prod_rating_l, prod_rcount_l, prod_asin_l = [], [], [], [], [], []

        try:
            # dissect soup
            for soup_src in soup.find_all("div", {"class": "organic-offer-wrapper organic-gallery-offer-inner m-gallery-product-item-v2 img-switcher-parent"}):    
                
                # for tag in soup_src.find_all(attrs={"data-e2e-name":"price@@normal"}):
                #     log.info('%s' '%s', tag.name, tag.text)
                
                # for tag in soup_src.find_all(True):
                #     log.info('%s' '%s', tag.name, tag.text)
                                    
                product_names = self.extract_text_vtags(soup_src, 'h4', prod_name_l)
                product_prices = self.extract_text_vattributes(soup_src, {"data-e2e-name":"price@@normal"}, prod_price_l)

            log.info('Product Names: %s', product_names)
            log.info('Product Prices: %s', product_prices)

            '''
            for p in product_list:
                p_name = p['Item Name']
                p_price = p['Price']
                p_rating = p['Rating']
                p_rcount = p['Review Count']
                p_asin = p['ASIN']

                prod_name_l.append(p_name)
                prod_price_l.append(p_price)
                prod_rating_l.append(p_rating)
                prod_rcount_l.append(p_rcount)
                prod_asin_l.append(p_asin)

            #generating CSV
            product_dict = {'Item Name': prod_name_l,
                            'Price': prod_price_l,
                            'Rating': prod_rating_l,
                            'Review Count': prod_rcount_l,
                            'ASIN' : prod_asin_l
                            }

            df = pd.DataFrame(product_dict) 
        
            # saving the dataframe 
            df.to_csv('sample_product_{}-{}.csv'.format(str(date.today()),str(random.randrange(0,99999))))
            print("Done saving csv")

            '''

        except Exception as e:
            print("Soup error:", str(e))
            return False

    def extract_text_vtags(self, soup, tag, prod_list):
        ''' iterator for each tag. extract tag and text 
            params -    soup: html soup
                        tag: tag use to locate data
                        prod_list: list to contain extracted data
                        '''

        for item in soup.find(tag):
            item_extract = item.text
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
            prod_list.append(item_extract)
        return prod_list    