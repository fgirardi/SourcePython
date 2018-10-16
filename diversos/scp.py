#!/usr/bin/python
# Python SCP and Expect Example 1.0
# Author: Fabiano Girardi
# Execute: scp.py file.txt

import pexpect
import sys
import time
import os

expectations = ['[Pp]assword',
		'continue (yes/no)?',
		pexpect.EOF,
		pexpect.TIMEOUT,
		'Name or service not known',
		'Permission denied',
		'No  such file or directory',
		'No route to host',
		'Network is unreachable',
		'failure in name resolution',
		'No space left on device'
		]

def fetchFileSCP(child=None, *args):
	print "*****Received Args:", args
	try:
		if not child:
			child = pexpect.spawn( 'scp -r root@192.168.15.21:/home/root/{0} ./{0}'.format(args[0]))
		res = child.expect( expectations )
		print "*****Child Exit Status:",child.exitstatus
		print res,"::",child.before,":After:",child.after
		if res == 0:
			child.sendline('root')
			return	fetchFileSCP(child,None)
		if res == 1:
			child.sendline('yes')
			return	fetchFileSCP(child,None)
		if res == 2:
			line = child.before
			print "*****Line:",line 
			print "*****Now check the result and return status."
		if res == 3:
			print "*****TIMEOUT Occurred."
			child.kill(0)
			return False
		if res >= 4:
			child.kill(0)
			print "*****ERROR:",expectations[res]
			return False
		return True
	except:
		import traceback; traceback.print_exc()
		print "*****Did file finish?"

if __name__ == '__main__':
	stat = fetchFileSCP(None,sys.argv[1])
	if stat:
		print "*****File Transferred successfully."
	else:
		print "*****Failure while copying files securely."
