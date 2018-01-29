#coding:utf-8

import selenium
from selenium import webdriver
from selenium.webdriver.common.proxy import *

myProxy = "localhost:8087"

proxy = Proxy({
	'proxyType': ProxyType.MANUAL,
	'httpProxy': myProxy,
	'ftpProxy': myProxy,
	'sslProxy': myProxy,
	'noProxy':''})

driver = webdriver.Firefox(proxy=proxy)
driver.implicitly_wait(5)
driver.get("https://www.google.com")
content = driver.page_source.encode("utf-8")
print content
