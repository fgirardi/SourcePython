import pexpect
import os
import sys

c = pexpect.spawn('ssh root@192.168.15.21')
ret = c.expect(['[Pp]assword: ',pexpect.EOF, pexpect.TIMEOUT])
if ret != 0:
	print("Err1")
	sys.exit(1)
c.sendline("root")

ret = c.expect(['root@nodegrid:~#',pexpect.EOF, pexpect.TIMEOUT ])
if ret != 0:
	print("Err2")
	sys.exit(1)

os.write(1, c.match.group(0))
c.interact()
