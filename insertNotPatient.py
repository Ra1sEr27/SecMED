
from struct import pack
from cryptography.fernet import Fernet
import os
import getpass
from pymongo import MongoClient
import pymongo
import json
import hashlib
import hmac
import getpass

def insertNotPatient(key,accessdb,role):
    while(True):
        try:
            # connect to the MongoDB
            client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
            mydb = client["Hospital"]
            mycol = mydb[accessdb]
        except(pymongo.errors.ServerSelectionTimeoutError):
            print("Database is not existed")
        username = input("Enter name: ")
        if username == "exit":
            exit()
        elif username == "back":
            break
        while(True):
            password = getpass.getpass("Enter password: ")
            if password == "exit":
                exit()
            elif password == "back":
                break
            confirmpasswd = getpass.getpass("Enter password again: ")
            if confirmpasswd == "exit":
                exit()
            elif confirmpasswd == "back":
                break
            if password == confirmpasswd:
                break
            else:
                print("Passwords are not matched, please try again")
        
        if accessdb != "dataOwner": #generate staff id
            staffcolnumlist = []
            allcollist = mydb.list_collection_names()
            for i in range(len(allcollist)):
                if "staff" in allcollist[i]:
                    staffcolnumlist.append(allcollist[i][7])
            sorted_staffcolnumlist = []
            for i in range(len(staffcolnumlist)):
                sorted_staffcolnumlist.append(int(staffcolnumlist[i]))
            sorted_staffcolnumlist.sort()
            section_no = accessdb[7]
            section_no_int = int(section_no)
            if section_no_int in sorted_staffcolnumlist:
                directory = os.path.abspath('.') #get current directory of the folder
                dir_path = os.path.join(directory, "section{}-staff".format(section_no)) #open this dir to count files
            else:
                print("Invalid section")

            staff_id_first2digits = str(section_no)
            while(len(staff_id_first2digits) != 2):
                staff_id_first2digits = "0" + staff_id_first2digits
            
            staff_id_last4digits = 0
            staff_id = role[0] +staff_id_first2digits + "000" + str(staff_id_last4digits)
            dir_list = os.listdir(dir_path)
            dir_list_onlyID = []
            for i in range(len(dir_list)): #append all of the file names from the chosen folder
                dir_list_onlyID.append(dir_list[i][:7])
            while(staff_id in dir_list_onlyID): #increase the number of last 4 digits
                staff_id_last4digits = int(staff_id_last4digits)
                staff_id_last4digits += 1
                staff_id_last4digits = str(staff_id_last4digits)
                
                while(len(staff_id_last4digits) != 4): #pad 0 to the left of last 4 digits
                    staff_id_last4digits = "0" + staff_id_last4digits
                    #print("in loop ",staff_id_last4digits)
                staff_id = role[0] +staff_id_first2digits + str(staff_id_last4digits)
        else: #generate dataOwner id
            directory = os.path.abspath('.') #get current directory of the folder
            dir_path = os.path.join(directory, "dataOwner") #open this dir to count files
            staff_id_last4digits = 0
            staff_id = "a000000"
            dir_list = os.listdir(dir_path)
            dir_list_onlyID = []
            for i in range(len(dir_list)):
                dir_list_onlyID.append(dir_list[i][:7])
            #print(dir_list_onlyID)
            while(staff_id in dir_list_onlyID):
                staff_id_last4digits = int(staff_id_last4digits)
                staff_id_last4digits += 1
                staff_id_last4digits = str(staff_id_last4digits)
                while(len(staff_id_last4digits) != 4):
                    staff_id_last4digits = "0" + staff_id_last4digits
                staff_id = "a" + "00" + staff_id_last4digits
        #hash the password
        password_byte = str.encode(password)
        hmac1 = hmac.new(key, password_byte, digestmod=hashlib.sha256)
        #Create password MD from hmac1
        hashedpassword = hmac1.hexdigest()
        # create a json format from input
        
        doc = {"id": "{}".format(staff_id),"name": "{}".format(username), "password": "{}".format(hashedpassword), "role": "{}".format(role), "accessdb": "{}".format(accessdb)}
        doc_sorted = json.dumps(doc, indent=3)
        print("Document: \n{}".format(doc_sorted))
        # Convert JSON to string
        doc = json.dumps(doc)
        #encrypt the document
        
        doc_encrypted = encryptjson(key,doc)
        
        doc_encrypted_sorted = json.dumps(doc_encrypted, indent = 3)
        print("Encrypted document: \n", doc_encrypted_sorted)
        confirm = input("Do you want to insert the above encrypted document? (y/n/back/exit): ")
        if confirm == "y":
            try:
                if staff_id[0] == "a": #save to dataOwner folder
                    with open('./dataOwner/{}_{}.json'.format(staff_id,username),'w') as file:
                        file.write(doc_sorted)
                elif staff_id[0] in ("r","m"): #save to staff folder
                    with open('./section{}-staff/{}_{}.json'.format(section_no,staff_id,username),'w') as file:
                        file.write(doc_sorted)
                x = mycol.insert_one(doc_encrypted)
                print("The document has been saved to {} (id: {}).".format(accessdb,x.inserted_id))
            except(pymongo.errors.ServerSelectionTimeoutError, AttributeError):
                print("Cannot save the document")
        elif confirm == "n":
            break
        elif confirm == "back":
            pass
        elif confirm == "exit":
            exit()
        else:
            print("Invalid command, please try again")

def encryptjson(key,data_string):
    #start = timeit.default_timer()
    #print("Used key: ",key)
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
    
    # create MAC from key and data
    mac = hmac.new(key, data_byte, hashlib.sha256).digest()
    #print("key: {}, id: {}".format(key,id_byte))
    hmac1 = hmac.new(key, id_byte, digestmod=hashlib.sha256)
    #Create MD from hmac1
    md1 = hmac1.hexdigest()

    mac = mac.decode('ISO-8859-1')

    # convert bytes to string
    encrypted = encrypted.decode("ISO-8859-1")
    #encpname = encpname.decode("utf-8")

    # Upload ciphertext, MD and MAC to MongoDB
    doc = {'MD_id': '{}'.format(md1), 'CT': '{}'.format(
        encrypted), 'MAC': '{}'.format(mac)}
    doc_string = json.dumps(doc)
    #stop = timeit.default_timer()
    #print('Enc Time: ', stop - start)
    return doc
    
# with open('dataOwner.key', 'rb') as file:  #section1_staff.key , section2_staff.key, section3_staff.key . . . , section5_staff.key
#     dataOwner_key = file.read()
# insertdataOwner_registrar_staff(dataOwner_key,"dataOwner","inserterrole","dataOwner")