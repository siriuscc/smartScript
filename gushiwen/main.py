# -*- coding: utf-8 -*-


import json
import requests
import urllib 
from scrapy.selector import Selector


headers ={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }


def parseConts(url,pageCount=-1):
    
    r=requests.get(url,headers=headers)
    sel=Selector(r)
    conts=sel.css('.main3 .left .sons .cont')
    tops=[]

    for cont in conts:
        item={
            'title':'',
            'rows':[]
        }   
        title=cont.css('b').xpath('text()')[0].extract()
        item['title']=title
        contsons=cont.css('.contson p').xpath('text()').extract()   
        if len(contsons)<1:
            contsons=cont.css('.contson').xpath('text()').extract()
        for row in contsons:
            line=row.replace("\n", "").strip()
            if len(line)>0:
                item['rows'].append(line)

        tops.append(item)
    
    if pageCount<0:
        try:
            pageCount=int(sel.css('#FromPage .pagesright span').xpath('text()').re('[0-9]+')[0])
        except BaseException as e:
            print e

    return tops,pageCount

def printList(songList):

    for item in songList:
        print item['title']
        # print len(item['rows'])
        for row in item['rows']:
            print '    '+row

def searchAuthor(author='毛泽东',page=1):

    # %E6%AF%9B%E6%B3%BD%E4%B8%9C
    author=urllib.quote(author) 
    url='https://so.gushiwen.org/search.aspx?type=author&page={page}&value={value}'.format(page=page,value=author)

    pageContent,pageCount=parseConts(url)

    while page<pageCount:
        page=page+1
        url='https://so.gushiwen.org/search.aspx?type=author&page={page}&value={value}'.format(page=page,value=author)
        nextPageContent,pageCount=parseConts(url,pageCount)

        pageContent.extend(nextPageContent)
        print 'download:'+str(page)+',size:'+str(len(pageContent))

    return pageContent





if __name__=='__main__':

    # tops=getTop('https://so.gushiwen.org/search.aspx?value=%E6%AF%9B%E6%B3%BD%E4%B8%9C&page=2')

    ls=searchAuthor()
    printList(ls)

   