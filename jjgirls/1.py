from urllib import request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from pyquery import PyQuery as pyq

def catchhtml(url):
    proxy="http://127.0.0.1:1087"
    proxy_handler=request.ProxyHandler({'http':proxy})
    opener=request.build_opener(proxy_handler)
    request.install_opener(opener)
    request.urlretrieve(url, '1.txt')

url = 'http://www.jjgirls.com';
# url += '/gallery/asian-models-254/index.html';
catchhtml(url)