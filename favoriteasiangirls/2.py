from urllib import request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from pyquery import PyQuery as pyq

Base = declarative_base()
engine = create_engine('mysql+pymysql://root:root@/tmpwebsite?unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock',connect_args={'charset':'utf8'})
DBSession = sessionmaker(bind=engine)
session = DBSession()
class Article(Base):
    __tablename__ = 'favoriteasiangirls_article'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    status = Column(Integer)


def catchhtml(url):
    request.urlretrieve(url, '3.txt')
    # response = request.urlopen(url)
    # html = response.read()
    # doc = pyq(html);
    # cts = doc('.GalThumbsWr .ThumbClmn a')
    # for i in cts:
    #     a = pyq(i)
    #     url = a.attr("href")
    #     print(url)

url = 'http://favoriteasiangirls.com/gallery/asian-pussy-143/1.html';
# url += '/gallery/asian-models-254/index.html';
catchhtml(url)