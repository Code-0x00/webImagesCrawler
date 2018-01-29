#coding:utf-8
import urllib2
import re
from selenium import webdriver
from selenium.webdriver.common.proxy import *
import time
import SqlDB

class GoogleImage:
        def __str__(self):
        	return 'GoogleImage'

        __repr__ = __str__
    
        def __init__(self, mSqlDB = 0, mProxy = None):
                print 'GoogleImage----in----'
                self.mSqlDB = mSqlDB
                self.isUsingSqlDB = False
                self.mProxy = mProxy
                if type(mSqlDB.__class__) is type(SqlDB.SqlDB):
                        self.isUsingSqlDB = True
                        print 'using sqlDB'
                else:
                        print 'can not use sqlDB'
                #print 'the type of mSqlDB:' + str(mSqlDB.__class__) 
                print 'GoogleImage----out----'

        def insertDB(self, url, keywords):
                print 'GoogleImage----insertDB----in----'
                if self.isUsingSqlDB:
                        print 'using sqlDB'
                        #print 'engine:' + self.__str__()
                        self.mSqlDB.insert(url, self.__str__(), keywords)
                else:
                        print 'can not use sqlDB'
                print 'GoogleImage----insertDB----out----'

        def fetch(self, keywords):
                print 'GoogleImage----fetch----in----'
                #localHtmlFile = open('google_1.html', 'rb')
                #content = localHtmlFile.read()
                driver = webdriver.Firefox(proxy=self.mProxy)
                driver.get("https://www.google.com.hk/search?q=" + keywords + "&newwindow=1&safe=strict&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjAqtz97ZnMAhVFFywKHZYzDQkQ_AUIBygB&biw=1745&bih=814")
                js="var q=document.documentElement.scrollTop=100000"
                driver.execute_script(js)
                driver.implicitly_wait(5)
                content=driver.page_source.encode("utf-8")
                for page_num in range(20):
                        waitCount = 0
                        print('page:'+str(page_num+1))
                        driver.execute_script(js)
                        while(content==driver.page_source.encode("utf-8")):
                                waitCount += 1
                                time.sleep(0.2)
                                print "waitCount:" + str(waitCount)
                                if(waitCount >= 20):
                                        break
                        if(waitCount >= 20):
                                break
                        print "new content"
                        content = driver.page_source.encode("utf-8")
                urls=re.findall(r'<div class="rg_meta">[^<]*<\/div>',content,re.I)
                #print urls
                for matchUrl in urls:
                        #print matchUrl
                        jpgUrlList = re.findall(r'"ou":"[^"]*.jpg"', matchUrl, re.I)
                        if len(jpgUrlList) > 0:
                                urlList = re.findall(r'http[^"]*.jpg', jpgUrlList[0], re.I)
                                if len(urlList) > 0: 
                                        url = urlList[0]
                                        print url
                                        self.insertDB(url, unicode(keywords, "utf-8"))
		driver.close()
                print 'GoogleImage----fetch----out----'
                    
if __name__=="__main__":
        print 'GoogleImage----main----in----'
        GoogleImage = GoogleImage()
        GoogleImage.fetch('阿比西尼亚猫')
        print 'GoogleImage----main----out----'
