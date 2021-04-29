# from product_scraper import AmazonProductScraper as AMZ
from helpers import AlibabaProductScraper as BB

def main():
    #create bot
    bot = BB()
    bot.get_data()

if __name__ == "__main__":
    main()