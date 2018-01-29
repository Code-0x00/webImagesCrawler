#coding:utf-8

import urllib2
import urllib
import sys

class DownloadImage:
	def __init__(self):
		print 'DownloadImage----in----'
		print 'DownloadImage----out----'

	def urlcallback(self, a,b,c):
		print "download %d%%" %(100.0/(c/b + 1)*a)

	def download(self, url, local, mProxy=None):
		print 'DownloadImage----download----in----'
		opener = urllib2.build_opener(urllib2.ProxyHandler({'http':mProxy}), urllib2.HTTPHandler)
		urllib2.install_opener(opener)
		method = urllib2.Request(url)
		urllib.urlretrieve(url,local,self.urlcallback) 
		print 'DownloadImage----download----out----'
	


if __name__=="__main__":
	print 'DownloadImage----main----in----'
	downloadImage = DownloadImage()
	downloadImage.download(url='http://upload.chinapet.com/forum/201401/06/131929o7int562hiubeu4u.jpg', local='netInChina.jpg')
	downloadImage.download(url='https://scontent.cdninstagram.com/t51.2885-15/e35/12965631_224547241237230_778658931_n.jpg?ig_cache_key=MTIzMTYyNzU3ODMxMDg1MTY5NA%3D%3D.2', local='netInAmerica.jpg', mProxy='http://127.0.0.1:8087')
	print 'DownloadImage----main----out----'
