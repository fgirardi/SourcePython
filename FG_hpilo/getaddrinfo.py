import socket
import ssl

def open_socket():

	if not hasattr(ssl, 'PROTOCOL_TLS'):
		    ssl.PROTOCOL_TLS = ssl.PROTOCOL_SSLv23

	hostname = '192.168.16.3'
	port = 443
	for res in socket.getaddrinfo(hostname, port, 0, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            sock = None
            try:
                sock = socket.socket(af, socktype, proto)
                sock.settimeout(3000)
		print("af={0}".format(af))
		print("socktype={0}".format(socktype))
		print("proto={0}".format(proto))
                print(2, "Connecting to %s port %d" % sa[:2])
                sock.connect(sa)
            except socket.timeout:
                if sock is not None:
                    sock.close()
                    print("Timeout connecting to %s port %d" % (hostname, port))
            except socket.error as exc:
                if sock is not None:
			sock.close()
			print("Error connecting to %s port %d: %s" % (hostname, port, str(exc)))

	try:
		result = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS)
	except ssl.SSLError as exc:
		print("Cannot establish ssl session with %s:%d: %s" % (self.hostname, self.port), str(exc))

if __name__ == '__main__':
	open_socket()
	
