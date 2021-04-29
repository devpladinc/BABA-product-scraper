import logging

logger = logging.basicConfig(level=logging.DEBUG,
            format="{asctime} {levelname:8} {message}",
            style='{',
            filename='bblog.log',
            filemode='w')