from cryptography.fernet import Fernet
from pymongo import MongoClient
import pymongo
import hashlib
import hmac, timeit
def findDoc(key,id,db):
    
    client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
    mydb = client['SecMED']
    mycol = mydb[db]
    id_byte = str.encode(id)
    #generate MAC from patient id
    newhmac = hmac.new(key, id_byte, digestmod=hashlib.sha256)
    newmd = newhmac.hexdigest()
    try:
        document = mycol.find_one({'MD_id': newmd}) #find the wanted document by MD_id
        #print(document)
    except(pymongo.errors.ServerSelectionTimeoutError):
        print("Connection timeout")
        exit()
    
    return document
