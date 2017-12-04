from urllib import request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from pyquery import PyQuery as pyq

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
        data = self.session.query(Article).filter(Article.status==0).first()
        data.status = 1
        self.session.add(data)
        self.session.commit()
        return data
    def insert(self,model,url):
        count = self.session.query(model).filter(model.url==url).count()
        if(count == 0):
            new = model(url=url,status=0)
            self.session.add(new)
            self.session.commit()
            # print('insert',url)
        else:
            print('重复')

Base = declarative_base()

class Letter(Base):
    __tablename__ = 'jjgirls_letter'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    status = Column(Integer)

def catchhtml(url):
    proxy="http://127.0.0.1:1087"
    proxy_handler=request.ProxyHandler({'http':proxy})
    opener=request.build_opener(proxy_handler)
    request.install_opener(opener)
    # request.urlretrieve(url, 'cache/letter.txt')
    # return True
    response = request.urlopen(url)
    html = response.read()
    doc = pyq(html);
    cts = doc('.L1172T:eq(0) h2:eq(0) a')
    # print(cts)
    for i in cts:
        a = pyq(i)
        url = a.attr("href")
        text = a.text()
        print(url,text)
        insertdb(url)

def insertdb(url):
    db = DbManager(1)
    db.insert(Letter,url)

if __name__=='__main__':

    url = base_url
    catchhtml(url)
    # fixurl('/gallery/664336/洋物乱交/http://www.jjgirls.com/uncensored/caribbeancompr/guys-go-crazy/103117_001/')
