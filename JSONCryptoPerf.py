
from asyncio import start_server
from cryptography.fernet import Fernet
import json
import hashlib, rsa
import SigningPhasePerf
import os, subprocess, cpabe, keygenerator, timeit,time
def encryptjson(pid,certid,start,i):
    #start = timeit.default_timer()
    #--------Begin Encryption Phase----------
    #convert string to JSON
    # convert pname to byte format
    id_byte = str.encode(pid)
    #generate Symkey
    symkey = keygenerator.symkeygenerator(pid)
    with open('./Symkeys/{}_key.txt'.format(pid),'wb') as file:
        file.write(symkey)
    with open('./testpatient/{}.txt'.format(pid),'r') as file:
        doc = file.read()
    doc_byte = str.encode(doc, encoding="ISO-8859-1")
    # this encrypts the data read from your json and stores it in 'encrypted'
    #start = timeit.default_timer()
    CT_byte= Fernet(symkey).encrypt(doc_byte)
    
    #hash patient id
    id_MD = hashlib.sha256(id_byte).hexdigest()
    # convert bytes to string
    CT = CT_byte.decode("ISO-8859-1")
    #stop = timeit.default_timer()
    #print('Enc Time: ', stop - start)
    #encrypt SymKey with CP-ABE PubKey
    #print("here")
    cpabe.encrypt_key(pid)
    
    #rename encrypted symkey file to be able to read the file
    p = subprocess.call(["mv", "./Symkeys/{}_key.txt.cpabe".format(pid), "./Symkeys/{}_key.txt".format(pid)])
    
    #-----Begin Signing Phase------
    DS_XOR_R, R1, runtimexor = SigningPhasePerf.Sign(CT_byte,certid, id_MD)
    #stop = time.time()
    #print("Time({}): ".format(i),stop-start)
    #read the encrypted SymKey
    with open('./Symkeys/{}_key.txt'.format(pid),'rb') as file:
        enc_Symkey = file.read()
    #convert byte to string for storing in the DB
    enc_Symkey = enc_Symkey.decode("ISO-8859-1")
    #rename the symkey file
    p = subprocess.call(["mv", "./Symkeys/{}_key.txt".format(pid), "./Symkeys/{}_key.txt.cpabe".format(pid)])
    #Decrypt the local Symkey
    cpabe.decrypt("./Symkeys/{}_key.txt.cpabe".format(pid))
    # Form a JSON document for storing on cloud
    doc = {'MD_id': '{}'.format(id_MD), 'CT': '{}'.format(CT), 'enc_SK': '{}'.format(enc_Symkey),
    'DS*R': '{}'.format(DS_XOR_R), 'R1': '{}'.format(R1)}
    #stop = timeit.default_timer()
    #runtime = stop - start
    #print(doc)
    return doc, runtimexor

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