# coding:utf-8
import os
import re
import math
import time
import shutil
import subprocess
from PIL import Image, ImageDraw
import random
import numpy as np
import matplotlib.pyplot as plt
import imgSeek


# 获取屏幕尺寸
def _get_screen_size():
	size_str = os.popen('adb shell wm size').read()
	m = re.search('(\d+)x(\d+)', size_str)
	if m:
		width = m.group(1)
		height = m.group(2)
		return "{height}x{width}".format(height=height, width=width)


# 截图，并拉取截图
def pull_screenshot(path):

	# 新的方法请根据效率及适用性由高到低排序

	process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
	screenshot = process.stdout.read()
		
	binary_screenshot = screenshot.replace(b'\r\n', b'\n')

	f = open(path, 'wb')
	f.write(binary_screenshot)
	f.close()
	

# 转换色彩模式hsv2rgb
def hsv2rgb(h, s, v):
	h = float(h)
	s = float(s)
	v = float(v)
	h60 = h / 60.0
	h60f = math.floor(h60)
	hi = int(h60f) % 6
	f = h60 - h60f
	p = v * (1 - s)
	q = v * (1 - f * s)
	t = v * (1 - (1 - f) * s)
	r, g, b = 0, 0, 0
	if hi == 0: r, g, b = v, t, p
	elif hi == 1: r, g, b = q, v, p
	elif hi == 2: r, g, b = p, v, t
	elif hi == 3: r, g, b = p, q, v
	elif hi == 4: r, g, b = t, p, v
	elif hi == 5: r, g, b = v, p, q
	r, g, b = int(r * 255), int(g * 255), int(b * 255)
	return r, g, b

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

# 找到
def find_piece_and_board(im):
	width, height = im.size# w=1080,h=1920

	# 棋子的半高，自己量出来吧，不算了
	piece_base_height_1_2=20
	# 棋子的宽度
	piece_body_width=80
	# 棋子的位置
	piece_x_sum = 0
	piece_x_c = 0
	piece_y_max = 0

	from_left_find_board_y = 0
	from_right_find_board_y = 0

	scan_x_border = int(width / 8)  # 扫描棋子时的左右边界
	scan_start_y = 0  # 扫描的起始y坐标
	# 像素访问对象
	im_pixel=im.load()#1028*1920
	
	# 以50px步长，尝试探测scan_start_y,只扫描中间的1/3,找到应该扫描的区域
	for i in range(int(height / 3), int( height*2 /3 ), 50):
		# 获取一下第一行的最后一个节点，得到颜色
		last_pixel = im_pixel[0,i]

		for j in range(1, width):
			pixel=im_pixel[j,i]
			# 不是纯色的线，则记录scan_start_y的值，准备跳出循环
			if pixel[0] != last_pixel[0] or pixel[1] != last_pixel[1] or pixel[2] != last_pixel[2]:
				scan_start_y = i - 50
				break
		if scan_start_y:
			break

	# 从scan_start_y开始往下扫描，棋子应位于屏幕上半部分，这里暂定不超过2/3
	for i in range(scan_start_y, int(height * 2 / 3)):
		for j in range(scan_x_border, width - scan_x_border):  # 横坐标方面也减少了一部分扫描开销
			pixel = im_pixel[j,i]
			# 根据棋子的最低行的颜色判断，找最后一行那些点的平均值，这个颜色这样应该 OK，暂时不提出来
			# 找到棋子的像素点
			if (50 < pixel[0] < 60) and (53 < pixel[1] < 63) and (95 < pixel[2] < 110):
				piece_x_sum += j
				piece_x_c += 1
				piece_y_max = max(i, piece_y_max)# 尽量是最下面的那一行
				# print '(',j,',',i,'),'

	if not all((piece_x_sum, piece_x_c)):
		return 0, 0, 0, 0
	piece_x = piece_x_sum / piece_x_c
	piece_y = piece_y_max - piece_base_height_1_2  # 上移棋子底盘高度的一半

	# 得到棋子的位置(piece_x,piece_y)	
	min_b_y=height
	min_b_x=width
	max_b_x=0
	max_b_y=0

	# 目的板块的位置
	board_x = False
	board_y = 0
	board_px = 0

	findBox=False

	# 找到上顶点
	for i in range(int(height / 3), int(height * 2 / 3)):

		last_pixel = im_pixel[0, i]
		# 计算阴影的RGB值,通过photoshop观察,阴影部分其实就是背景色的明度V 乘以0.7的样子
		h, s, v = rgb2hsv(last_pixel[0], last_pixel[1], last_pixel[2])
		r, g, b = hsv2rgb(h, s, v * 0.7)

		if from_left_find_board_y and from_right_find_board_y:
			break

		# 还没找上边界 
		if not findBox:
			board_x_sum = 0
			board_x_c = 0

			for j in range(width):
				pixel = im_pixel[j,i]
				# 在棋子里面的像素点不检查
				if abs(j - piece_x) < piece_body_width:
					continue

				# 第一个和背景不一样颜色的区域，也就是下一个要跳的位置
				if abs(pixel[0] - last_pixel[0]) + abs(pixel[1] - last_pixel[1]) + abs(pixel[2] - last_pixel[2]) > 10:
					# min_b_x=j
					min_b_y=i
					board_x=j
					findBox=True
					# 这里加10是为了防止得到的是杂色上边界
					board_px=im_pixel[j,i+10]
					break
		else:
			break;

	# 找到下顶点
	for i in range(min_b_y,int(height * 2 / 3)):

		px=im_pixel[board_x,i]
		# 是同一个颜色，也就是盒子区域
		if abs(px[0]-board_px[0])+abs(px[1]-board_px[1])+abs(px[2]-board_px[2])<10:
			max_b_y=i

	board_y=(min_b_y+max_b_y)/2

	return piece_x, piece_y, board_x, board_y


