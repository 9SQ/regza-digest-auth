import codecs
import json
from Crypto.Util import Padding
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import requests
from requests.auth import HTTPDigestAuth

ip = "192.168.1.3" # set your REGZA IP Address
user_id = "EC-21-E5-73-0B-9B" # set any user ID (MAC address format)

request_connection = "http://" + ip + "/v2/public/request_connection"
confirm_connection = "http://" + ip + "/v2/remote/confirm_connection"
cancel_connection = "http://" + ip + "/v2/public/cancel_connection"

payload = {
    'user_id': user_id
}

try:
    response = requests.post(request_connection, data=payload)
    regza = json.loads(response.text)

    if "status" in regza and regza["status"] == 0 :
        print("pin: ", end='')
        pin = input() # input displayed PIN code on REGZA

        encrypted_password = codecs.decode(regza["password"], 'hex')
        salt = regza["salt"]
        key = PBKDF2(pin.encode('ascii'), salt.encode('ascii'), count=1331)[:16]
        decryptor = AES.new(key, AES.MODE_CBC, IV=bytearray(16))
        decrypted_password = Padding.unpad(decryptor.decrypt(encrypted_password), AES.block_size, 'pkcs7').decode('ascii')

        print("user_id: " + user_id)
        print("user_pw: ", end='')
        print(decrypted_password)

        response = requests.post(confirm_connection, auth=HTTPDigestAuth(user_id, decrypted_password), data={})
        result = json.loads(response.text)

        if "status" in result and result["status"] == 0:
            print("Registration successful.")
        else:
            print("Registration failed.")
    else:
        print("Error.")

except KeyboardInterrupt:
    response = requests.post(cancel_connection, data=payload)
    regza = json.loads(response.text)

    if "status" in regza and regza["status"] == 0 :
        print("\nRegistration cancelled.")
    else:
        print("Error.")
