import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import random
from Constants import uastrings as uas
from utils import logger
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

        content, soup, ct = self.parse_url('https://www.alibaba.com/catalog/baby-food_cid')

        product_list, prod_name_l, prod_price_l, prod_rating_l, prod_rcount_l, prod_asin_l = [], [], [], [], [], []

        try:
            # dissect soup
            for item in soup.find_all("div", {"class": "organic-offer-wrapper organic-gallery-offer-inner m-gallery-product-item-v2 img-switcher-parent"}):
                item = item.encode("utf-8")
                print("item:{}\n\n\n\n\n".format(item))

                
                # item_rating = self.get_product_rating(item)
                item_name = self.get_product_name(item)
                # item_review_cnt = self.get_review_cnt(item)
                # item_asin = self.get_product_asin(item)
                # item_price = self.get_product_price(item)


                ''' 
                product = {
                    'Item Name' : item_name,
                    'Price' : item_price,
                    'Rating' : item_rating,
                    'Review Count' : item_review_cnt,
                    'ASIN' : item_asin
                }

                product_list.append(product)

            print("Product list:", product_list)

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

    def get_product_name(self, soup_src):
        try:
            item_name = soup_src.find("p", {"class" : "elements-title-normal__content medium"}).text.strip()
                    
        except Exception as e:
            item_name = "N/A"

        return item_name


    def get_product_rating(self, soup_src):
        try:
            item_rating = soup_src.find("span", {"class" : "a-icon-alt"}).text.strip()
        except Exception as e:
            item_rating = "N/A"

        return item_rating


    def get_review_cnt(self, soup_src):
        try:
            item_review_cnt = soup_src.find("a", {"class" : "a-size-small a-link-normal"}).text.strip()
        except Exception as e:
            item_review_cnt = "N/A"

        return item_review_cnt


    def get_product_asin(self, soup_src):
        try:
            asin_tag = soup_src.find("a", {"class" : "a-size-small a-link-normal"})
            # ASIN = after /project-reviews
            item_asin = str(asin_tag['href'].split("/")[2])

        except Exception as e:
            item_asin = "N/A"

        return item_asin


    def get_product_price(self, soup_src):
        try:
            item_price = soup_src.find("p", {"class" : "elements-offer-price-normal medium"}).text.strip()    
        
        except Exception as e:
            item_price = "N/A"

        return item_price
    
    def get_min_order(self, soup_src):
        try:
            item_min_order = soup_scr.find("p", {"class" : "element-offer-minorder-normal medium"}).text.strip()
        
        except Exception as e:
            item_min_order = "N/A"

        return item_min_order