# 跳跳时间
def jump(distance,swipe,press_lambda):
	press_time = distance * press_lambda
	press_time = max(press_time, 200)   # 设置 200 ms 是最小的按压时间
	press_time = int(press_time)

	# 随机原地跳舞，假装是个人
	rt=random.uniform(0.1,1)
	if rt>0.2 and rt<0.205:
		press_time=1

	# 这里点击的位置要稍微有点变化，要不然腾讯会认为你是机器人
	cmd = 'adb shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
		x1=int(swipe['x1'])+int(random.uniform(-20,20)),
		y1=int(swipe['y1'])+int(random.uniform(-20,20)),
		x2=int(swipe['x2'])+int(random.uniform(-30,30)),
		y2=int(swipe['y2'])+int(random.uniform(-30,30)),
		duration=press_time
	)
	os.system(cmd)
	return press_time

# debug图片注释
def save_debug_creenshot(ts, im, piece_x, piece_y, board_x, board_y,screenshot_backup_dir):

	draw = ImageDraw.Draw(im)
	# 对debug图片加上详细的注释
	draw.line((piece_x, piece_y) + (board_x, board_y), fill=2, width=3)
	draw.line((piece_x, 0, piece_x, im.size[1]), fill=(255, 0, 0))
	draw.line((0, piece_y, im.size[0], piece_y), fill=(255, 0, 0))
	draw.line((board_x, 0, board_x, im.size[1]), fill=(0, 0, 255))
	draw.line((0, board_y, im.size[0], board_y), fill=(0, 0, 255))
	draw.ellipse((piece_x - 10, piece_y - 10, piece_x + 10, piece_y + 10), fill=(255, 0, 0))
	draw.ellipse((board_x - 10, board_y - 10, board_x + 10, board_y + 10), fill=(0, 0, 255))
	del draw
	im.save('{}{}_d.png'.format(screenshot_backup_dir, ts))

def backup_screenshot(ts,screenshot_backup_dir):
	# 为了方便失败的时候 debug
	if not os.path.isdir(screenshot_backup_dir):
		os.mkdir(screenshot_backup_dir)
	shutil.copy('autojump.png', '{}{}.png'.format(screenshot_backup_dir, ts))


def clickPoint(x,y):
	cmd="adb shell input tap {x} {y}".format(x=x, y=y)
	os.system(cmd)

def retry():
	x=540
	y=1584
	clickPoint(x,y)

