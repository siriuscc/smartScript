# coding:utf-8




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


domain="http://www.zysj.com.cn"


reload(sys)
sys.setdefaultencoding('utf-8')


def tab(k,c):
	s='';
	for i in range(k):
		s+=c

	return s

# 书籍章节目录
def getContents(bookName,url):

	print url
	body=requests.get(url)

	# print body

	sel = Selector(text=body.text)
	item_set=sel.xpath("//ul[@id='table-of-contents']/li")

	# for i in item_set:
	# 	print i.extract()


	return findR(item_set,1,bookName)

def findROld(item_set,level,path):
	
	parts=[]

	if len(item_set)>0:
		for item in item_set:
			part={
				'level':level,
				'title':'',
				'path':'',
				'href':None,
				'subContents':None
			}
			arr=item.xpath('./text()')

			if len(arr)>0:

				part['title'] = arr[0].extract().strip().replace('?','')
				# print '\t has text:',part['title'],len(arr),arr.extract()
				print 'no link title:',part['title'] ,len(arr),

			else:
				arr=item.xpath('./a/text()')

				part['title'] = arr[0].extract().strip().replace('?','')
				part['href']=item.xpath('a/@href').extract()[0]

				# print 'arr:',arr[0].extract(),len(arr),arr.extract()
				print 'title:',item.xpath('a/@title').extract()[0]

			# 不要把文件名也给进去
			part['path']=path
			sub_parts=item.xpath('ul/li')
			if len(sub_parts)>0:
				part['subContents']=findR(sub_parts,level+1,path+"/"+part['title'])

				# print 'title:',part['title']
			parts.append(part)
	return parts

def findR(item_set,level,path):
	
	parts=[]

	if len(item_set)>0:
		for item in item_set:
			part={
				'level':level,
				'title':'',
				'path':'',
				'href':None,
				'subContents':None
			}
			arr=item.xpath('./text()')


			aset=item.xpath('./a')
			
			if len(aset)>0:
				part['title']=aset[0].xpath("./text()").extract()[0].strip().replace('?','')
				part['href']=aset[0].xpath('./@href').extract()[0].strip().replace('?','')
				
			else :
				part['title']=arr[0].extract().strip().replace('?','')

			# print tab(level,'\t'),part['title']
			

			# 不要把文件名也给进去
			part['path']=path
			sub_parts=item.xpath('ul/li')
			if len(sub_parts)>0:
				part['subContents']=findR(sub_parts,level+1,path+"/"+part['title'])

				# print 'title:',part['title']
			parts.append(part)
	return parts


def partNav(parts):

	# help(parts)

	for part in parts:
		
		if part['href']==None:
			path=getPathR(part,parts)	 
			
			if path !=None:			
				part['path']=path
	
	for part in parts:
		if part['href']==None:
			pass
			# print part['path'],'\t',part['title']


def getPathR(part,parent):

	# if part['href']==None and part['subContents']==None:
	# 	parent.remove(part)
	# 	return None

	if part['href']==None:
		part['path']=getPathR(part['subContents'][0],part['subContents'])

		return part['path']
	else:
		return part['path']+'/'+part['title']+".md"


def partR(parts):

	firstPath=None

	brother=None

	bins=list()

	for part in parts:
		if part['href']==None:
			if part['subContents']!=None : # 有子集，父死子继
				part['path']=partR(part['subContents'])

				# if brother != None:
				# 	brother['path']=part['path']+"/"+part['title']+".md"

				# 	print 'brother:',brother['path']

				# 	brother=None
			else: # 没有子集
				bins.append(part)
				# parts.remove(part)
				continue

		if firstPath==None:
			firstPath=part['path']+"/"+part['title']+'.md'

	for part in bins:
		
		parts.remove(part)


		# print 'firstPath:',firstPath	

	return firstPath


	#  底层，找到，得到第一个


