import sys
sys.path.append('/usr/share/spm')
from helper import *

from jsondiff import diff
import glob
import json
import os
import re
import requests
import xml.etree.ElementTree as ET
import random
import socket 
import time
PY3 = sys.version_info[0] >= 3
if PY3:
	import urllib.request as urllib2
	class Bogus(Exception): pass
	socket.sslerror = Bogus
	basestring = str
	from os import fsencode
else:
	import urllib2
	fsencode = lambda x: x

data = '''
<RIBCL VERSION="2.0">
<LOGIN USER_LOGIN="{0}" PASSWORD="{1}">
      <{2} MODE="read">
         <{3}/>
      </{2}>
   </LOGIN>
</RIBCL>
'''

IFS='<?xml version="1.0"?>'

# we don't need a session, since all interactions with iLO are XML based
def needsSession(dev):
	return False

request_info = [('GET_ALL_USERS', ['USER_LOGIN']),
		('GET_NETWORK_SETTINGS', ['SNTP_SERVER1',
					'IPV6_ADDRESS']),
		('GET_SSO_SETTINGS', ['TRUST_MODE']),
		('GET_DIR_CONFIG',
			['DIR_AUTHENTICATION_ENABLED', \
					'DIR_LOCAL_USER_ACCT', \
					'DIR_SERVER_ADDRESS', \
					'DIR_SERVER_PORT', \
					'DIR_USER_CONTEXT_1', \
					'DIR_USER_CONTEXT_2', \
					'DIR_USER_CONTEXT_3', \
					'DIR_ENABLE_GRP_ACCT', \
					'DIR_GRPACCT1_NAME', \
					'DIR_GRPACCT1_PRIV', \
					'DIR_GRPACCT2_NAME', \
					'DIR_GRPACCT2_PRIV']),
		('GET_ENCRYPT_SETTINGS', ['ENABLE_REDUNDANCY']),
		('GET_SNMP_IM_SETTINGS', ['SNMP_ACCESS', \
							'SNMP_ADDRESS_1', \
							'SNMP_ADDRESS_1_ROCOMMUNITY', \
							'SNMP_ADDRESS_1_TRAPCOMMUNITY', \
							'SNMP_ADDRESS_2', \
							'SNMP_PORT', \
							'SNMP_TRAP_PORT']),
		('GET_FW_VERSION', ['FIRMWARE_VERSION', \
						'FIRMWARE_DATE', \
						'MANAGEMENT_PROCESSOR']),
		('GET_GLOBAL_SETTINGS', ['SESSION_TIMEOUT', \
						'SNMP_ACCESS_ENABLED', \
						'SNMP_PORT', \
						'SNMP_TRAP_PORT', \
						'SSH_PORT', \
						'SSH_STATUS', \
						'ENFORCE_AES', \
						'IPMI_DCMI_OVER_LAN_ENABLED', \
						'REMOTE_SYSLOG_ENABLE', \
						'REMOTE_SYSLOG_PORT', \
						'REMOTE_SYSLOG_SERVER_ADDRESS'])
		]

def GetLastFile(dev, suffix):
	os.chdir('/var/local/SPCONF')

	if suffix == "baseline":
		#baseline files is sorted by device type
                files = sorted(glob.glob('{0}_*.{1}'.format(dev.type, suffix)), reverse=True)
        else:
                #validate files is sorted by device name
                files = sorted(glob.glob('{0}_*.{1}'.format(dev.device_name, suffix)), reverse=True)

	if len(files) == 0:
		return None

	try:
		with open(files[0], 'r') as f:
			return json.loads(f.read())
	except:
		return None

def GetBaseline(dev):
	parsed = GetLastFile(dev, 'baseline')
	if parsed:
		print(json.dumps(parsed, indent=4, sort_keys=True))

def SPshowConfig(dev):
	parsed = GetLastFile(dev, 'validate')
	if parsed:
		print(json.dumps(parsed, indent=4, sort_keys=True))

