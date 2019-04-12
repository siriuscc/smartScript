喜马拉雅 免费资源爬虫



目标：

输入专辑URL，能爬取整个专辑：




先把免费的下载下来





专辑页：康震品读古诗词


sound-list _OO



通过专辑ID得到专辑信息：
https://www.ximalaya.com/revision/play/album?albumId=12826705&pageNum=1&sort=0&pageSize=30


播放信息：
https://mpay.ximalaya.com/mobile/track/pay/69202714?device=pc


音频页：
https://www.ximalaya.com/renwen/12826705/69192280



播放地址：
https://vod.xmcdn.com/download/1.0.0/group1/M00/16/50/wKgJN1pwWo7T8JzTAB-dUcbGXaI447.m4a?buy_key=aed65595bbd6d943057c57973f8b5b93&sign=97e319f07ca77a60135a8038b1cc51dd&timestamp=1554372392038000&token=8683&duration=669





获取 专辑下的音频列表，包括播放地址，只返回免费的

http://mobile.ximalaya.com/mobile/v1/album/track?albumId=12826705&device=android



// 获取一级分类列表
https://www.ximalaya.com/revision/category/breadcrumbCategoryInfo


// 可以拿到专辑的信息，没有播放地址，每一个音频称为track，对应一个trackId 
https://www.ximalaya.com/revision/album/getTracksList?albumId=12826705&pageNum=1


// 得到专辑信息
http://mpaywsa.ximalaya.com/mobile/track/pay/71512582/ts-1554380161325?device=android
albumId=12826705
trackId=71512582
title=【新春特辑】康震老师给大家拜年啦！
fileId=MY/1LM26omyXheXlT3HpQ7DbGJpHUNdbYKpIJRMzTdVFCzmNeyBUiShjVKtW1j2s5Mvk4z7hZwFPrefH+nTQbQ==
buyKey=fe4f133ccbf4b22dfa2a1e704ccbbda8
isAuthorized=True

