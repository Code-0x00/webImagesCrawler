#coding:utf-8
import sys
import argparse
import SqlDB
import BaiduImage
import FlickrImage
import InstagramImage
import BingImage
import GoogleImage
import selenium
from selenium import webdriver
from selenium.webdriver.common.proxy import *

def baiduImage():
	print 'baiduImage----in----'
	print 'baiduImage----out----'

def bingImage():
	print 'bingImage----in----'
	print 'bingImage----out----'

def googleImage():
	print 'googleImage----in----'
	print 'googleImage----out----'

def instagramImage():
	print 'instragramImage----in----'
	print 'instargramImage----out----'

def flickrImage():
	print 'flickrImage----in----'
	print 'flickrImage----out----'

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"--engine",
		default=None,
		help='BaiduImage+BingImage+GoogleImage+InstagramImage+FlickrImage'
	)
	parser.add_argument(
		"--keywords",
		default='AbyssinianCat',
		help="the keywords for enging searching"
	)
	parser.add_argument(
		"--proxy",
		default='localhost:8087',
		help="the proxy for engine searching"
	)
	args = parser.parse_args()
	print 'FetchAll----in----' + 'engine:' + str(args.engine) + "," + "keywords:" + args.keywords + "," + "proxy:" + args.proxy
	
	mSqlDB = SqlDB.SqlDB()
	
	mProxy = Proxy({
		'proxyType': ProxyType.MANUAL,
		'httpProxy': args.proxy,
		'ftpProxy': args.proxy,
		'sslProxy': args.proxy,
		'noProxy': ''})

	if(args.engine == None):
		print 'use all engine for your keywords:' + args.keywords
		engine = BaiduImage.BaiduImage(mSqlDB)
		engine.fetch(args.keywords)
		engine = BingImage.BingImage(mSqlDB)
		engine.fetch(args.keywords)
		engine = GoogleImage.GoogleImage(mSqlDB=mSqlDB, mProxy=mProxy)
		engine.fetch(args.keywords)
		engine = InstagramImage.InstagramImage(mSqlDB=mSqlDB, mProxy=mProxy)
		engine.fetch(args.keywords)
		engine = FlickrImage.FlickrImage(mSqlDB=mSqlDB, mProxy=mProxy)
		engine.fetch(args.keywords)
	elif(args.engine.find('BaiduImage') == 0):
		engine = BaiduImage.BaiduImage(mSqlDB)
		engine.fetch(args.keywords)
	elif(args.engine.find('BingImage') == 0):
		engine = BingImage.BingImage(mSqlDB)
		engine.fetch(args.keywords)
	elif(args.engine.find('GoogleImage') == 0):
		engine = GoogleImage.GoogleImage(mSqlDB=mSqlDB, mProxy=mProxy)
		engine.fetch(args.keywords)
	elif(args.engine.find('InstagramImage') == 0):
		engine = InstagramImage.InstagramImage(mSqlDB=mSqlDB, mProxy=mProxy)
		engine.fetch(args.keywords)
	elif(args.engine.find('FlickrImage') == 0):
		engine = FlickrImage.FlickrImage(mSqlDB=mSqlDB, mProxy=mProxy)
		engine.fetch(args.keywords)

	print 'FetchAll----out----'
