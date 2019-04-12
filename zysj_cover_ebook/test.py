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






if __name__=='__main__':
	



	s='''
	<div id="content">
	<li data-hi="hi-14318" data-cc="1">卷之三十五天集·杂证谟
	<ul>
	<li data-hi="hi-14319" data-cc="2"><a href="/lilunshuji/jingyuequanshu/124-41-1.html" title="诸虫">诸虫</a></li>
	<li data-hi="hi-14320" data-cc="2"><a href="/lilunshuji/jingyuequanshu/124-41-2.html" title="诸毒（附虫毒）">诸毒（附虫毒）</a></li>
	</ul>
	</li>
	<li data-hi="hi-14321" data-cc="1">卷之三十六天集·杂证谟
	<ul>
	<li data-hi="hi-14322" data-cc="2"><a href="/lilunshuji/jingyuequanshu/124-42-1.html" title="诸气－经义">诸气－经义</a>
	<ul>
	<li data-hi="hi-14323" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14323" title="天地气（一）">天地气（一）</a></li>
	<li data-hi="hi-14324" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14324" title="阴阳气（二）">阴阳气（二）</a></li>
	<li data-hi="hi-14325" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14325" title="时气（三）">时气（三）</a></li>
	<li data-hi="hi-14326" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14326" title="运气（四）">运气（四）</a></li>
	<li data-hi="hi-14327" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14327" title="经气脏气（五）">经气脏气（五）</a></li>
	<li data-hi="hi-14328" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14328" title="脉气（六）">脉气（六）</a></li>
	<li data-hi="hi-14329" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14329" title="形气（七）">形气（七）</a></li>
	<li data-hi="hi-14330" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14330" title="血气（八）">血气（八）</a></li>
	<li data-hi="hi-14331" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14331" title="营卫气（九）">营卫气（九）</a></li>
	<li data-hi="hi-14332" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14332" title="谷气（十）">谷气（十）</a></li>
	<li data-hi="hi-14333" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14333" title="气味（十一）">气味（十一）</a></li>
	<li data-hi="hi-14334" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14334" title="酒气（十二）">酒气（十二）</a></li>
	<li data-hi="hi-14335" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14335" title="邪气（十三）">邪气（十三）</a></li>
	<li data-hi="hi-14336" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14336" title="病气（十四）">病气（十四）</a></li>
	<li data-hi="hi-14337" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14337" title="治气（十五）">治气（十五）</a></li>
	<li data-hi="hi-14338" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14338" title="总论气理（十六）">总论气理（十六）</a></li>
	<li data-hi="hi-14339" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14339" title="论调气（十七）">论调气（十七）</a></li>
	<li data-hi="hi-14340" data-cc="3"><a href="/lilunshuji/jingyuequanshu/124-42-1.html#hi-14340" title="述古（十八、共二条）">述古（十八、共二条）</a></li>
	</ul>
	</li>
	</ul>
	</li>
	</div>
	'''
	sel=Selector(text=s)

	li_set=sel.xpath('//div[@id="content"]/li')


	print len(li_set)
	for li_item in li_set:
		item=li_item.xpath('.//text()')

		print item[0].extract()
		print '---------------------------------------'
