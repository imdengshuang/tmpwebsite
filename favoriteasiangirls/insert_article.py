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
    title = Column(String)
    status = Column(Integer)

base_url = 'http://favoriteasiangirls.com';

def catchhtml(url):
    # request.urlretrieve(url, '2.txt')
    response = request.urlopen(url)
    html = response.read()
    doc = pyq(html);
    cts = doc('.Thumb a')
    for i in cts:
        a = pyq(i)
        url = base_url+a.attr("href")
        title = a.attr("title")
        insertDb(Article,url,title)

def insertDb(model,url,title):
    count = session.query(model).filter(model.url==url).count()
    if(count == 0):
        new = model(url=url,title=title,status=0)
        session.add(new)
        session.commit()
    else:
        print('重复')

url = 'http://favoriteasiangirls.com/?page=4';
# url += '/gallery/asian-models-254/index.html';
catchhtml(url)