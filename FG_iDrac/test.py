import requests
import logging
import httplib

# Debug logging
httplib.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
req_log = logging.getLogger('requests.packages.urllib3')
req_log.setLevel(logging.DEBUG)
req_log.propagate = True
url = "https://192.168.2.28/sysmgmt/2012/server/firmware/queue"

querystring = {"ST1":"4f8c70990896a42c9de7efc23ccb2e00"}

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
    'Cookie': "batteriesIcon=status_ok; fansIcon=status_ok; intrusionIcon=status_ok; removableFlashMediaIcon=status_ok; temperaturesIcon=status_ok; voltagesIcon=status_ok; powerSuppliesIcon=status_ok; sysidledicon=ledIcon%20grayLed; -http-session-=::http.session::276c3f8643560657605d8ccac0fc76bd; tokenvalue=4f8c70990896a42c9de7efc23ccb2e00",
    'Connection': "keep-alive",
    'Postman-Token': "104d6035-8d72-4b59-b0ec-55153e7d7416"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False)

print(response.text)

