from urllib import request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from pyquery import PyQuery as pyq
import os, time, random, sys

base_url = 'http://www.jjgirls.com';

class DbManager(object):
    """docstring for DbManager"""
    def __init__(self, arg):
        super(DbManager, self).__init__()
        self.arg = arg
        engine = create_engine('mysql+pymysql://root:root@/tmpwebsite?unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock',connect_args={'charset':'utf8'})
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
    def getone(self):
        data = self.session.query(Letter).filter(Letter.status==0).first()
        data.status = 1
        self.session.add(data)
        self.session.commit()
        return data
    def insert(self,model,url,title):
        count = self.session.query(model).filter(model.url==url).count()
        if(count == 0):
            new = model(url=url,status=0,title=title)
            self.session.add(new)
            self.session.commit()
            # print('insert',url)
        else:
            print('重复')
    def close(self):
        self.session.close()

Base = declarative_base()

class Letter(Base):
    __tablename__ = 'jjgirls_letter'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    status = Column(Integer)
class Models(Base):
    __tablename__ = 'jjgirls_models'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    status = Column(Integer)

def catchhtml(url):
    proxy="http://127.0.0.1:1087"
    proxy_handler=request.ProxyHandler({'http':proxy})
    opener=request.build_opener(proxy_handler)
    request.install_opener(opener)
    # request.urlretrieve(url, 'cache/models.txt')
    # return True
    response = request.urlopen(url)
    html = response.read()
    doc = pyq(html);
    cts = doc('.avlist:eq(0) a')
    # print(cts)
    for i in cts:
        a = pyq(i)
        url = a.attr("href")
        text = fix_title(a.text())
        insertdb(base_url+url,text)

def fix_title(title):
    # print(title)
    # print(title.find('('))
    # print(title[:title.find('(')])
    return title[:title.find('(')]


def insertdb(url,title):
    db = DbManager(1)
    db.insert(Models,url,title)

if __name__=='__main__':
    args = sys.argv
    if len(args)==2:
        limit = int(args[1])
    else:
        limit = 1
    db = DbManager(1)
    one_data = db.getone()
    print(one_data.id,one_data.url)
    db.close()
    res = catchhtml(one_data.url)
    # print(res)
