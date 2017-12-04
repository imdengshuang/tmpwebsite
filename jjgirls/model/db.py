from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

class DbManager(object):
    """docstring for DbManager"""
    def __init__(self, dbname):
        super(DbManager, self).__init__()
        self.dbname = dbname
        # print(dbname)
        engine = create_engine('mysql+pymysql://root:root@/'+dbname+'?unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock',connect_args={'charset':'utf8'})
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
    def getone(self,model,status=0,target_status=1):
        data = self.session.query(model).filter(model.status==status).first()
        data.status = target_status
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
    def fail(self,model,id,target_status=2):
        try:
            one_data = self.session.query(model).filter(model.id==id).first()
            if(one_data):
                one_data.status = target_status
                self.session.add(one_data)
                self.session.commit()
                return one_data
        except Exception as e:
            print(e)
    def close(self):
        self.session.close()
    def update_cate(self,model,id,value,value2):
        try:
            one_data = self.session.query(model).filter(model.id==id).first()
            if(one_data):
                one_data.cate = value
                one_data.cate2 = value2
                self.session.add(one_data)
                self.session.commit()
                return one_data
        except Exception as e:
            print(e)