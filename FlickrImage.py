#coding:utf-8
import re
from selenium import webdriver
import time
import SqlDB

class FlickrImage:
	def __str__(self):
		return 'FlickrImage'

	__repr__ = __str__
	
        def __init__(self, mSqlDB = 0, mProxy = None):
		print 'FlickrImage----in----'
		self.mSqlDB = mSqlDB
		self.isUsingSqlDB = False
                self.mProxy = mProxy
		if type(mSqlDB.__class__) is type(SqlDB.SqlDB):
			self.isUsingSqlDB = True
			print 'using sqlDB'
		else:
			print 'can not use sqlDB'
		#print 'the type of mSqlDB:' + str(mSqlDB.__class__) 
		print 'FlickrImage----out----'

	def insertDB(self, url, keywords):
		print 'FlickrImage----insertDB----in----'
		if self.isUsingSqlDB:
			print 'using sqlDB'
			#print 'engine:' + self.__str__()
			self.mSqlDB.insert(url, self.__str__(), keywords)
		else:
			print 'can not use sqlDB'
		print 'FlickrImage----insertDB----out----'

	def fetch(self, keywords):
		print 'FlickrImage----fetch----in----'
		
		#localHtmlFile = open('flickr_1.html', 'rb')
		#content = localHtmlFile.read()
		
                driver = webdriver.Firefox(proxy=self.mProxy)
		driver.get("https://www.flickr.com/search/?text=" + keywords +"&view_all=1")
		js="var q=document.documentElement.scrollTop=100000"
		driver.execute_script(js)
		driver.implicitly_wait(5)
		content=driver.page_source.encode("utf-8")
		#print content
		#number = 0
		#saveContent = open('flickr_' + str(number) + '.html', 'wb')
		#saveContent.write(content)
		#saveContent.close()
              
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
				try:
					driver.find_element_by_class_name("infinite-scroll-load-more").click()
				except Exception, e:
					break
			print "new content"
			content = driver.page_source.encode("utf-8")
			saveContent = open('flickr_' + str(page_num) + '.html', 'wb')
			saveContent.write(content)
			saveContent.close()
			
		urls=re.findall(r'<div class="view photo-list-photo-view awake"[^>](.*)>',content,re.I)
		for mUrl in urls:
			matchUrl=re.findall('//(.*).jpg', mUrl, re.I)
			matchUrl="http://" + matchUrl[0] + '.jpg'
			if matchUrl.find('_n.jpg') > 0:
				matchUrl = matchUrl.replace('_n.jpg', '_b.jpg')
			elif matchUrl.find('_m.jpg') > 0:
				matchUrl = matchUrl.replace('_m.jpg', '_b.jpg')
			url = matchUrl
			print url
			self.insertDB(url, unicode(keywords, "utf-8"))
		driver.close()
		print 'FlickrImage----fetch----out----'
					
if __name__=="__main__":
	print 'FlickrImage----main----in----'
	flickrImage = FlickrImage()
	flickrImage.fetch('Abyssinian')
	print 'FlickrImage----main----out----'
