from urllib import request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from pyquery import PyQuery as pyq
import os, time, random, sys
from multiprocessing import Pool,Lock,cpu_count



base_url = 'http://www.jjgirls.com';

class DbManager(object):
    """docstring for DbManager"""
    def __init__(self, arg):
        super(DbManager, self).__init__()
        self.arg = arg
        engine = create_engine('mysql+pymysql://root:root@/tmpwebsite?unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock',connect_args={'charset':'utf8'})
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
    def getone(self,model):
        data = self.session.query(model).filter(model.status==0).first()
        data.status = 1
        self.session.add(data)
        self.session.commit()
        return data
    def insert(self,model,url,title,status=0):
        count = self.session.query(model).filter(model.url==url).count()
        if(count == 0):
            new = model(url=url,title=title,status=status)
            self.session.add(new)
            self.session.commit()
            # print('insert',url)
        else:
            # print('重复')
            pass
    def fail(self,model,id):
        try:
            one_data = self.session.query(model).filter(model.id==id).first()
            if(one_data):
                one_data.status = 2
                self.session.add(one_data)
                self.session.commit()
                return one_data
        except Exception as e:
            print(e)
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
class ArticleModels(Base):
    __tablename__ = 'jjgirls_article_models'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    status = Column(Integer)
class Pic(Base):
    __tablename__ = 'jjgirls_pic'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    status = Column(Integer)
def catchhtml(url):
    try:
        proxy="http://127.0.0.1:1087"
        proxy_handler=request.ProxyHandler({'http':proxy})
        opener=request.build_opener(proxy_handler)
        request.install_opener(opener)
        # request.urlretrieve(url, 'cache/article_models.txt')
        # return True
        response = request.urlopen(url)
        html = response.read()
        html = html.decode('utf-8')
        # html = response.read()
        doc = pyq(html);
        cts = doc('.p160160 a')
        # print(cts)
        # return True
        for i in cts:
            a = pyq(i)
            url = a.attr("href")
            text = a.text()
            url = fixurl(url)
        #     url = url.lower()
            # print(url,text)
            insertdb(url,text)
        return True
    except Exception as e:
        print(e,url)
        return False

def insertdb(url,title):
    db = DbManager(1)
    if(url.startswith('http://www.jjgirls.com/')):
        db.insert(ArticleModels,url,title,0)
    else:
        db.insert(ArticleModels,url,title,9)
    db.close()

def fixurl(str):
    if(str.count('http') > 0 and not str.startswith('http')):
        # print('yes')
        # print(str.find('http'))
        # print(str[str.find('http'):])
        return str[str.find('http'):]
    else:
        # print('no')
        return str

def download(name,limit):

    start = time.time()
    # time.sleep(random.random() * 3)
    db = DbManager(1)
    lock.acquire()
    try:
        one_data = db.getone(Models)
    finally:
        lock.release()
    # print(one_data.url,one_data.title)
    # print('Task %s has started.' % (str(int(name)+1)))
    res = catchhtml(one_data.url)
    # print(res)
    if(not res):
        db.fail(Models,one_data.id)
    db.close()
    end = time.time()
    print('Task (%s/%s) id: %s runs %0.2f seconds.' % (str(int(name)+1), limit, one_data.id, (end - start)))

if __name__=='__main__':
    args = sys.argv
    if len(args)==2:
        limit = int(args[1])
    else:
        limit = 1
    # res = catchhtml('http://www.jjgirls.com/model/Abigaile.Johnson')
    # print(res)
    lock = Lock()
    cpu_count = cpu_count()
    p = Pool(cpu_count)
    begin = time.time()
    for i in range(limit):
        p.apply_async(download, args=(i,limit,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    end = time.time()
    print('All subprocesses done.:'+ str(round(end-begin,2)))