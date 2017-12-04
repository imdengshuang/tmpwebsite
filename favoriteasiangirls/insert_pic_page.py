from urllib import request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from pyquery import PyQuery as pyq
import os,sys,datetime,time

Base = declarative_base()
engine = create_engine('mysql+pymysql://root:root@/tmpwebsite?unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock',connect_args={'charset':'utf8'})
DBSession = sessionmaker(bind=engine)

args = sys.argv
if len(args)==2:
    limit = int(args[1])
else:
    limit = 1

session = DBSession()
class Article(Base):
    __tablename__ = 'favoriteasiangirls_article'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    status = Column(Integer)
class PicPage(Base):
    __tablename__ = 'favoriteasiangirls_pic_page'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    status = Column(Integer)
base_url = 'http://favoriteasiangirls.com';

def catchhtml(url,title):
    try:
        print('start get html')
        begin = time.time()
        response = request.urlopen(url)
        html = response.read()
        end = time.time()
        print('finish;time:'+ str(round(end-begin,2)))
        doc = pyq(html);
        cts = doc('.GalThumbsWr .ThumbClmn a')
        for i in cts:
            a = pyq(i)
            url = a.attr("href")
            if(not url.startswith('http')):
                url= base_url + url
            insertDb(PicPage,url,title)
        return True
    except Exception as e:
        raise e
        return False

def insertDb(model,url,title):
    count = session.query(model).filter(model.url==url).count()
    if(count == 0):
        new = model(url=url,title=title,status=0)
        session.add(new)
        session.commit()
    else:
        print('重复')

def getlist(model,limit,callback):
    count = session.query(model).filter(model.status==0).count()
    if(count > 0):
        all_data = session.query(model).filter(model.status==0).limit(limit).all()
        for one_data in all_data :
            res = callback(one_data)
            if(res):
                one_data.status = 1
            else:
                one_data.status = 2
            session.add(one_data)
        session.commit()

def deal_data(one_data):
    return catchhtml(one_data.url,one_data.title)
getlist(Article,limit,deal_data)