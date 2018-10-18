import os
import time

def set_new_date():

	fpath = ''
	for root, dirs, files in os.walk(fpath):
    	for name in files:
        	if name[-3:]=='.dv':
            	try:
                	t = time.mktime(time.strptime(name, 'clip-%Y-%m-%d %H;%M;%S.dv'))
                	os.utime(os.path.join(root,name), (t,t))
            	except ValueError as err:
                	print(root,name)
                	print(err)
