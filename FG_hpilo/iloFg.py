self.read_response
self.save_request
self.timeout
self.port
def update_rib_firmware(self, filename=None, version=None, progress=None):

        # Backwards compatibility
        if filename == 'latest':
            version = 'latest'
            filename = None

        if filename and version:
            raise ValueError("Supply a filename or a version number, not both")

        if not (filename or version):
            raise ValueError("Supply a filename or a version number")

        current_version = self.get_fw_version()
        ilo = current_version['management_processor'].lower()
        filename = hpilo_fw.parse(filename, ilo)

        fwlen = os.path.getsize(filename)
        root, inner = self._root_element('RIB_INFO', MODE='write')
        etree.SubElement(inner, 'TPM_ENABLED', VALUE='Yes')
        inner = etree.SubElement(inner, 'UPDATE_RIB_FIRMWARE', IMAGE_LOCATION=filename, IMAGE_LENGTH=str(fwlen))
        self._upload_file(filename, progress)
            return self._request(root, progress)[1]

 
def _upload_file(self, filename, progress):
        with open(filename, 'rb') as fd:
            firmware = fd.read()
        boundary = b'------hpiLO3t%dz' % random.randint(100000,1000000)
        while boundary in firmware:
            boundary = b'------hpiLO3t%dz' % str(random.randint(100000,1000000))
        parts = [
            b"""--%s\r\nContent-Disposition: form-data; name="fileType"\r\n\r\n""" % boundary,
            b"""\r\n--%s\r\nContent-Disposition: form-data; name="fwimgfile"; filename="%s"\r\nContent-Type: application/octet-stream\r\n\r\n""" % (boundary, fsencode(filename)),
            firmware,
            b"\r\n--%s--\r\n" % boundary,
        ]
        total_bytes = sum([len(x) for x in parts])
        sock = self._get_socket()

        self._debug(2, self.HTTP_UPLOAD_HEADER % (total_bytes, boundary))
        sock.write(self.HTTP_UPLOAD_HEADER % (total_bytes, boundary))
        for part in parts:
            if len(part) < self.BLOCK_SIZE:
                self._debug(2, part)
                sock.write(part)
            else:
                sent = 0
                fwlen = len(part)
                while sent < fwlen:
                    written = sock.write(part[sent:sent+self.BLOCK_SIZE])
                    if written is None:
                        plen = len(part[sent:sent+self.BLOCK_SIZE])
                        raise IloCommunicationError("Unexpected EOF while sending %d bytes (%d of %d sent before)" % (plen, sent, fwlen))

                    sent += written
                    if callable(progress):
                        progress("Sending request %d/%d bytes (%d%%)" % (sent, fwlen, 100.0*sent/fwlen))

        data = ''
        try:
            while True:
                d = sock.read()
                data += d.decode('ascii')
                if not d:
                    break
        except socket.sslerror as exc: # Connection closed
            if not data:
                raise IloCommunicationError("Communication with %s:%d failed: %s" % (self.hostname, self.port, str(exc)))

        self._debug(1, "Received %d bytes" % len(data))
        self._debug(2, data)
        if 'Set-Cookie:' not in data:
            # Seen on ilo3 with corrupt filesystem
            body = re.search('<body>(.*)</body>', data, flags=re.DOTALL).group(1)
            body = re.sub('<[^>]*>', '', body).strip()
            body = re.sub('Return to last page', '', body).strip()
            body = re.sub('\s+', ' ', body).strip()
            raise IloError(body)
        self.cookie = re.search('Set-Cookie: *(.*)', data).group(1)
        self._debug(2, "Cookie: %s" % self.cookie)


 def _request(self, xml, progress=None):
        """Given an ElementTree.Element, serialize it and do the request.
           Returns an ElementTree.Element containing the response"""
        if not self.protocol and not self.read_response:
            self._detect_protocol()

        # Serialize the XML
        if hasattr(etree, 'tostringlist'):
            xml = b"\r\n".join(etree.tostringlist(xml)) + b'\r\n'
        else:
            xml = etree.tostring(xml)

        header, data =  self._communicate(xml, self.protocol, progress=progress)

        # This thing usually contains multiple XML messages
        messages = []
        while data:
            pos = data.find('<?xml', 5)
            if pos == -1:
                message = self._parse_message(data)
                data = None
            else:
                message = self._parse_message(data[:pos])
                data = data[pos:]

            # _parse_message returns None if a message has no useful content
            if message is not None:
                messages.append(message)

        if not messages:
            return header, None
        elif len(messages) == 1:
            return header, messages[0]
        else:
            return header, messages


