# 根据ArticleModels获取图片地址
from urllib import request

from pyquery import PyQuery as pyq
import os, time, random, sys
from multiprocessing import Pool,Lock,cpu_count

#自有模块
import model.model as model
import model.db as dbm


base_url = 'http://www.jjgirls.com';

def catchhtml(url):
    try:
        proxy="http://127.0.0.1:1087"
        proxy_handler=request.ProxyHandler({'http':proxy})
        opener=request.build_opener(proxy_handler)
        request.install_opener(opener)
        response = request.urlopen(url)
        html = response.read()
        # 转换编码解决乱码
        html = html.decode('utf-8')
        doc = pyq(html);
        cts = doc('.p160222 a')
        if(not cts):
            print(url)
            print('empty')
            exit()
        # 直接输出结果,排查问题
        # print(cts)
        # return True
        for i in cts:
            a = pyq(i)
            url = a.attr("href")
            text = a.text()
            # 处理url
            url = fixurl(url)
            insertdb(url,text)
        return True
    except Exception as e:
        print(e,url)
        return False

def insertdb(url,title):
    db = dbm.DbManager('tmpwebsite')
    if(url.endswith('.jpg') or url.endswith('.png') or url.endswith('.gif') or url.endswith('.jpeg')):
        if(not url.startswith('http')):
            url = base_url + url
        db.insert(model.Pic,url,title,0)
    else:
        db.insert(model.Pic,url,title,9)
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
    db = dbm.DbManager('tmpwebsite')
    lock.acquire()
    try:
        one_data = db.getone(model.ArticleModels)
    finally:
        lock.release()
    # print(one_data.url,one_data.title)
    # print('Task %s has started.' % (str(int(name)+1)))
    res = catchhtml(one_data.url)
    # print(res)
    if(not res):
        db.fail(model.ArticleModels,one_data.id)
    db.close()
    end = time.time()
    print('Task (%s/%s) id: %s runs %0.2f seconds.' % (str(int(name)+1), limit, one_data.id, (end - start)))

if __name__=='__main__':
    # print('this is example')
    # catchhtml('http://www.jjgirls.com/japanese/abiru-sakai/5/')
    # exit();


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