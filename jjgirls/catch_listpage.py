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

class ListPage(Base):
    __tablename__ = 'jjgirls_list_page'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    status = Column(Integer)

def catchhtml(cate_name):
    cate_name = cate_name.lower()
    proxy="http://127.0.0.1:1087"
    proxy_handler=request.ProxyHandler({'http':proxy})
    opener=request.build_opener(proxy_handler)
    request.install_opener(opener)
    # request.urlretrieve(url, 'cache/1.txt')
    url = base_url+'/'+cate_name+'/1'
    response = request.urlopen(url)
    html = response.read()
    doc = pyq(html);
    cts = doc('.L1172T h2:eq(1) a')
    for i in cts:
        a = pyq(i)
        url = a.attr("href")
        text = a.text()
        url = fixurl(url)
        url = url.lower()
        print(url,text)
        if(text == 'Last'):
            max_num = int(url.replace('/'+cate_name+'/',''))
        # break
    print(max_num)
    for x in list(range(1,max_num+1)):
        insertdb(base_url+'/'+cate_name+'/'+str(x))

def insertdb(url):
    db = DbManager(1)
    db.insert(ListPage,url)

def fixurl(str):
    if(str.count('http') > 0 and not str.startswith('http')):
        # print('yes')
        # print(str.find('http'))
        # print(str[str.find('http'):])
        return str[str.find('http'):]
    else:
        # print('no')
        return str

if __name__=='__main__':

    cate_list = [
        'archive',
        'avgirls',
        'amateur',
        'wife',
        'hardcore',
        'asian',
        'european'
    ]
    for x in cate_list:
        catchhtml(x)
    # catchhtml(cate_list[0])
    # fixurl('/gallery/664336/洋物乱交/http://www.jjgirls.com/uncensored/caribbeancompr/guys-go-crazy/103117_001/')
