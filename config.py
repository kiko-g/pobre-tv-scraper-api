import os
from fake_useragent import UserAgent

PORT = os.getenv("PORT") or 5555
HOST = os.getenv("HOST") or '0.0.0.0'
ENVIRONMENT = os.getenv("ENVIRONMENT") or 'development'


def get_mode(environment: str):
    if environment.lower() == 'production':
        return False
    else:
        return True


ua = UserAgent()
headers = {'User-Agent': ua.random,
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
