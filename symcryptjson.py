
from cryptography.fernet import Fernet
import json
import hashlib, rsa
import SigningPhase
import os, subprocess, cpabe
def encryptjson(data_string):
    #start = timeit.default_timer()
    #--------Begin Encryption Phase----------
    #convert string to JSON
    data_json = json.loads(data_string)

    #store name in name variable
    id = data_json["id"]
    #convert string to byte for encryption
    data_byte = str.encode(data_string)
    # convert pname to byte format
    id_byte = str.encode(id)
    #import Symkey
    with open('{}_key.txt'.format(id),'rb') as file:
        symkey = file.read()
    # this encrypts the data read from your json and stores it in 'encrypted'
    fernet = Fernet(symkey)
    CT_byte= fernet.encrypt(data_byte)
    #hash patient id
    id_MD = hashlib.sha256(id_byte).hexdigest()
    # convert bytes to string
    CT = CT_byte.decode("ISO-8859-1")
    #encrypt SymKey with CP-ABE PubKey
    cpabe.encrypt(id)
    
    print("test")
    #rename encrypted symkey file to be able to read the file
    p = subprocess.call(["mv", "{}_key.txt.cpabe".format(id), "{}_key.txt".format(id)])
    #-----Begin Signing Phase------
    DS_XOR_R, R1 = SigningPhase.Sign(CT_byte)
    #read the encrypted SymKey
    with open('{}_key.txt'.format(id),'rb') as file:
        enc_Symkey = file.read()
    #rename the symkey file
    p = subprocess.call(["mv", "{}_key.txt".format(id), "{}_key.txt.cpabe".format(id)])
    #Decrypt the local Symkey
    cpabe.decrypt(id)
    # Upload ciphertext, MD and MAC to MongoDB
    doc = {'MD_id': '{}'.format(id_MD), 'CT': '{}'.format(CT), 'enc_SK': '{}'.format(enc_Symkey),
    'DS*R': '{}'.format(DS_XOR_R), 'R1': '{}'.format(R1)}
    #stop = timeit.default_timer()
    #print('Enc Time: ', stop - start)
    print(doc)
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

    #convert string to byte
    CTbytes = str.encode(CT)
    #decrypt the ciphertext
    
    with open('dataOwner.key','rb') as file:
        check_key = file.read()

    fernet = Fernet(check_key)
    decdoc = fernet.decrypt(CTbytes)
    #convert the decrypted byte to string
    decdoc = decdoc.decode("utf-8")
    
    #convert string to json format
    decdoc = json.loads(decdoc)
    
    #stop = timeit.default_timer()
    #print('Dec Time: ', stop - start)
    return decdoc
#test code

with open('/home/nontawat/SecMED/Patients/p0000_Intira Preecha.json','r') as file:
        pdoc = file.read()
#pdoc_string = json.dumps(pdoc)
#print(type(pdoc_string))
encryptjson(pdoc)