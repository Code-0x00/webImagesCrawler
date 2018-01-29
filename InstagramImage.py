#coding:utf-8
import urllib2
import re
from selenium import webdriver
import time
import SqlDB

class InstagramImage:
	def __str__(self):
		return 'InstagramImage'

	__repr__ = __str__
	
        def __init__(self, mSqlDB = 0, mProxy = None):
		print 'InstagramImage----in----'
		self.mSqlDB = mSqlDB
		self.isUsingSqlDB = False
                self.mProxy = mProxy
		if type(mSqlDB.__class__) is type(SqlDB.SqlDB):
			self.isUsingSqlDB = True
			print 'using sqlDB'
		else:
			print 'can not use sqlDB'
		#print 'the type of mSqlDB:' + str(mSqlDB.__class__) 
		print 'InstagramImage----out----'

	def insertDB(self, url, keywords):
		print 'InstagramImage----insertDB----in----'
		if self.isUsingSqlDB:
			print 'using sqlDB'
			#print 'engine:' + self.__str__()
			self.mSqlDB.insert(url, self.__str__(), keywords)
		else:
			print 'can not use sqlDB'
		print 'InstagramImage----insertDB----out----'

	def fetch(self, keywords):
		print 'InstagramImage----fetch----in----'
		
                driver = webdriver.Firefox(proxy=self.mProxy)
		max_id = '0'
		for page_num in range(100):
			Page_num = page_num
			if max_id == '0':
				searchUrl = 'https://www.instagram.com/explore/tags/' + keywords
			else:
				searchUrl = 'https://www.instagram.com/explore/tags/' + keywords + '?max_id='+str(max_id)
			
			print searchUrl
			driver.get(searchUrl)
			driver.implicitly_wait(5)
			content=driver.page_source.encode("utf-8")
			
			urls=re.findall('"id":"[^"]*","display_src":"[^"]*"',content,re.I)
			count = 0
			for i in urls:
				display_id = re.findall('"id":"[^"]*"', i, re.I)[0]
				display_src = re.findall('"display_src":"[^"]*"', i, re.I)[0]
				real_id = re.findall('"[^"]*"$',display_id,re.I)[0].split('"')[1].strip()
				real_src = re.findall('"[^"]*"$',display_src,re.I)[0].split('"')[1].strip()
				url = real_src.replace('\\', '')
				print url
				count = count + 1
				#print "count=" + str(count)
				self.insertDB(url, unicode(keywords, "utf-8"))
				if count == 12:
					max_id = real_id
					print 
					break

		driver.close()
		print 'InstagramImage----fetch----out----'
					
if __name__=="__main__":
	print 'InstagramImage----main----in----'
	instagramImage = InstagramImage()
	instagramImage.fetch('Abyssinian')
	print 'InstagramImage----main----out----'