def GaussianGist(mu,sigma,k):

	# 高斯分布
	s=np.round(np.random.normal(mu,sigma,k),2)

	# 随机打乱，还是不开比较好
	# random.shuffle(s)

	# 输出图像
	# count, bins, ignored = plt.hist(s, 30, normed=True)
	# plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
	# 	linewidth=2, color='r')
	# plt.show()

	return s


def main():
	path='autojump.png'
	screenshot_backup_dir = 'debug/'
	mapPath='map'

	# 按压点：最好按照真实点设置，要不然腾讯可能会识别
	swipe={'x1':764,'x2':952,'y1':1460,'y2':1708}

	# 最大游戏次数
	gameMaxCount=10
	# 压力系数
	press_lambda=1.38
	# 最大步数
	maxStep=120
	# 最大分数
	maxScore=740

	# 正态参数，简单点说就是数据的发散程度
	sigma=10

	# 生成每一次游戏的步数和分数限制
	maxSteps=GaussianGist(maxStep,sigma,gameMaxCount+1)
	maxScores=GaussianGist(maxScore,sigma,gameMaxCount+1)

	print 'sirius jump,scan size:',_get_screen_size(),'\n'
	
	# 映射向量
	kvList=imgSeek.loadMap(mapPath)
	# 当前的游戏次数
	gameNum=0
	# 当前步数
	step=0
	while True:
		# 游戏开始
		if step==0:
			print '@--------------new game,gameNum:{gameNum},aim Step:{maxStep},aim Score:{maxScore}--------------@'.format(gameNum=gameNum,maxStep=int(maxSteps[gameNum]),maxScore=int(maxScores[gameNum]))
			time.sleep(1)# 载入游戏画面需要一点时间
		# 步进
		step=step+1

		# 抓取图片
		pull_screenshot(path)
		# 打开图片
		im = Image.open(path)

		# 分析图片
		piece_x, piece_y, board_x, board_y=find_piece_and_board(im)
		distance=math.sqrt((board_x - piece_x) ** 2 + (board_y - piece_y) ** 2)
		# 获取分数
		score=imgSeek.identifyNum(im,kvList)

		# 没有位移，意味着这局结束了
		if distance<1:
			print 'end game,gameNum={gameNum},step={step},score={score}\n\n'.format(gameNum=gameNum,step=step,score=score)
			# 当前步数重置，游戏数加一
			step=0
			gameNum=gameNum+1
		
			if gameNum>gameMaxCount:
				print 'game test to max count ,end continue'
				break

			# 等待两秒后重新开始游戏
			time.sleep(5)
			retry()
			continue

		# 超出最大步数限制，每次都失误
		if step>maxSteps[gameNum] or score>maxScores[gameNum]:
			print 'out of max limit [maxScore:{maxScore},maxStep:{maxStep}],add some error on every step'.format(maxScore=maxScore,maxStep=maxStep)
			distance=distance+random.uniform(100,200)

		press_time=jump(distance,swipe,press_lambda)
		print 'step:{step},score:{score} --> (x1:{x1},y1:{y1}),(x2:{x2},y2:{y2})\t press time is {press_time}'.format(
			step=step,score=score,x1=piece_x,y1=piece_y,x2=board_x,y2=board_y,press_time=press_time
			)

		# 保存debug信息
		# ts = int(time.time())
		# save_debug_creenshot(ts, im, piece_x, piece_y, board_x, board_y,screenshot_backup_dir)
		# backup_screenshot(ts,screenshot_backup_dir)

		# 距离远就需要长一点时间
		wait=1.0+distance/1000
		time.sleep(wait)

		# 模拟随机暂停
		rt=random.uniform(0.1, 1.0)
		if rt>0.2 and rt <0.3:
			print '*** random wait {rt} sec'.format(rt=rt)
			time.sleep(rt)
		elif rt>0.5 and rt<0.510:
			# 很小的概率,停个手
			print'*** random wait 5 sec'
			time.sleep(5)
		elif rt>0.6 and rt<0.6010:
			# 超级小的概率，停一些
			print '*** random wait {t} sec'.format(t=6+1/rt)
			time.sleep(6+1/rt)	


if __name__ == '__main__':

	main()


# 针对腾讯的识别
# 	修改一下手指的按压点，坐标要接近人的使用习惯，然后是每次要有随机
# 	加入随机停顿
# 	每一次游戏的步数服从正态分布

