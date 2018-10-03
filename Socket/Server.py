import socket
import sys

def CreateSocket():

	try:

		global port 
		global host
		global s
		port = 9999
		host = ""
		s = socket.socket()
		
	except socket.error as msg:
		print("Error CreateSocket. {0}".format(str(msg)))


def BindSocket():

	try:

		global host
		global port
		global s

		print("Binding the Port {0}".format(str(host)))

		s.bind((host,port))
		s.listen(5)
	
	except socket.error as msg:
		print("Error BindSocket. {0}\nRetriying...".format(str(host)))
		BindSocket()


def SocketAccept():

	conn, address = s.accept()
	print("Conn={0} IP={1} Port={2}".format(conn, address[0], address[1]))
	SendCommand(conn)
	conn.close()

def SendCommand(conn):
	
	while True:
		cmd = input()
		if cmd.upper() == 'QUIT':
		    conn.close()
		    s.close()
		    sys.exit()
		if len(str.encode(cmd)) > 0:
		    conn.send(str.encode(cmd))
		    client_response = str(conn.recv(1024),"utf-8")
		    #print(client_response, end="")
		    print(client_response)



def main():
	CreateSocket()
	BindSocket()
	SocketAccept()

main()