def SPshowDiff(dev):
	baseline = GetLastFile(dev, 'baseline')
	validate = GetLastFile(dev, 'validate')

	if not baseline or not validate:
		return

	return diff(baseline, validate, syntax='symmetric')

def makeRequest(dev, xml):
	try:
		ret = requests.post('https://{0}/ribcl'.format(dev.ip)
				, headers = {'User-Agent' : 'locfg-Perl-script/4.80'}
				, data = xml
				, verify = False)
	except Exception as e:
		print('Error: ' + str(e))
		return None

	if ret.status_code != 200:
		print('Error: request returned ' + str(ret.status_code))
		return None

	return ret.text

def checkResultRequestGetConfig(data, info):
	# split the multiple XMLs inside the reponse, and check for the one who
	# contains the tag we want
	xml = ''
	for i in ''.join(data).strip().split(IFS):
		if info in i:
			xml = IFS + i

	# if the requested info is license dependant, get the last XML from the
	# request
	if not xml:
		xml = IFS + data.split(IFS)[-1]

	xml_root = ET.fromstring(xml)

	err = xml_root.findall('.//RESPONSE')[0].get('STATUS')
	# 0x0000 mean that no error was returned
	if err != '0x0000':
		print('Error: ' + xml_root.findall('.//RESPONSE')[0].get('MESSAGE'))
		return None

	return xml_root

def checkResultRequestModify(data):
	"""
	Return only invalid massages
	"""

	data = data.strip()
	if not data:
		return ''

	msg_ret_xml = None
	msg = ''
	try:
		msg_ret_xml = ET.fromstring(data)
	except ET.ParseError:
		return ''

	if msg_ret_xml.tag != 'RIBCL':
		return ''

	for child in msg_ret_xml:
		if child.tag == 'RESPONSE':
			if child.get('STATUS') != '0x0000' or child.get('MESSAGE') != 'No error':
				msg = str(child.get('STATUS')) + ' ' + str(child.get('MESSAGE')) 
		if child.tag == 'INFORM':
			if msg != '':
				msg = msg + ' information: [' + child.text + ']' 

	return msg 

def SPsetConfig(dev):
	"""
	Set Config default to ILo device
	"""

	result = 0
	root = ET.Element('RIBCL', VERSION = "2.0")
	login = ET.SubElement(root, 'LOGIN', USER_LOGIN = dev.user.decode('string_escape'), PASSWORD = dev.passwd)
	rib_info = ET.SubElement(login, 'RIB_INFO', MODE = 'write')

	# First take the difference between baseline and validate.
	json_diff = SPshowDiff(dev)
	# Iterate the json
	if json_diff is None:
		return 0

	for p_id, p_info in json_diff.items():
		# each feature has a especifc command modifies.
		mod = 'MOD' + p_id[3:].upper() 
		# Don't have a set config to modify all users or don't have a set config to firmware version
		if mod in ['MOD_ALL_USERS', 'MOD_FW_VERSION']:
			continue

		settings = ET.SubElement(rib_info, mod)
		for key in p_info:
			key_format = key.upper()
			value_format = p_info[key][0].upper()
			ET.SubElement(settings, key_format, VALUE = value_format)

	# Convert to string because the parameter data only accept string
	data = makeRequest(dev, ET.tostring(root, 'utf-8', method="xml"))
	if data is None:
		return 1

	# The return contains various XML 
	messages = []
	while data:
		# do a loop jumping to next xml head
		pos = data.find('<?xml', 5)
		if pos == -1:
			# if not found a new xml head means that there no more xml, so parse the last.
			message = checkResultRequestModify(data) 
			data = None
		else:
			# check the next xml message
			message = checkResultRequestModify(data[:pos])
			# increase to next head of xml
			data = data[pos:]

		if message != '':
			# do a append to array of messages.
			messages.append(message)

	print('\n'.join(messages).strip())

	return 0

