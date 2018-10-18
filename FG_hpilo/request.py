import os
import json
import xml.etree.ElementTree as ET
import re
import requests
import subprocess
import time
try:
	    import http.client as http_client
except ImportError:
	    # Python 2
	        import httplib as http_client
		http_client.HTTPConnection.debuglevel = 1

requests.packages.urllib3.disable_warnings()

ILO_FW = 'https://192.168.16.3/cgi-bin/uploadRibclFiles' 
ILO_RIBC =  'https://192.168.16.3/ribcl' 
user = 'Administrator'
passwd = "67004833"

def make_request(sessionKey, fwlen):

	print("fwlen={0}".format(fwlen))

	root = ET.Element('RIBCL', VERSION = "2.0")
	login = ET.SubElement(root, 'LOGIN', USER_LOGIN = user.decode('string_escape'), PASSWORD = passwd)
	rib_info = ET.SubElement(login, 'RIB_INFO', MODE = 'write')
	ET.SubElement(rib_info,'TPM_ENABLED', VALUE = "Yes")
	ET.SubElement(rib_info,'UPDATE_RIB_FIRMWARE', IMAGE_LOCATION = "ilo4_260.bin", IMAGE_LENGTH = str(fwlen))

	print("VVVVVVVVVVVVVVVVVVVV")
	print(ET.tostring(root))
	print("AAAAAAAAAAAAAAAAAAAA")
	
	if hasattr(ET, 'tostringlist'):
            xml = b"\r\n".join(ET.tostringlist(root)) + b'\r\n'
        else:
            xml = ET.tostring(root)

	try:
		r = requests.post(ILO_RIBC
				,verify=False
				,headers={'Connection' : 'Close'}
				,cookies={'RibclFlash' : sessionKey[11:]}
				,data=xml)
	
	except Exception as e:
		print('Error: ' + str(e))
		return None


	print(r.status_code)
	print(r.text)


def upload_firmware():
 	filename = "/tmp/ilo4_260.bin"
	fwlen = os.path.getsize(filename)
	files={'files': open(filename,'rb')}
	r = requests.post(ILO_FW
			,verify=False
			,files=files
			)

	cookie = r.headers['Set-Cookie']
	print(cookie)
	return cookie, fwlen

if __name__ == '__main__':
	cookie, fwlen = upload_firmware()
	time.sleep(5)
	make_request(cookie, fwlen)
