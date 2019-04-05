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
# import imgSeek


# 获取屏幕尺寸
def _get_screen_size():
	size_str = os.popen('adb shell wm size').read()
	m = re.search('(\d+)x(\d+)', size_str)
	if m:
		width = m.group(1)
		height = m.group(2)
        return int(height),int(width)
		# return "{height}x{width}".format(height=height, width=width)


def clickPoint(x,y):
	cmd="adb shell input tap {x} {y}".format(x=x, y=y)
	os.system(cmd)


def main():


    i=0
    while True:
        clickPoint(500,1750)
        time.sleep(0.5)
        i=i+1

        if i%20==1:
            print("click {time} times".format(time=i));


# debug图片注释
def save_debug_creenshot(im, piece_x, piece_y, board_x, board_y,screenshot_backup_dir):

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
	im.save('{}_d.png'.format(screenshot_backup_dir))



if __name__ == '__main__':

	main()




