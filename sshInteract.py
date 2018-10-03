import pexpect
import os
import sys
import time

connection_string = 'ssh root@192.168.1.91' 
pexpect_passwd = 'Password: '
password = 'root'

c = pexpect.spawn(connection_string)

ret = c.expect([pexpect_passwd, pexpect.EOF, pexpect.TIMEOUT])

if ret != 0:
	print("Err.1  Ret: [{0}]".format(ret))
	sys.exit(1)

c.sendline(password)
time.sleep(5)

ret = c.expect(['root@nodegrid:~#',pexpect.EOF, pexpect.TIMEOUT ])
if ret != 0:
	print("Err.2 Ret: [{0}]".format(ret))
	sys.exit(1)

os.write(1, c.match.group(0))
c.interact()
