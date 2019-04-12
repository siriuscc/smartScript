# coding:utf-8


# 爬取所有电子书


import urllib3
import os
import re
import sys
import requests
import json
import time, threading
import traceback
import threadpool
import random 

from multiprocessing import cpu_count
from urllib import quote
from scrapy.selector import Selector


from logtool import *


reload(sys)
sys.setdefaultencoding('utf-8')



debugTag=True
logTag=True
errorTag=True



def convertNum(num):
	dic_num=[u"零",u"一",u"二",u"三",u"四",u"五",u"六",u"七",u"八",u"九",u'十']

	degree=[u'零',u'十',u'百',u'千']
	numstr=u'';
	d=num
	k=0

	while d>0:
		r=d%10
		k=k+1
		if k>1:
			numstr=degree[k-1]+numstr
		numstr=dic_num[r]+numstr
		d=d/10
	return numstr

#  主目录
def visitContents(domain):

	url=domain+"/lilunshuji/index.html"
	debug('\t request:'+url)

	body=requests.get(url);

	retry=10
	while not body.ok and retry>0: 
		body=requests.get(url);
		retry=retry-1


	sel = Selector(text=body.text)

	dl_set=sel.xpath("//div[@id='tab-nav']/dl")

	# for dl_item in dl_set:
	dl_item=dl_set[2]

	title=dl_item.xpath(".//dt/text()").extract()[0]
	
	for item in dl_item.xpath(".//dd/a"):
		href=item.xpath('@href').extract()[0]
		text=item.xpath('.//text()').extract()[0]

	# 	log('\t'+domain+href)
	# # print t.xpath('@href').extract()
	# 	log('\t'+text)

		visitSubClass(text,domain+href,domain)


# 子分类
def visitSubClass(clazzName,url,domain):
	debug('\t request:'+url)

	body=requests.get(url);
	sel = Selector(text=body.text)

	linkSet=sel.xpath("//ul[@id='tab-content']/li/a")

	for linkItem in linkSet:
		link=linkItem.xpath("@href").extract()[0]
		bookName=linkItem.xpath(".//text()").extract()[0].strip()

		try:
			visitBookContents(clazzName,bookName,domain+link,domain)
		
		except Exception,e:
			log(clazzName+':'+bookName+" throw a Exception:")
			# print e
			error(domain+link,e)
			


# 书籍章节目录
def visitBookContents(clazzName,bookName,url,domain):
	debug('\t request:'+url)

	body=requests.get(url)
	sel = Selector(text=body.text)

	# link_set=sel.xpath("//ul[@id='table-of-contents']/li/a")
	link_set=sel.css("#table-of-contents  li a")


	print 'contents:',len(link_set)

	# 创建书籍

	path=creatBook(clazzName,bookName)

	log(path)
	
	argList=list()

	if path !=False:
		
		argList.append(([bookName,path,link_set],None))

		# # 阻塞等待
		# while threading.activeCount()>=cpu_count():
		# 	time.sleep(random.randint(1,3))

		# t= threading.Thread(target=writeBook,args=(bookName,path,link_set))#创建程
		# t.setDaemon(True)
		# t.start()#开启线程
		writeBook(bookName,path,link_set)
	else:
		log('book exist,success')
	log("............\tclose a book:"+bookName+'\t...............\n\n')






# 书籍章节目录
def getBookMsg(clazzName,bookName,url,domain):
	debug('\t request:'+url)

	body=requests.get(url,timeout=5)
	sel = Selector(text=body.text)

	# link_set=sel.xpath("//ul[@id='table-of-contents']/li/a")
	link_set=sel.css("#table-of-contents  li a")

	argList=list()

	if path !=False:	
		argList.append(([bookName,path,link_set],None))
	
	# else:
	# 	log('book exist,success')
	# log("............\tclose a book:"+bookName+'\t...............\n\n')

	# 统计一下 list

	# for item in argList:
	# 	print 'book:',item[0][0]

	return argList
	

def downloadBook(clazzName,bookName,argList):
	

	# 创建书籍
	path=creatBook(clazzName,bookName)
	

	# 线程池 
	pool=threadpool.ThreadPool(4)

	tasks=threadpool.makeRequests(writeBook,argList)

	for task in tasks:
		pool.putRequest(task) 
	
	pool.wait()



def writeBook(bookName,path,link_set):
	
	print len(link_set)

	for i in range(len(link_set)):
		
		link_item=link_set[i]

		href=link_item.xpath("@href").extract()[0]

		sectionName=link_item.xpath("text()").extract()[0].strip()

		text_set=visitSection(sectionName,domain+href,domain)

		print 'sectionName:',sectionName

		log('... append a Section <'+ sectionName +'>\t to '+bookName)
		# 将内容输出到文件中
		appendSectionToFile(bookName,u'第'+convertNum(i+1)+u'回:'+sectionName,text_set,path)
	finishBook(path)


# 获取章节中内容
def visitSection(sectionName,url,domain):
	debug('\t request:'+url)

	body=None

	retry=10

	while (body==None or body.ok==False) and retry>0:
		
		try:
			body=requests.get(url)
		except Exception,e:
			pass

		retry=retry-1


	# except Exception,e:
	# 	print '\n\n\nerror'

	# 	# print help(body.ok)
	# 	print body.ok
	# 	print url
	# 	print e

	# 	print '\n\n\n***************************************************************'



	sel = Selector(text=body.text)

	title=sel.xpath("//div[@id='content']/h1/text()").extract()[0]

	text_set=sel.xpath("//div[@id='content']/p/text()").extract()

	return text_set

#  创建书籍
def creatBook(clazzName,bookName,directory='data/'):
	
	path=directory+clazzName.strip()+"/"+bookName.strip()+".onwrite.txt"

	successPath=directory+clazzName.strip()+"/"+bookName.strip()+".txt"

	if os.path.exists(successPath):
		log('book exist:'+bookName)
		return False

	if os.path.exists(path):
		log('book last download faild,download:'+bookName)
		
		os.remove(path)

	if not os.path.exists(directory):
		os.mkdir(directory)

	if not os.path.exists(directory+clazzName+"/"):
		os.mkdir(directory+clazzName+"/")

	log('create new book:'+bookName)

	return path


# 完成文件的读写
def finishBook(path):

	newPath=path.replace('.onwrite.','.')

	os.rename(path,newPath)
	log('finishBook')

	print threading.enumerate()


	return newPath

#  追加一个章节到书本
def appendSectionToFile(bookName,sectionName,text_set,path):

	with open(path, 'a') as f:

		f.write('\n\n\n'+sectionName+'\n')

		for line in text_set:	
			f.write('\t'+line+'\n')


if __name__=='__main__':

	domain="http://www.zysj.com.cn"
	# visitContents(domain)


	# url='http://www.zysj.com.cn/lilunshuji/index_97.html'

	# clazzName=u'中医著作'

	# visitSubClass(clazzName,url,domain)



	url='http://www.zysj.com.cn/lilunshuji/jingyuequanshu/index.html'
	
	clazzName=u'中医书籍'
	bookName=u'《景岳全书》'


	visitBookContents(clazzName,bookName,url,domain)