param = {'GET_NETWORK_SETTINGS' : 'RIB_INFO',
		'GET_SSO_SETTINGS' : 'SSO_INFO',
		'GET_DIR_CONFIG' : 'DIR_INFO',
		'GET_ENCRYPT_SETTINGS' : 'RIB_INFO',
		'GET_SNMP_IM_SETTINGS' : 'RIB_INFO',
		'GET_FW_VERSION' : 'RIB_INFO',
		'GET_GLOBAL_SETTINGS' : 'RIB_INFO',
		'GET_ALL_USERS' : 'USER_INFO'
	}

def getRibCLI(dev, jn, info, info_list):
	try:
		xml_root = makeRequest(dev,  data.format(dev.user.decode('string_escape'),
					dev.passwd,
					param[info],
					info))
		if xml_root is None:
			return False

		xml_ret = checkResultRequestGetConfig(xml_root, info)
		if xml_ret is None:
			return False

		jn[info.lower()] = {}
		for i in info_list:
			field = xml_ret.findall('.//' + i)

			if field:
				# when getting users, return all users in a list
				if info == 'GET_ALL_USERS':
					v = [ f.get('VALUE') for f in field ]

				# ipv6_address can return multiple XML nodes with the same name
				elif info == 'GET_NETWORK_SETTINGS' and i == 'IPV6_ADDRESS':
					val = [ f.get('ADDR_STATUS', '') for f in field ]
					v = 'Enable' if 'ACTIVE' in val else 'Disable'

				else:
					v = field[0].get('VALUE')

			# when getting firmware version, the root tag does not include
			# subtabs, so grab the attributes when no subtag exists
			else:
				v = xml_ret.findall('.//' + info)
				if v:
					v = v[0].get(i)

				# license dependant request can fail, so only check for a msg
				# field
				if not v:
					v = xml_ret.findall('.//RESPONSE')[0].get('MESSAGE')

			jn[info.lower()][i.lower()] = v

	except Exception as e:
		print(json.dumps({'device' : dev.device_name, 'status' :
			'error', 'message' : str(e)}, indent=4))
		return False

	return True

def SPgetConfig(dev):
	json_ret = {}

	for req in request_info:
		if req[0] == 'GET_ENCRYPT_SETTINGS':
			continue
		if not getRibCLI(dev, json_ret, req[0], req[1]):
			return 1

	print(json.dumps(json_ret, indent=4, sort_keys=True))

def SPgetFWVersion(dev):
	j = {}
	getRibCLI(dev, j, 'GET_FW_VERSION', ['FIRMWARE_VERSION'])
	print(j.get('get_fw_version', {}).get('firmware_version', ''))

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
                print("Connecting to %s port %d" % sa[:2])
                sock.connect(sa)
            except socket.timeout:
                if sock is not None:
                    sock.close()
                    print("Timeout connecting to %s port %d" % (hostname, port))
            except socket.error as exc:
                if sock is not None:
			sock.close()
			print("Error connecting to %s port %d: %s" % (hostname, port, str(exc)))
	
	if not sock:
		print("Unable to resolve %s" % hostname)

	try:
		result = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS)
	except ssl.SSLError as exc:
		print("Cannot establish ssl session with %s:%d: %s" % (self.hostname, self.port), str(exc))

	return result

