from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
import os, time, random, sys, logging, socket
from multiprocessing import Pool,Lock,cpu_count
from pyquery import PyQuery as pyq
from urllib import request
import http.cookiejar


class DbManager(object):
    """docstring for DbManager"""
    def __init__(self, arg):
        super(DbManager, self).__init__()
        self.arg = arg
        engine = create_engine('mysql+pymysql://root:root@/tmpwebsite?unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock',connect_args={'charset':'utf8'})
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
    def getone(self):
        data = self.session.query(Pic).filter(Pic.status==1).first()
        data.status = 3
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
            pass
            # print('重复')
    def fail(self,model,id):
        try:
            one_data = self.session.query(model).filter(model.id==id).first()
            if(one_data):
                one_data.status = 0
                self.session.add(one_data)
                self.session.commit()
                return one_data
        except Exception as e:
            print(e)
    def close(self):
        self.session.close()

Base = declarative_base()

class ListPage(Base):
    __tablename__ = 'jjgirls_list_page'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    status = Column(Integer)
class Article(Base):
    __tablename__ = 'jjgirls_article'
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


def check_img(one_data):
    print(one_data.id)
    this_dir = os.path.dirname(__file__)
    pic_dir = os.path.join(this_dir,'pic')
    ext = os.path.splitext(one_data.url)[1]
    new_dir = os.path.join(pic_dir,str(one_data.title))
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_filename = os.path.join(new_dir,str(one_data.id)+ext)
    # print new_filename
    return os.path.isfile(new_filename)

def download(name,limit):

    start = time.time()
    # time.sleep(random.random() * 3)
    db = DbManager(1)
    lock.acquire()
    try:
        one_data = db.getone()
    finally:
        lock.release()

    res = check_img(one_data)
    print(res)
    if(not res):
        db.fail(Pic,one_data.id)
    db.close()
    end = time.time()
    # print('Task (%s/%s) id: %s runs %0.2f seconds.' % (str(int(name)+1), limit, one_data.id, (end - start)))
    sys.stdout.write('\r')
    sys.stdout.write('Task (%s/%s) id: %s runs %0.2f seconds.' % (str(int(name)+1), limit, one_data.id, (end - start)))
    sys.stdout.write('\r')
    sys.stdout.flush()

if __name__=='__main__':
    args = sys.argv
    if len(args)==2:
        limit = int(args[1])
    else:
        limit = 1

    # download(1)

    lock = Lock()
    cpu_count = cpu_count()
    p = Pool(cpu_count)
    begin = time.time()
    for i in range(limit):
        p.apply_async(download, args=(i,limit))
    print('start subprocesses...')
    p.close()
    p.join()
    end = time.time()
    print('All subprocesses done.:'+ str(round(end-begin,2)))
