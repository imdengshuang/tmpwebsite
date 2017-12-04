from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
import os, time, random, sys, logging, socket
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
        data = self.session.query(Pic).filter(Pic.status==0).first()
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


def download_img(one_data):
    try:
        this_dir = os.path.dirname(__file__)
        pic_dir = os.path.join(this_dir,'pic')
        ext = os.path.splitext(one_data.url)[1]
        new_dir = os.path.join(pic_dir,str(one_data.title))
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        new_filename = os.path.join(new_dir,str(one_data.id)+ext)
        # print new_filename
        begin = time.time()
        socket.setdefaulttimeout(5)
        if(one_data.url.startswith('https')):
            proxy="https://127.0.0.1:1087"
            proxy_handler=request.ProxyHandler({'https':proxy})
        else:
            proxy="http://127.0.0.1:1087"
            proxy_handler=request.ProxyHandler({'http':proxy})
        opener=request.build_opener(proxy_handler)

        url = one_data.url
        if(url.find('uncensoreds') > 0):
            url = url.replace('uncensoreds','uncensored')
            # print('替换字符串 uncensoreds',url)
        if(url.find('japaneses') > 0):
            url = url.replace('japaneses','japanese')
            # print('替换字符串 japaneses',url)

        # opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0'),('Host','www.jjgirls.com'),('Accept-Encoding','gzip, deflate'),('Accept-Language','zh-CN,en-US;q=0.7,en;q=0.3'),('Connection','keep-alive'),('Upgrade-Insecure-Requests','1')]
        request.install_opener(opener)
        # print 'start download'
        # headers = {'Host': 'www.jjgirls.com', 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0'}
        # req = urllib.request.Request(one_data.url)
        # req.add_header('Host', 'www.jjgirls.com')
        # req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0')
        res = request.urlopen(url)
        hreader = res.getheaders()
        # print(hreader)
        # exit()
        if(hreader[2][1] == 'image/jpeg'):
            request.urlretrieve(url, new_filename)
        else:
            # print(hreader,one_data.url,one_data.id)
            return False
        # request.urlretrieve(one_data.url, new_filename)
        end = time.time()
        # print ('finish;time:'+ str(round(end-begin,2)))
        return True
    except Exception as e:
        print(e)
        print(one_data.url)
        return False
def download(name,limit):

    start = time.time()
    # time.sleep(random.random() * 3)
    db = DbManager(1)
    lock.acquire()
    try:
        one_data = db.getone()
    finally:
        lock.release()

    res = download_img(one_data)

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
