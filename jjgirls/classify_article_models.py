from urllib import request

from pyquery import PyQuery as pyq
import os, time, random, sys
from multiprocessing import Pool,Lock,cpu_count

#自有模块
import model.model as model
import model.db as dbm


base_url = 'http://www.jjgirls.com';


def analysis_url(url):
    # print(url)
    list = url.split('/')
    return list[3]+'-'+list[4]

def download(name,limit):
    # print(name)
    start = time.time()
    # time.sleep(random.random() * 3)
    db = dbm.DbManager('tmpwebsite')
    lock.acquire()
    try:
        one_data = db.getone(model.ArticleModels)
    finally:
        lock.release()
    # print(one_data.url,one_data.title)
    list = one_data.url.split('/')
    cate = list[3]
    cate2 = list[4]
    # print(cate)
    db.update_cate(model.ArticleModels,one_data.id,cate,cate2)
    id = one_data.id
    db.close()
    end = time.time()
    print('Task (%s/%s) id: %s runs %0.2f seconds.' % (str(int(name)+1), limit, id, (end - start)))

if __name__=='__main__':

    args = sys.argv
    if len(args)==2:
        limit = int(args[1])
    else:
        limit = 1
    lock = Lock()
    # res = download(1,2)
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