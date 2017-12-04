from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
import os, time, random, sys
from multiprocessing import Pool,Lock,cpu_count
from pyquery import PyQuery as pyq
from urllib import request



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
    def insert(self,model,url,title):
        count = self.session.query(model).filter(model.url==url).count()
        if(count == 0):
            new = model(url=url,title=title,status=0)
            self.session.add(new)
            self.session.commit()
            # print('insert',url)
        else:
            print('重复')

Base = declarative_base()

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
        # print('start get html')
        begin = time.time()
        response = request.urlopen(url)
        html = response.read()
        end = time.time()
        # print('finish;time:'+ str(round(end-begin,2)))
        doc = pyq(html);
        cts = doc('.GalThumbsWr .ThumbClmn a')
        for i in cts:
            a = pyq(i)
            url = a.attr("href")
            if(not url.startswith('http')):
                url= base_url + url
            db = DbManager(1)
            db.insert(PicPage,url,title)
        # print('insert finish')
        return True
    except Exception as e:
        raise e
        return False

def download(name):

    start = time.time()
    # time.sleep(random.random() * 3)
    db = DbManager(1)
    lock.acquire()
    try:
        one_data = db.getone()
    finally:
        lock.release()
    # print(one_data.url,one_data.title)
    catchhtml(one_data.url,one_data.title)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (str(int(name)+1), (end - start)))

if __name__=='__main__':
    args = sys.argv
    if len(args)==2:
        limit = int(args[1])
    else:
        limit = 1
    lock = Lock()
    cpu_count = cpu_count()
    p = Pool(cpu_count)
    begin = time.time()
    for i in range(limit):
        p.apply_async(download, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    end = time.time()
    print('All subprocesses done.:'+ str(round(end-begin,2)))
