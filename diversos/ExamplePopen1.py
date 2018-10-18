import subprocess
import re
import json

<<<<<<< HEAD
def findInformationCertificate(ip):

	data = {"certificate" :{}}
	SubjectExp = '^(\s+Subject:\s+)(.+)$'
	IssuerExp = '^(\s+Issuer:\s+)(.+)$'
	SizeKeyExp = '^(\s+Public-Key:\s+)(.+)$'
	#args = "openssl s_client -showcerts -servername 192.168.16.3 -connect gnupg.org:443 2>/dev/null"j
	args = "openssl s_client -connect {0}:443 2> /dev/null | openssl x509 -inform pem -noout -text".format(ip)
	p1 = subprocess.Popen(args,
			stdin = subprocess.PIPE, 
			stdout = subprocess.PIPE, 
			stderr = subprocess.PIPE,
			shell=True)

	output = p1.stdout.read()

	match = re.search(SubjectExp, output, re.MULTILINE)
	if match:
		Subject = match.group(2)
	
	match = re.search(IssuerExp, output, re.MULTILINE)
	if match:
		Issuer = match.group(2)

	match = re.search(SizeKeyExp, output, re.MULTILINE)
	if match:
		SizeKey = match.group(2)

	data['certificate']['Subject'] = Subject 
	json_data = json.dumps(data)

	data['certificate']['Issuer'] = Issuer
	json_data = json.dumps(data)

	data['certificate']['SizeKey'] = SizeKey
	json_data = json.dumps(data)

	return json_data

print (findInformationCertificate("192.168.16.3"))
=======
def count_lines(website):
    args = ['curl', website]
    args2 = ['wc', '-l']
    process_curl = subprocess.Popen(args, stdout=subprocess.PIPE,
                                    shell=False)
    process_wc = subprocess.Popen(args2, stdin=process_curl.stdout,
                                  stdout=subprocess.PIPE, shell=False)
    # Allow process_curl to receive a SIGPIPE if process_wc exits. 
    process_curl.stdout.close()
    return process_wc.communicate()[0]

print (count_lines("www.google.com"))
>>>>>>> 450f0cc444c339d7efe89899bcc0aa0fe68020bb
