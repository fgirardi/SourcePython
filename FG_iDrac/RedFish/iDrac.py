import requests
import sys

def check_idrac_fw_support(idrac_ip, idrac_username, idrac_password):
    req = requests.get('https://%s/redfish/v1/UpdateService/FirmwareInventory/' % (idrac_ip), 
		        auth=(idrac_username, idrac_password), 
			verify=False)
    statusCode = req.status_code
    if statusCode == 400:
        print("WARNING, current server iDRAC version does not support Redfish firmware features. Refer to Dell online Redfish documentation for information on which iDRAC version supports firmware features.")
        sys.exit()
    else:
        pass

check_idrac_fw_support('192.168.2.28','root','NodeGridD3m0Passw0rd')
