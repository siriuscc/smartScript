# coding:utf-8


import threadpool
import threading

import time





def sayhello(name,tag):
	for i in range(5):
		time.sleep(1)
		mutex = threading.Lock()
		
		mutex.acquire()

		print threading.currentThread().name,",name:",name,',tag:',tag

		mutex.release()

if __name__=='__main__':


	pool=threadpool.ThreadPool(4)

	dataList=[ ( [1,'a'],None),([2,'b'],None)]

	print dataList

	# # [2,'b'],[3,'c'],[4,'d'],[5,'e'],[6,'f'],[7,'g'],[8,'h'],[9,'j'],[10,'y']

	requests=threadpool.makeRequests(sayhello,dataList)



	for req in requests:
		pool.putRequest(req) 
	
	pool.wait()

