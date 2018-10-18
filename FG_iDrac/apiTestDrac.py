import json
import sys
import requests
from requests.auth import HTTPBasicAuth

IDRAC_REDFISH_POST_URL='https://{0}/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset'
IDRAC_REDFISH_GET_URL='https://{0}/redfish/v1/Systems/System.Embedded.1/'


requests.packages.urllib3.disable_warnings()
# Reset Types Allowed:
#On
#GracefulRestart 
#PushPowerButton 
#NMI

def getPower():

	r = requests.get(IDRAC_REDFISH_GET_URL.format('170.178.141.146')
			, verify=False
			, headers={'content-type':'application/json'}
			, auth=('root','NodeGridD3m0Passw0rd'))

	if r.status_code != requests.codes.ok:
		print('getPower. Err: '+ str(r.status_code))
		print(r.content)
		sys.exit(1)

	print(r.json()['PowerState'])

def setPower(resettype):
	if not resettype:
		resettype = 'ForceOff'

	payload = {'ResetType': resettype}
	headers = {'content-type': 'application/json'}

	print('Reset Type = ' + resettype)
	r = requests.post(IDRAC_REDFISH_POST_URL.format('170.178.141.146')
			, verify=False
			, headers = headers
			, auth=('root','NodeGridD3m0Passw0rd')
			, data=json.dumps(payload)
			# , json={'ResetType' : resettype}
			)

	
	if r.status_code == requests.codes.ok or r.status_code == 204:
		print('OK')
		print(r.content)
	else:
		print('setPower. Err: '+ str(r.status_code))
		print(r.content)
		sys.exit(1)



if __name__ == '__main__':

	if len(sys.argv) < 2:
		print "Use python apiTest.py g OR apiTest.py s"
		sys.exit(1)

	if sys.argv[1] == 'g':
		getPower()
	elif sys.argv[1] == 's':
		setPower(sys.argv[2] if len(sys.argv) == 3 else None)
	else:
		print "The parameter must be g = GET or s = SET"
		sys.exit(1)
