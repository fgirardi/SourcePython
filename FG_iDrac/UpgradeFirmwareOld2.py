import requests
import sys
import json
import xml.etree.ElementTree as ET
import urllib3
urllib3.disable_warnings()
import logging
import httplib

# Debug logging
httplib.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
req_log = logging.getLogger('requests.packages.urllib3')
req_log.setLevel(logging.DEBUG)
req_log.propagate = True

url = "https://192.168.2.28/data/login"

payload = "user=root&password=NodeGridD3m0Passw0rd"
headers = {
    'Pragma': "no-cache",
    'Origin': "https://192.168.2.28",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    'Content-Type': "application/x-www-form-urlencoded",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Referer': "https://192.168.2.28/login.html",
    'Connection': "keep-alive",
    }
try:
	response = requests.request("POST", 
					url, 
					data=payload, 
					headers=headers,
					verify=False)
except requests.exceptions.RequestException as e:  # This is the correct syntax
	print e
	sys.exit(1)

tree = ET.ElementTree(ET.fromstring(response.text))
root = tree.getroot()
authResult =  root.findall('authResult')[0].text
if authResult != '0':
	print(root.findall('errorMsg')[0].text)
	sys.exit(1)

tmp = root.findall('forwardUrl')[0].text
forwardUrl = tmp.split(',')
ST1 = forwardUrl[0][15:]
ST2 = forwardUrl[1][4:]
print("ST1 " + ST1)
print("ST2 " + ST2)
httpSession = response.headers["Set-Cookie"].split(';')[0]
print("httpSession: " + httpSession)
httpSession = httpSession[15:]
print("httpSession: " + httpSession)

import requests

url = "https://192.168.2.28/sysmgmt/2012/server/firmware/queue"

querystring = {"ST1":ST1}

payload = "------WebKitFormBoundaryAhY35LjpQcniwzvg\\r\\nContent-Disposition: form-data; name=\"firmwareUpdate\"; filename=\"BIOS_C86TV_WN64_2.5.0.EXE\"\\r\\nContent-Type: application/x-msdownload\\r\\n\\r\\n\\r\\n------WebKitFormBoundaryAhY35LjpQcniwzvg--\\r\\n"
headers = {
    'Pragma': "no-cache",
    'Origin': "https://192.168.2.28",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    'Content-Type': "multipart/form-data; boundary=----WebKitFormBoundaryAhY35LjpQcniwzvg",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Referer': "https://192.168.2.28/cemgui/fwupdate.html?cat=C14&tab=T36&id=P48",
    'Cookie': "batteriesIcon=status_ok; fansIcon=status_ok; intrusionIcon=status_ok; removableFlashMediaIcon=status_ok; temperaturesIcon=status_ok; voltagesIcon=status_ok;powerSuppliesIcon=status_ok;sysidledicon=ledIcon%20grayLed; -http-session-={0}; tokenvalue={1}".format(httpSession,ST1),
    'Connection': "keep-alive",
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring,verify=False)

print(response.text)