def upload_file(filename):
	BLOCK_SIZE = 64 * 1024
	HTTP_UPLOAD_HEADER = b"POST /cgi-bin/uploadRibclFiles HTTP/1.1\r\nHost: localhost\r\nConnection: Close\r\nContent-Length: %d\r\nContent-Type: multipart/form-data; boundary=%s\r\n\r\n"
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
	
        sock = open_socket()

        sock.write(HTTP_UPLOAD_HEADER % (total_bytes, boundary))
        for part in parts:
		if len(part) < BLOCK_SIZE:
                	sock.write(part)
		else:
                	sent = 0
                	fwlen = len(part)
                	while sent < fwlen:
				written = sock.write(part[sent:sent+BLOCK_SIZE])
			
				if written is None:
                        		plen = len(part[sent:sent+BLOCK_SIZE])
                        		print("Unexpected EOF while sending %d bytes (%d of %d sent before)" % (plen, sent, fwlen))

				sent += written

        data = ''
        try:
            while True:
                d = sock.read()
                data += d.decode('ascii')
                if not d:
                    break
        except socket.sslerror as exc: # Connection closed
            if not data:
                print("Communication with %s:%d failed: %s" % ('192.168.16.3', 443, str(exc)))

        if 'Set-Cookie:' not in data:
            # Seen on ilo3 with corrupt filesystem
            body = re.search('<body>(.*)</body>', data, flags=re.DOTALL).group(1)
            body = re.sub('<[^>]*>', '', body).strip()
            body = re.sub('Return to last page', '', body).strip()
            body = re.sub('\s+', ' ', body).strip()
	    print("Error: {0}".format(body))
	
	cookie = re.search('Set-Cookie: *(.*)', data).group(1)
        print("Cookie: %s" % cookie)
	return cookie

def communicate(xml, cookie):
	hostname = '192.168.16.3'
	port = 443

        HTTP_HEADER = b"POST /ribcl HTTP/1.1\r\nHost: localhost\r\nContent-Length: %d\r\nConnection: Close%s\r\n\r\n"
    	XML_HEADER = b'<?xml version="1.0"?>\r\n'
	sock = open_socket()
	msglen = len(XML_HEADER + xml)
        extra_header = b"\r\nCookie: %s" % cookie.encode('ascii')
	http_header = HTTP_HEADER % (msglen, extra_header)
	msglen += len(http_header)
	print("http_header={0}".format(http_header))
	sock.write(http_header)
	print("XML_HEADER={0}".format(XML_HEADER))
	sock.write(XML_HEADER)
	print("xml={0}".format(xml))
	sock.write(xml)
	data = ''
        try:
            while True:
                d = sock.read().decode('ascii', 'iloxml_replace')
                data += d
                if not d:
                    break
                if d.strip().endswith('</RIBCL>'):
			d = d[d.find('<?xml'):]
                    	while '<?xml' in d:
				end = d.find('<?xml', 5)
                        	if end == -1:
                            		msg = d
                            		if msg:
                                		print(msg)
                            		break
                        	else:
					msg = d[:end]
					if msg:
                                		print(msg)
                            		d = d[end:]

        except socket.sslerror as exc: # Connection closed
            if not data:
                print("Communication with %s:%d failed: %s" % (hostname, port, str(exc)))

        print(1, "Received %d bytes" % len(data))

def SPUpdateFirmware(dev):

	filename = "/tmp/ilo4_260.bin"
	fwlen = os.path.getsize(filename)
	root = ET.Element('RIBCL', VERSION = "2.0")
	login = ET.SubElement(root, 'LOGIN', USER_LOGIN = dev.user.decode('string_escape'), PASSWORD = dev.passwd)
	rib_info = ET.SubElement(login, 'RIB_INFO', MODE = 'write')
	ET.SubElement(rib_info,'TPM_ENABLED', VALUE = "Yes")
	ET.SubElement(rib_info,'UPDATE_RIB_FIRMWARE', IMAGE_LOCATION = "ilo4_260.bin", IMAGE_LENGTH = str(fwlen))
	
	# Serialize the XML
        if hasattr(ET, 'tostringlist'):
            xml = b"\r\n".join(ET.tostringlist(root)) + b'\r\n'
        else:
            xml = ET.tostring(root)

	cookie = upload_file(filename)
	time.sleep(5)
	print (xml)
	communicate(xml, cookie)
	time.sleep(5)
	#data = makeRequest(dev, xml)
	#print("data={0}".format(data))
	#if data is None:
	#	return 1


