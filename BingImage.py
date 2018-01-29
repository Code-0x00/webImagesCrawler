#coding:utf-8
import urllib
import urllib2
import re
import SqlDB
import os
from selenium import webdriver

class BingImage:
	def __str__(self):
		return 'BingImage'

        __repr__=__str__
	
	def __init__(self,mSqlDB):
		print('BingImage---in---')
		self.mSqlDB = mSqlDB
		self.isUsingSqlDB = False
		if type(mSqlDB.__class__) is type(SqlDB.SqlDB):
			self.isUsingSqlDB = True
			print ('using sqlDB')
		else:
			print ('can not use sqlDB')
		#print 'the type of mSqlDB:' + str(mSqlDB.__class_)
		print ('BingImage----out----')

	def insertDB(self, url, keywords):
		print ('BingImage----insertDB----in----')
		if self.isUsingSqlDB:
			print ('using sqlDB')
			#print 'engine:' + self.__str__()
			self.mSqlDB.insert(url, self.__str__(), keywords)
		else:
			print ('can not use sqlDB')
		print ('BingImage----insertDB----out----')

	def fetch(self, keywords):
		print ('BingImage----fetch----in----')
		for page_num in range(5):
			current_index=page_num*35
			searchUrl="http://cn.bing.com/images/async?q="+urllib.quote(keywords)+"&async=content&first="+ str(current_index) + "&count=35"
			webheaders = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'}
			request=urllib2.Request(url=searchUrl,headers=webheaders)
			print searchUrl
			try:
				response=urllib2.urlopen(request)
			except:
				continue

			original=r'imgurl:&quot;(.*?)&quot'
			page=response.read()
			urls=re.findall(original,str(page))
			for mUrl in set(urls):
				print mUrl
				self.insertDB(mUrl, unicode(keywords, "utf-8"))
		print 'BingImage----fetch----out----'
                    
                
if __name__=="__main__":
	print 'BingImage----main----in----'
	bingImage = BingImage(0)
	bingImage.fetch('阿比西尼亚猫')
	print 'BingImage----main----out----'
