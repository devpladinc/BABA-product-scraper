import logging


logging.basicConfig(level=logging.DEBUG,
    format="{asctime} {levelname:8} {message}",
    style='{',
    filename='bb_log.log',
    filemode='w')