
from cryptography.fernet import Fernet
import json
import hashlib, rsa
import SigningPhasePerf
import os, subprocess, cpabe, keygenerator, timeit
def encryptjson(pid,certid):
    #start = timeit.default_timer()
    #--------Begin Encryption Phase----------

    id_byte = str.encode(pid)
    #generate Symkey
    # this encrypts the data read from your json and stores it in 'encrypted'
    #start = timeit.default_timer()
    
    cpabe.encrypt_text(pid)
    #p = subprocess.call(["dataowner", "or", "medicalstaff"])
    #hash patient id
    id_MD = hashlib.sha256(id_byte).hexdigest()
    # convert bytes to string
    #CT = CT_byte.decode("ISO-8859-1")
    #stop = timeit.default_timer()
    #print('Enc Time: ', stop - start)
    #encrypt SymKey with CP-ABE PubKey
    #cpabe.encrypt(id)
    
    #rename encrypted json file to be able to read the file
    p = subprocess.call(["mv", "./patientCrypto/{}.txt.cpabe".format(pid), "./patientCrypto/{}.txt".format(pid)])
    #read the encrypted json file
    with open('./patientCrypto/{}.txt'.format(pid),'rb') as file:
        CT_byte = file.read()
    #-----Begin Signing Phase------
    #CT_byte = str.encode(CT, encoding="ISO-8859-1")
    DS_XOR_R, R1, runtime = SigningPhasePerf.Sign(CT_byte,certid, id_MD)

    #convert byte to string for storing in the DB
    CT = CT_byte.decode("ISO-8859-1")

    # Form a JSON document for storing on cloud
    doc = {'MD_id': '{}'.format(id_MD), 'CT': '{}'.format(CT),
    'DS*R': '{}'.format(DS_XOR_R), 'R1': '{}'.format(R1)}
    #stop = timeit.default_timer()
    #runtime = stop - start
    #print(doc['CT'])
    return doc, runtime

# def decryptjson(key,doc):
#     #start = timeit.default_timer()
#     #store the stored ciphertext in CT
#     try:
#         CT = doc['CT']
#     except(TypeError):
#         print("Cannot find the document")
#         return False
#     #store the original MAC to origmac

#     #convert string to byte
#     CTbytes = str.encode(CT)
#     #decrypt the ciphertext
    
#     with open('dataOwner.key','rb') as file:
#         check_key = file.read()

#     fernet = Fernet(check_key)
#     decdoc = fernet.decrypt(CTbytes)
#     #convert the decrypted byte to string
#     decdoc = decdoc.decode("utf-8")
    
#     #convert string to json format
#     decdoc = json.loads(decdoc)
    
#     #stop = timeit.default_timer()
#     #print('Dec Time: ', stop - start)
#     return decdoc
#test code

# with open('/home/nontawat/SecMED/Patients/p0000_Intira Preecha.json','r') as file:
#         pdoc = file.read()
# #pdoc_string = json.dumps(pdoc)
# #print(type(pdoc_string))
# encryptjson(pdoc)