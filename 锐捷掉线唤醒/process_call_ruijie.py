# -*- coding: utf-8 -*-



import psutil
import re
import sys
import os 
import win32api  
import time

# 结束进程
def killprocess(aim_name):

	pids=psutil.pids()
	# print pids

	aim_pid=-1

	for x in pids:
		p=psutil.Process(x)
		name=p.name()
		
		if (name==aim_name):
			aim_pid=x
			print "kill pid="+str(x)+" name="+name
			p.kill()
			break

def create_process(aim_path):
	win32api.ShellExecute(0, 'open', aim_path, '', '', 1)



if __name__=='__main__':
	win32api.ShellExecute(0, 'open', 'D:\\Opera.mp3', '', '', 1)         # 播放视频
	
	flag=os.system('ping baidu.com')
	while(True):
		if(flag==1):
			killprocess('8021x.exe')
			create_process(u'C:\Program Files\锐捷网络\Ruijie Supplicant\RuijieSupplicant.exe')
			flag=os.system('ping baidu.com')
		time.sleep(30)
		
		flag=os.system('ping baidu.com')



# >>> win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 0)           # 后台执行  
# >>>            # 前台打开  
# >>> win32api.ShellExecute(0, 'open', 'notepad.exe', '1.txt', '', 1)      # 打开文件  
# >>> win32api.ShellExecute(0, 'open', 'http://www.sohu.com', '', '', 1)   # 打开网页  
# >>> win32api.ShellExecute(0, 'open', 'D:\\Opera.mp3', '', '', 1)         # 播放视频
# >>> win32api.ShellExecute(0, 'open', 'D:\\hello.py', '', '', 1)          # 运行程序  

