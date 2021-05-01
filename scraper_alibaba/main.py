from helpers import AlibabaProductScraper as BB
from utils import logging as log
import csv

def main():
    #create bot
    bot = BB()
    
    # extract csv file
    csv_file = open('urls.csv', 'r')
    csv_f = csv.reader(csv_file)

    url_list = []
    for row in csv_f:
        # clean url
        url = str("".join(row))
        url_list.append(url)

    log.info('URL list: %s', url_list)
    
    for url in url_list:
        bot.get_data(url)


if __name__ == "__main__":
    main()