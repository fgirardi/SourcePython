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


def BindSocket():

	try

		global host
		global port
		global s

		print("Binding the Port {0}".format(str(host)))

		s.bind(host,port)
		s.listen(5)
	
	except socket.error as msg:
		print("Error BindSocket. {0}\nRetriying...".format(str(host)))
		BindSocket()


def SocketAccept():

	conn, address = s.accept()

	print("Conn={0} IP={1} Port={2}".format(conn, address[0], address[1]))
	SendCommand(conn)
	conn.close()
