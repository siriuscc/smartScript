#coding:utf-8

from PIL import Image, ImageDraw
import numpy as np
import os


# 裁切图片,返回压缩裁切后的图片
def	cropImg(img,params):

	start_x=params['start_x']
	start_y=params['start_y']
	step=params['step']

	width=params['width']
	height=params['height']

	for i in range(5):
		region = (start_x,start_y,start_x+width
			,start_y+height)
		#裁切图片
		cropImg = img.crop(region)
		start_x=start_x+width+step
		yield cropImg


# 转换色彩模式rgb2hsv,色调H,饱和度S,明度V
def rgb2hsv(r, g, b):
	r, g, b = r/255.0, g/255.0, b/255.0
	mx = max(r, g, b)
	mn = min(r, g, b)
	df = mx-mn
	if mx == mn:
		h = 0
	elif mx == r:
		h = (60 * ((g-b)/df) + 360) % 360
	elif mx == g:
		h = (60 * ((b-r)/df) + 120) % 360
	elif mx == b:
		h = (60 * ((r-g)/df) + 240) % 360
	if mx == 0:
		s = 0
	else:
		s = df/mx
	v = mx
	return h, s, v


# 返回image 对象
# 根据明度 做黑白划分
def RGB2Int8(im):  
	# print "image info,",im.format,im.mode,im.size  
	(width,height)=im.size  
	# print 'size:',width,height
	R=0  
	G=0  
	B=0  
	pxs=im.load()
	for x in xrange(width):
		for y in xrange(height):

			px=pxs[x,y]

			h,s,v=rgb2hsv(int(px[0]),int(px[1]),int(px[2]))

			if v<0.5:
				pxs[x,y]=(0,0,0,255)
			else:
				pxs[x,y]=(255,255,255,255)
	
	# 黑白化
	im=im.convert('1')
	# 压缩1/4
	im=im.resize((width/4,height/4),Image.ANTIALIAS)
	# int 化
	im=im.convert('L')

	return im




# 加载测试集上的图片
def loadImg(path,kvList,params):

	for filename in os.listdir(path):  
		srcimg=Image.open(path+'/'+filename)
		print identifyNum(srcimg)
	
# TODO 


# 对原来的大图做切割
def identifyNum(srcimg,kvList,params={'start_x':124,'start_y':205,'step':13,'width':67,'height':83}):
	
	# 切割图片
	imgs=cropImg(srcimg,params)
	
	n=0
	for img in imgs:

		# 分类图片得到每一个位
		num=classifyImg(img,kvList)
		if num>=0 and num<=9:
			n=n*10+num
		else:
			break
	return n



# 分类图片
def classifyImg(img,kvList):

	# 先转为int格式
	img=RGB2Int8(img)

	narr=np.array(img,dtype=np.int)
	width,height=narr.shape			
	narr=narr.reshape(1,width*height)
	arr=np.sum(np.subtract(narr,kvList)**2,axis=1)
	
	for i in range(len(arr)):
		n=int(arr[i])
		if n==0:
			break

	if i>9:
		i=-1		
	return i

# 加载带标签的图片
def loadMap(path):
	savePath='train'
	h=20
	w=16
	mapList=np.zeros((11,w*h),np.int)
	for filename in os.listdir(path):  

		img=Image.open(path+'/'+filename)
		# 转为八位数
		img=img.convert('L')
		num=int(filename.split('_')[0])
		narr=np.array(img,dtype=np.int)
		narr=narr.reshape(1,w*h)
		mapList[num,:]=narr[:]

	return mapList


if __name__ == '__main__':

	pass
	# path='debug'
	# savePath='train'
	

	# kvList=loadMap(mapPath)

	# # loadImg(path,kvList)

	# #  测试一把identifyNum
	# img=Image.open('test1.png')
	# # print 

	# arr=np.array(RGB2Int8(img),np.int)
	# print arr

	# params={'start_x':124,'start_y':205,'step':13,'width':67,'height':83}
	# print identifyNum(img,kvList,params)

