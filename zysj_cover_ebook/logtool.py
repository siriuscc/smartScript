
import threading


debugTag=False
logTag=False
errorTag=True

def error(url,e):
	if errorTag:
		with open('zysj.error', 'a') as f:	
			f.write('\t {thread} url:{url} \n'.format(thread=threading.currentThread().name,url=url))
			f.write('\t {thread} msg:{msg} \n'.format(thread=threading.currentThread().name,msg=e.message))
		
			f.write('\t {thread} traceback:{traceback} \n'.format(thread=threading.currentThread().name,traceback=traceback.format_exc()))
			
			f.write('\n\n')



def debug(msg):
	if debugTag:
		with open('zysj.debug', 'a') as f:
			f.write(threading.currentThread().name+':debug:'+msg+'\n')
		# print 'debug:',msg
		# log("currentThread"+":"+)

def log(msg):
	if logTag:
		print threading.currentThread().name+':log:',msg
	