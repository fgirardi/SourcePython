import xml.etree.ElementTree as ET

test = '<?xml version="1.0" encoding="UTF-8"?> <root> <status>ok</status> <authResult>5</authResult> <errorMsg>Msg - Error</errorMsg></root>'

tmp = ET.ElementTree(ET.fromstring(test)) 
print(tmp)
root = tmp.getroot()
print(root.findall('errorMsg')[0].text)

