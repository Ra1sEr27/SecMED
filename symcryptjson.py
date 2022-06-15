
from cryptography.fernet import Fernet
import json
import hashlib, rsa
import SigningPhase
import os, subprocess
def encryptjson(key,data_string):
    #start = timeit.default_timer()
    #convert string to JSON
    data_json = json.loads(data_string)
    print(type(data_json))
    #store name in name variable
    id = data_json["id"]
    #convert string to byte for encryption
    data_byte = str.encode(data_string)
    
    # convert pname to byte format
    id_byte = str.encode(id)
    # this encrypts the data read from your json and stores it in 'encrypted'
    fernet = Fernet(key)
    CT_byte= fernet.encrypt(data_byte)
    #hash patient id
    id_MD = hashlib.sha256(id_byte).hexdigest()
    # convert bytes to string
    CT = CT_byte.decode("ISO-8859-1")
    #encrypt SymKey with CP-ABE PubKey
    p = subprocess.call(["cpabe-enc", "pub_key", "{}_key.txt".format(id), "dataowner or medicalstaff"])
    #rename encrypted symkey file to be able to read the file
    p = subprocess.call(["mv", "{}_key.txt.cpabe".format(id), "{}_key.txt".format(id)])
    #-----Begin Signing Phase------
    DS = SigningPhase.Sign(CT_byte)
    #read the encrypted SymKey
    with open('{}_key.txt'.format(id),'rb') as file:
        enc_Symkey = file.read()
    # Upload ciphertext, MD and MAC to MongoDB
    doc = {'MD_id': '{}'.format(id_MD), 'CT': '{}'.format(CT), 'enc_SK': '{}'.format(enc_Symkey)}
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
with open('p010000_key.txt','rb') as file:
        symkey = file.read()
with open('/home/nontawat/SecMED/Patients/p010000_Intira Preecha.json','r') as file:
        pdoc = file.read()
#pdoc_string = json.dumps(pdoc)
#print(type(pdoc_string))
encryptjson(symkey, pdoc)