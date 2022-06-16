from cryptography.fernet import Fernet
from pymongo import MongoClient
import pymongo
import hashlib, cpabe
def findDoc(id):
    client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
    mydb = client['EncryptedMTR']
    mycol = mydb['patient']
    id_byte = str.encode(id)
    #generate MAC from patient id
    id_MD = hashlib.sha256(id_byte).hexdigest()
    #print(id_MD)
    try:
        document = mycol.find_one({'MD_id': id_MD}) #find the wanted document by MD_id
        #print(document)
    except(pymongo.errors.ServerSelectionTimeoutError):
        print("Connection timeout")
        exit()
    #print(document)
    enc_SK = document["enc_SK"]
    #print(type(enc_SK))
    print(enc_SK)
    #store the enc_Symkey to local storage
    #enc_SK = str.encode(enc_SK)
    #print("Byte SK: ",enc_SK)
    # enc_SK.decode("ISO-8859-1")
    # print(enc_SK)
    with open('{}1_key.txt.cpabe'.format(id),'w') as file:
         file.write(enc_SK)
    #Decrypt the enc_Symkey
    cpabe.decrypt("p00011")
    # with open('{}1_key.txt'.format(id),'r') as file:
    #     Symkey = file.read()
    # print(Symkey)
    # return document
findDoc("p0001")