def _get_socket(self):
        """https connection and do an HTTP/raw socket request"""
	class FakeSocket(object):
	        def __init__(self, rfile=None, wfile=None):
                    self.input = open(rfile, 'rb')
                    self.output =open(wfile, 'ab')
                    self.read = self.input.read
                    self.write = self.output.write
                    data = self.input.read(4)
                    self.input.seek(0)
                def close(self):
                    self.input.close()
                    self.output.close()
            sock = FakeSocket(self.read_response, self.save_request)
            return sock

        err = None
        for res in socket.getaddrinfo(self.hostname, self.port, 0, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            sock = None
            try:
		# Create a new socket using the given address family, socket type and protocol number
                sock = socket.socket(af, socktype, proto)
                sock.settimeout(self.timeout)
                sock.connect(sa)
            except socket.timeout:
                if sock is not None:
                    sock.close()
                err = "Timeout connecting to %s port %d" % (self.hostname, self.port)
            except socket.error as exc:
                if sock is not None:
                    sock.close()
                err = "Error connecting to %s port %d: %s" % (self.hostname, self.port, str(exc))

        if err is not None:
            raise err

        if not sock:
            err = "Unable to resolve %s" % self.hostname

        try:

        	return ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS)
        except ssl.SSLError as exc:
            raise IloCommunicationError("Cannot establish ssl session with %s:%d: %s" % (self.hostname, self.port, str(exc)))



def _communicate(self, xml, protocol, progress=None, save=True):
        sock = self._get_socket()
        msglen = len(self.XML_HEADER + xml)
        extra_header = b''
        extra_header = b"\r\nCookie: %s" % self.cookie.encode('ascii')
        http_header = self.HTTP_HEADER % (msglen, extra_header)
        msglen += len(http_header)
        sock.write(http_header)
        sock.write(xml)
        sock.close()
        data = ''
        try:
            while True:
                d = sock.read().decode('ascii', 'iloxml_replace')
                data += d
                if not d:
                    break
        except socket.sslerror as exc: # Connection closed
            if not data:
                raise IloCommunicationError("Communication with %s:%d failed: %s" % (self.hostname, self.port, str(exc)))

        sock.close()
        with open(self.save_response, 'a') as fd:
        	fd.write(data)

        # Do we have HTTP?
        header_ = ''
        if  data.startswith('HTTP/1.1 200'):
            header, data = data.split('\r\n\r\n', 1)
            header_ = header
            header = [x.split(':', 1) for x in header.split('\r\n')[1:]]
            header = dict([(x[0].lower(), x[1].strip()) for x in header])
            if header['transfer-encoding'] == 'chunked':
                _data, data = data, ''
                while _data:
                    clen, _data = _data.split('\r\n', 1)
                    clen = int(clen, 16)
                    if clen == 0:
                        break
                    data += _data[:clen]
                    _data = _data[clen+2:]

        elif data.startswith('HTTP/1.1 404'):
            # We must be using iLO2 or older, they don't do HTTP for XML requests
            # This case is only triggered by the protocol detection
            header = None

        else:
            header = None

        return header, data

    def _detect_protocol(self):
        # Use hponcfg when 'connecting' to localhost
        if self.hostname == 'localhost':
            self.protocol = ILO_LOCAL
            return
        # Do a bogus request, using the HTTP protocol. If there is no
        # header (see special case in communicate(), we should be using the
        # raw protocol
        header, data = self._communicate(b'<RIBCL VERSION="2.0"></RIBCL>', ILO_HTTP, save=False)
        if header:
            self.protocol = ILO_HTTP
        else:
            self.protocol = ILO_RAW


