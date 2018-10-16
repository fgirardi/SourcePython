import socket
import sys

def CreateSocket():

	try:
		global host
		global port
		global s
		host =""
		port = 9999
		s = socket.socket()
	
	except socket.error as msg:
		print("Socket Creation error: {0}".format(str(msg)))
