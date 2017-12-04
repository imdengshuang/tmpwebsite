from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
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
    cate = Column(String)
    cate2 = Column(String)
class Pic(Base):
    __tablename__ = 'jjgirls_pic'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    status = Column(Integer)
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
