import requests


def teste():

	ses = requests.Session()
	url = 'https://{0}/json/{1}'.format('192.168.2.150','login_session')
	res = ses.post(url = url
		,json={"method" : "login", "user_login" : "Administrator", "password" : "Adm1n1strat0r"}
		,verify=False) 

	print ("+++++++++++++++++++++++++++")
	print res.content
	print ("+++++++++++++++++++++++++++")

	print ("+++++++++++++++++++++++++++")
	print res.text
	print ("+++++++++++++++++++++++++++")

	print ("+++++++++++++++++++++++++++")
	print "ses.cookies:" + ses.cookies["sessionKey"]
	print ("+++++++++++++++++++++++++++")

	print ("+++++++++++++++++++++++++++")
	print "get_dict() "+ str(ses.cookies.get_dict())
	print ("+++++++++++++++++++++++++++")

	print ("---------------------------")
	print(ses)
	print ("---------------------------")



	return ses

if __name__ == '__main__':
	session = teste()
	print("****************************")
	print session.cookies["sessionKey"]
	print("****************************")
