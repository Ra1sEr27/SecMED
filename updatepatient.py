
from cryptography.fernet import Fernet
from pymongo import MongoClient
import pymongo
import json
import os
import findDoc
import symcrytjson
from pymongo import MongoClient
import pymongo


def updatePatient(key,patientdb):
    client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
    db = client['Hospital']
    patientcol = db[patientdb]
    #Enter patient name
    while(True):
        while(True):
            pid = input("Enter patient id: ")
            #type "exit" to terminate the program
            if pid == "exit":
                exit()
            elif pid == "back":
                #registrar.registrar(key,patientdb[7])
                break
            wanteddoc = findDoc.findDoc(key,pid,patientdb)
            if wanteddoc != "": #if function findDoc found the document then break the while loop
                break
            else:
                print("The wanted document is not found, please try again")
        if pid == "back":
            break
        decdoc = symcrytjson.decryptjson(key,wanteddoc)
        decdoc_sorted = json.dumps(decdoc, indent = 6)
        print("{}'s document: \n{}".format(pid,decdoc_sorted))

        while(True):
            edit_attr = input("Which {}'s attributes do you want to edit? (back->Enter staff name, exit->exit the program):".format(pid))
            if edit_attr in decdoc:
                
                while(True):
                    new_val = input("Enter the new value of attribute {} (back->select attribute, exit->exit the program): ".format(edit_attr))
                    if new_val == "exit":
                        exit()
                    elif new_val=="back":
                        break
                    else:
                        #apply new value to the selected attribute
                        origName = decdoc["name"] 
                        decdoc[edit_attr] = new_val

                        #covert the edited document to string
                        edited_decdoc_string = json.dumps(decdoc)
                        edited_decdoc_string_sorted = json.dumps(decdoc, indent = 6)
                        #encrypt the edited document
                        encrypted_edited_decdoc = symcrytjson.encryptjson(key,edited_decdoc_string,"")

                        #reindent the edited document
                        edited_decdoc_sorted = json.dumps(decdoc, indent = 6)

                        #reindent the encryted edited document
                        encrypted_edited_decdoc_sorted = json.dumps(encrypted_edited_decdoc, indent = 6)

                        #print the results
                        print("Edited {}'s document: \n{}".format(pid,edited_decdoc_sorted))
                        print("Encrypted edited {}'s document: \n{}".format(pid,encrypted_edited_decdoc_sorted))

                        #update to the database
                        while(True): #If user input the unexpected command then ask again
                            confirm = input("Do you want to save the above encrypted document? (y/n/exit): ")
                            if confirm == "y":
                                try:
                                    patientcol.delete_one(wanteddoc)
                                    patientcol.insert_one(encrypted_edited_decdoc)
                                    #delete original local file name
                                    f = open('./section{}-patient/{}_{}.json'.format(patientdb[7],pid,origName), 'w') #delete local file
                                    f.close()
                                    os.remove(f.name)
                                    with open('./section{}-patient/{}_{}.json'.format(patientdb[7],pid,decdoc["name"]),'w') as file:
                                        file.write(edited_decdoc_string_sorted)
                                    print("The document has been saved to {}".format(patientcol.name))
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
        