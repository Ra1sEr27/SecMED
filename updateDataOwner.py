from cryptography.fernet import Fernet
import getpass
from pymongo import MongoClient
import pymongo
import json
import hashlib
import hmac
import os
import symcrytjson

NoneType = type(None)
def updateDataOwner(key,wanteddoc):
    if type(wanteddoc) != NoneType: #Found the wanted document
        decdoc = symcrytjson.decryptjson(key,wanteddoc)
        
        decdoc_sorted = json.dumps(decdoc,indent = 6)
        print("{}'s document : \n{}".format(decdoc["id"],decdoc_sorted))
    
        while(True):
            edit_attr = input("Which {}'s attributes do you want to edit? (back->Enter staff name, exit->exit the program): ".format(decdoc["id"]))
            if edit_attr in decdoc:
                if edit_attr != "password":
                    new_val = input("Enter the new value of attribute {} (back->select attribute, exit->exit the program): ".format(edit_attr))
                    if new_val == "exit":
                        exit()
                    elif new_val=="back":
                        break
                else:
                    old_val = getpass.getpass("Enter the old password: ")
                    password_byte = str.encode(old_val)
                    hmac1 = hmac.new(key, password_byte, digestmod=hashlib.sha256)
                    #Create password MD from hmac1
                    old_val = hmac1.hexdigest()
                    if old_val == decdoc["password"]:
                        new_val = getpass.getpass("Enter the new password (back->select attribute, exit->exit the program): ")
                        if new_val == "exit":
                            exit()
                        elif new_val=="back":
                            break
                        while(True):
                            grantedpasswdchange = False
                            confirm = getpass.getpass("Enter your password again : ")
                            if confirm == "back":
                                break
                            elif confirm == "exit":
                                exit()
                            elif confirm == new_val:
                                print("Passwords are matched")
                                password_byte = str.encode(new_val)
                                hmac1 = hmac.new(key, password_byte, digestmod=hashlib.sha256)
                                #Create password MD from hmac1
                                new_val = hmac1.hexdigest()
                                grantedpasswdchange = True
                                break
                            else:
                                print("Passwords are not matched, please try again")
                    else:
                        print("Incorrect password")
                        grantedpasswdchange = False

                if edit_attr != "password" or grantedpasswdchange:
                    #apply new value to the selected attribute 
                    if edit_attr == "name":
                        origName = decdoc["name"]
                    decdoc[edit_attr] = new_val

                    #covert the edited document to string
                    edited_decdoc_string = json.dumps(decdoc)
                    edited_decdoc_string_sorted = json.dumps(decdoc, indent = 3)
                    #encrypt the edited document
                    encrypted_edited_decdoc = symcrytjson.encryptjson(key,edited_decdoc_string,"")

                    #reindent the edited document
                    edited_decdoc_sorted = json.dumps(decdoc, indent = 3)

                    #reindent the encryted edited document
                    encrypted_edited_decdoc_sorted = json.dumps(encrypted_edited_decdoc, indent = 3)

                    #print the results
                    edited_doc_lite = {"name": "{}".format(decdoc["name"]), "password": "{}".format(decdoc["password"]), "role": "{}".format(decdoc["role"]), "accessdb": "{}".format(decdoc["accessdb"])}
                    edited_doc_lite_sorted = json.dumps(edited_doc_lite, indent = 3)
                    
                    print("Edited {}'s document: \n{}".format(decdoc["id"],edited_doc_lite_sorted))
                    print("Encrypted edited {}'s document: \n{}".format(decdoc["id"],encrypted_edited_decdoc_sorted))

                    #update to the database
                    while(True): #If user input the unexpected command then ask again
                        confirm = input("Do you want to save the above encrypted document? (y/n/exit): ")
                        if confirm == "y":
                            try:
                                client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
                                db = client['Hospital'] #connect to db
                                staffcol = db["section{}-staff".format(decdoc["id"][2])]
                                staffcol.delete_one(wanteddoc)
                                staffcol.insert_one(encrypted_edited_decdoc)
                                #delete original local file name
                                f = open('./section{}-staff/{}_{}.json'.format(decdoc["id"][2],decdoc["id"],origName), 'w') #delete local file
                                f.close()
                                os.remove(f.name)
                                with open('./section{}-staff/{}_{}.json'.format(decdoc["id"][2],decdoc["id"],decdoc["name"]),'w') as file:
                                    file.write(edited_decdoc_string_sorted)
                                print("The document has been saved to {}".format(staffcol.name))
                            except(pymongo.http.ServerError):
                                print("Cannot save the document")
                            break
                        elif confirm == "n":
                            break
                        elif confirm == "exit":
                            exit()
                        else:
                            print("Invalid command, please try again")
                    if confirm in ("y","n"):
                        break
                            
            elif edit_attr=="back":
                break
            elif edit_attr == "exit":
                exit()
            else:
                print("Invalid attribute, please try again")
    else:
        print("There is no {}'s document stored in the system".format(decdoc["id"]))