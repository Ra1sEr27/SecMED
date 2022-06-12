
from cryptography.fernet import Fernet
import cryptography
import json
import hashlib
import hmac
import os, subprocess
def encryptjson(key,data_string):
    #start = timeit.default_timer()
    #convert string to JSON
    data_json = json.loads(data_string)
    #store name in name variable
    id = data_json["id"]
    #convert string to byte for encryption
    data_byte = str.encode(data_string)
    
    # convert pname to byte format
    id_byte = str.encode(id)
    # this encrypts the data read from your json and stores it in 'encrypted'
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data_byte)
    
    id_MD = hashlib.sha256(id_byte).hexdigest()
    # convert bytes to string
    encrypted = encrypted.decode("ISO-8859-1")
    #encrypt SymKey with CP-ABE PubKey
    p = subprocess.call(["program_name", "-input", i, "-output", o])
    # Upload ciphertext, MD and MAC to MongoDB
    doc = {'MD_id': '{}'.format(id_MD), 'CT': '{}'.format(
        encrypted), 'MAC': '{}'.format(mac)}
    #stop = timeit.default_timer()
    #print('Enc Time: ', stop - start)
    return doc

def decryptjson(key,doc):
    #start = timeit.default_timer()
    #store the stored ciphertext in CT
    try:
        CT = doc['CT']
    except(TypeError):
        print("Cannot find the document")
        return False
    #store the original MAC to origmac
    origmac = doc['MAC']
    #convert string to byte
    CTbytes = str.encode(CT)
    #decrypt the ciphertext
    
    with open('dataOwner.key','rb') as file:
        check_key = file.read()
        
    i = 0

    fernet = Fernet(check_key)

    decdoc = fernet.decrypt(CTbytes)

    #generate MAC for checking integrity
    mac = hmac.new(key, decdoc, hashlib.sha256).digest()
    mac = mac.decode('ISO-8859-1')
    
    #convert the decrypted byte to string
    decdoc = decdoc.decode("utf-8")
    
    #convert string to json format
    decdoc = json.loads(decdoc)
    
    #stop = timeit.default_timer()
    #print('Dec Time: ', stop - start)
    return decdoc
    