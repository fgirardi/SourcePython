import os

def filho():
	print('Ola eu sou o processo filho PID={0}'.format(os.getpid()))

def pai():
	while True:
		newPid = os.fork()
		if newPid == 0:
			filho()
		else:
			print('Ola eu sou o processo pai PID={0}. O PID do filho eh {0}'.format(os.getpid(), newPid))
		if input() == 'q':
			print('Fechando o Pai {0}'.format(os.getpid()))
			break


pai()