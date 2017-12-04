from urllib import request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from pyquery import PyQuery as pyq
import os, time, random, sys, logging
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
    def getone(self):
        data = self.session.query(Article).filter(Article.status==0).first()
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
            pass
            # print('重复')
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
def catchhtml(url,title):
    try:
        proxy="http://127.0.0.1:1087"
        proxy_handler=request.ProxyHandler({'http':proxy})
        opener=request.build_opener(proxy_handler)
        request.install_opener(opener)
        # request.urlretrieve(url, 'cache/3.txt')
        response = request.urlopen(url)
        html = response.read()
        doc = pyq(html);
        cts = doc('.p160222 a')
        for i in cts:
            a = pyq(i)
            url = a.attr("href")
            text = a.text()
        #     url = fixurl(url)
        # #     url = url.lower()
            # print(text)
            insertdb(url,title)
        return True
    except Exception as e:
        print(e,url)
        return False

def insertdb(url,title):
    db = DbManager(1)
    if(url.endswith('.jpg') or url.endswith('.png') or url.endswith('.gif') or url.endswith('.jpeg')):
        if(not url.startswith('http')):
            url = base_url + url
        db.insert(Pic,url,title,0)
    else:
        db.insert(Pic,url,title,9)
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

def log(str,logname='mylogger'):
    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)
    this_dir = os.path.dirname(__file__)
    log_dir = os.path.join(this_dir,'log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    # print(date)
    ext = '.txt';
    log_filename = os.path.join(log_dir,date+ext)
    # print(new_filename)
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info(str)

def download(name,limit):

    start = time.time()
    # time.sleep(random.random() * 3)
    db = DbManager(1)
    lock.acquire()
    try:
        one_data = db.getone()
    finally:
        lock.release()
    # print(one_data.url,one_data.title)
    # print('Task %s has started.' % (str(int(name)+1)))
    res = catchhtml(one_data.url,one_data.title)
    # print(res)
    if(not res):
        db.fail(Article,one_data.id)
    db.close()
    end = time.time()
    # print('Task (%s/%s) id: %s runs %0.2f seconds.' % (str(int(name)+1), limit, one_data.id, (end - start)))
    sys.stdout.write('\r')
    sys.stdout.write('Task (%s/%s) id: %s runs %0.2f seconds.' % (str(int(name)+1), limit, one_data.id, (end - start)))
    sys.stdout.write('\r')
    sys.stdout.flush()
    # log('Task (%s/%s) id: %s runs %0.2f seconds.' % (str(int(name)+1), limit, one_data.id, (end - start)))


if __name__=='__main__':
    args = sys.argv
    if len(args)==2:
        limit = int(args[1])
    else:
        limit = 1
    # log('测试日志')
    # res = catchhtml('http://www.jjgirls.com/japanese/mihina-nagai/20/','title')
    # print(res)
    lock = Lock()
    cpu_count = cpu_count()
    p = Pool(cpu_count)
    begin = time.time()
    for i in range(limit):
        p.apply_async(download, args=(i,limit,))
    print('start subprocesses...')
    p.close()
    p.join()
    end = time.time()
    print('All subprocesses done.:'+ str(round(end-begin,2)))