#  递归写入
def writeR(parts,file,level=1):
	
	if len(parts)<1:
		return

	for part in parts:
		# path=part['path']
		line =""
		# 存在文件
		if part['href']!=None:
			
			# 得到文件路径，part['path'] 是目录
			path=part['path']+'/'+part['title']+".md"
			line='{tag} * [{title}](/{path})\n'.format(tag=tab(part['level']-1,'  '),title=part['title'],path=path)

			# TODO 写入文章
			writeArticle(part['title'],level,part['path'],domain+part['href'])		
		else:

			line='{tag} * [{title}](/{path})\n'.format(tag=tab(part['level']-1,'  '),title=part['title'],path=part['path'])

		print line	


		file.write(line)

		if part['subContents']!=None:
			writeR(part['subContents'],file,level=level+1)
#  创建书籍


def creatArticle(directory,title,ext='md'):

	write_path=directory+'/'+title+".onwrite."+ext	# 写入中的路径
	success_path=directory+'/'+title+"."+ext		# 完成的路径

	# print 'write_path:',write_path

	if os.path.exists(success_path):
		log('book exist:'+success_path)
		return False

	if os.path.exists(write_path):
		log('last download eror,retry download:'+write_path)		
		os.remove(write_path)

	if not os.path.exists(directory):
		os.makedirs(directory)

	log('create new book:'+title)

	return write_path
# 完成文件的读写
def finishBook(path):

	newPath=path.replace('.onwrite.','.')

	os.rename(path,newPath)
	log('finishBook')


# 写文章
def writeArticle(title,level,path,url):

	# file_path=creatArticle(part['path'],part['title'])
	file_path=creatArticle(path,title,'md')

	if file_path==False:
		return

	body=requests.get(url)
	sel = Selector(text=body.text)
	title=sel.xpath("//div[@id='content']/h1/text()").extract()[0]
	stages=sel.xpath("//div[@id='content']/p/text()")

	with open(file_path, 'a') as f:

		f.write(tab(level,'#')+" "+title+"\n\n\n")
		for stage in stages:
			f.write('&emsp;&emsp;'+stage.extract()+"\n\n")

	finishBook(file_path)


# def checkParts(parts):

# 	if parts==None:
# 		return
# 	for part in parts:
# 		if part['path'].find('md')<0:
# 			print 'error:',part['title'],part['path']

# 		checkParts(part['subContents'])

def printParts(parts,level=1):

	if parts==None:
		return
	for part in parts:

		print '{tag}{title} : {path} ({href})'.format(tag=tab(level,'\t'),title=part['title'],path=part['path'],href=part['href'])
		

		printParts(part['subContents'],level+1)



# * [序](/序/README.md)
#   * [贾序](/序/intro01.md)
#   * [范序](/序/intro02.md)
#   * [查序](/序/intro03.md)
#   * [鲁序](/序/鲁序.md)
  
# * [章 2](/chapter2/README.md)
#   * [已知问题](/chapter2/issues.md)




if __name__=='__main__':

	bookName=u'景岳全书'
	url='http://www.zysj.com.cn/lilunshuji/jingyuequanshu/index.html'
	domain ='http://www.zysj.com.cn'

	parts=getContents(bookName,url)

	# print parts

	partR(parts)

	printParts(parts)

	path=u'./景岳全书.md'
	head='''---
ebook:
  title: 景岳全书
  cover: cover.png
  author: 张景岳
  comments: 明代张介宾撰，六十四卷。首选《内经》、《难经》、《伤寒》、《金匮》之论，博采历代医家精义，并结合作者经验，自成一家之书。
  publisher: sirius
  book-producer: sirius
  language: 中文
  tags: 中医, 诊断
  rating: 5
---
'''	

	with open(path, 'w') as f:
		f.write(head)

	with open(path, 'a') as f:

		writeR(parts,f)


	# title=u'阴阳篇（二）'
	# path=u'tst/卷之一入集·传忠录（上）'
	# url='http://www.zysj.com.cn/lilunshuji/jingyuequanshu/124-7-2.html'

	# writeArticle(title,3,path,url)





