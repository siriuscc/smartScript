# -*- coding: utf-8 -*-


import json
import requests
from scrapy.selector import Selector

headers ={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }




def getList():

    url='https://www.ximalaya.com/renwen/12826705/'

    r = requests.get(url,headers=headers)

    sel=Selector(r)
    lis=sel.css('.sound-list>ul>li._OO')
    songlist=[]

    for li in lis:

        try:
            link=li.css('.text>a')[0]
        except BaseException as e:
            print e
            print link.extract()

        item={
            'name':link.xpath('@title')[0].extract(),
            'link':link.xpath('@href')[0].extract()
        }
        songlist.append(item)

    return songlist


def songPage(songlist=list()):
    baseUrl='https://www.ximalaya.com'
    for item in songlist:
        print item['name']
        url=baseUrl+item['link']

        requests.get(url)
        Selector()


def getSongsDetail(albumId):

    url='http://mobile.ximalaya.com/mobile/v1/album/track?albumId={albumId}&device=android'.format(albumId=albumId)

    r=requests.get(url,headers=headers)
    js=json.loads(r.text.encode('utf-8'))


    songList=[]

    audios=js['data']['list']
    for item in audios:
        detail={
                'link64':item['playUrl64'],
                'link32':item['playUrl32'],
                'link164':item['playPathAacv164'],
                'link224':item['playPathAacv224'],
                'title':item['title'],
            }
        # print detail
        # print ''
        songList.append(detail)


    return songList




if __name__=='__main__':
  
    # songlist=getList()

    # songPage(songlist)
    # 可以得到免费的下载地址，没什么用啊
    print getSongsDetail(12826705)