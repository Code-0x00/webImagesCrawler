#coding:utf-8
import urllib2
import re
import SqlDB

class BaiduImage:
	def __str__(self):
		return 'BaiduImage'

	__repr__ = __str__
	
	def __init__(self, mSqlDB):
		print 'BaiduImage----in----'
		self.mSqlDB = mSqlDB
		self.isUsingSqlDB = False
		if type(mSqlDB.__class__) is type(SqlDB.SqlDB):
			self.isUsingSqlDB = True
			print 'using sqlDB'
		else:
			print 'can not use sqlDB'
		#print 'the type of mSqlDB:' + str(mSqlDB.__class__) 
		print 'BaiduImage----out----'

	def insertDB(self, url, keywords):
		print 'BaiduImage----insertDB----in----'
		if self.isUsingSqlDB:
			print 'using sqlDB'
			#print 'engine:' + self.__str__()
			self.mSqlDB.insert(url, self.__str__(), keywords)
		else:
			print 'can not use sqlDB'
		print 'BaiduImage----insertDB----out----'

	def fetch(self, keywords):
		print 'BaiduImage----fetch----in----'
		for page_num in range(500):
			Page_num = page_num
			searchUrl = 'http://image.baidu.com/search/wisemiddetail?tn=wisemiddetail&ie=utf8&word=' + keywords + '&pn='+str(Page_num)+'&size=big&fr=wiseresult&fmpage=result&pos=imglist'
			#print url
			request = urllib2.Request(searchUrl)
			
			try:
        			response = urllib2.urlopen(request)
			except  urllib2.HTTPError:
				continue

        		content = response.read()
			urls=re.findall('<a href="http:.*?<\/a>',content,re.I) 
        		for matchUrl in urls:
            			if '原图' in matchUrl:
					#print matchUrl
                			url = re.findall(r'<a href="(.+?)">',matchUrl)[0]
					print url
					self.insertDB(url, unicode(keywords, "utf-8"))
		print 'BaiduImage----fetch----out----'
					
if __name__=="__main__":
	print 'BaiduImage----main----in----'
	baiduImage = BaiduImage(0)
	baiduImage.fetch('阿比西尼亚猫')
	print 'BaiduImage----main----out----'
