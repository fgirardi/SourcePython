import Socket
import sys

def CreateSocket():

	try:

		global port = 9999
		global host = ""
		global s
		s = socket.socket()
		
	except socket.error as msg:
		print("Error CreateSocket. {0}".format(str(msg)))

