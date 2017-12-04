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
        # html = html.decode('utf-8')
        doc = pyq(html);
        cts = doc('.p160160 a')
        # 直接输出结果,排查问题
        # print(cts)
        # return True
        for i in cts:
            a = pyq(i)
            url = a.attr("href")
            text = a.text()
            # 处理url
            # url = fixurl(url)
            insertdb(url,text)
        return True
    except Exception as e:
        print(e,url)
        return False

def download_img(one_data):
    print(one_data.id)
    try:
        # 创建文件夹生成文件名
        this_dir = os.path.dirname(__file__)
        pic_dir = os.path.join(this_dir,'pic')
        ext = os.path.splitext(one_data.url)[1]
        new_dir = os.path.join(pic_dir,str(one_data.title))
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        new_filename = os.path.join(new_dir,str(one_data.id)+ext)

        url = one_data.url
        # 下载前处理url
        # if(url.find('uncensoreds') > 0):
        #     url = url.replace('uncensoreds','uncensored')
        #     print('替换字符串 uncensoreds',url)
        # if(url.find('japaneses') > 0):
        #     url = url.replace('japaneses','japanese')
        #     print('替换字符串 japaneses',url)



        begin = time.time()
        # 设置过期时间
        socket.setdefaulttimeout(5)
        # 设置代理
        if(one_data.url.startswith('https')):
            proxy="https://127.0.0.1:1087"
            proxy_handler=request.ProxyHandler({'https':proxy})
        else:
            proxy="http://127.0.0.1:1087"
            proxy_handler=request.ProxyHandler({'http':proxy})




        # debug
        httpHandler = request.HTTPHandler(debuglevel=0)
        httpsHandler = request.HTTPSHandler(debuglevel=0)

        # 重定向的时候自动使用cookie
        cookie = http.cookiejar.CookieJar()  # 声明一个CookieJar对象实例来保存cookie
        cookie_support= request.HTTPCookieProcessor(cookie)

        # 根据选择装载不同
        opener=request.build_opener(proxy_handler,cookie_support,httpHandler, httpsHandler)
        # opener=request.build_opener(proxy_handler,cookie_support)
        # opener=request.build_opener(proxy_handler)

        # 设置请求header
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0'),('Host','www.jjgirls.com'),('Accept-Encoding','gzip, deflate'),('Accept-Language','zh-CN,en-US;q=0.7,en;q=0.3'),('Connection','keep-alive'),('Upgrade-Insecure-Requests','1'),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),('Cache-Control','max-age=0'),('Cookie','b3ed3772209dc96c81a5d16430eda3c9=1; __atuvc=8%7C48; __atuvs=5a1d24596d932f42000; jajapanese=7')]
        # 装载请求的配置
        request.install_opener(opener)

        # 单纯获取header,根据header下载
        # res = request.urlopen(url)
        # header = res.getheaders()
        # print(header)
        # return False
        # exit()
        # if(header[2][1] == 'image/jpeg'):
        #     request.urlretrieve(one_data.url, new_filename)
        # else:
        #     # print(header,one_data.url,one_data.id)
        #     print(header)
        #     return False
        # request.urlretrieve(one_data.url, new_filename)

        # 下载文件
        request.urlretrieve(url, new_filename)

        # end = time.time()
        # print ('finish;time:'+ str(round(end-begin,2)))
        return True
    except Exception as e:
        print(e)
        print(one_data.url)
        return False



def insertdb(url,title):
    db = dbm.DbManager('tmpwebsite')
    if(url.startswith('http://www.jjgirls.com/')):
        db.insert(model.ArticleModels,url,title,0)
    else:
        db.insert(model.ArticleModels,url,title,9)
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
        one_data = db.getone(model.Models)
    finally:
        lock.release()
    # print(one_data.url,one_data.title)
    # print('Task %s has started.' % (str(int(name)+1)))
    res = catchhtml(one_data.url)
    # print(res)
    if(not res):
        db.fail(model.Models,one_data.id)
    db.close()
    end = time.time()
    print('Task (%s/%s) id: %s runs %0.2f seconds.' % (str(int(name)+1), limit, one_data.id, (end - start)))

if __name__=='__main__':
    print('this is example')
    exit();


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