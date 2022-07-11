import base64
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64, hashlib, random, timeit, pymongo, datetime, json, math
from random import choice
import binascii

client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
#client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client['EncryptedMTR']
Data_owner_list = []
mycol_audit = mydb['AuditLog']
mycol_patient = mydb['patient']
item_details = mycol_audit.find()
templist = []
thislist = []
no =0
def XOR (a, b):
    if a != b:
        return 1
    else:
        return 0

document_audit = mycol_audit.find_one({'MD_id': "a4d5e07e23b14fef41dbb972621cf67d2fc47e6614f6c61bc0b598ac474343c5"})
timestamp = ''
for i in document_audit:
    if (i[0:2] == "20"):
        timestamp = timestamp+i
print(timestamp)
#time = document[3]
R1 = document_audit[timestamp]['R1']
#print(len(R1))
#print("R1=",R1)
#print(type(R1))
#R1 = use the R*1 from the input ID

constR = "111011101110011010000100101111000101000100100101111001010000110010010000110110001111000110010001101111010100010010101110000101000101110100001001011010111100001001110111011101110101111011111011111110010010101010010001101010001000000011001001001111000100100100001001000111011001111001111110100101011111011001101101100110111100111100011100011100011010000010101010011010000011100001011011110011010010001010000010111001010001110011010010000000001001101100010001110111111101100111100000010110000101000011010110010001111000001010011001001001100001101101000101101010010010001101111111011001111111010000011010011101001100001010011111101100011010111101001001100001001100011000001011100010011111010110110100010111011100001100111000101000110110100010111100100111011001101000010100111010100010010011111010110010000111111001010001111111011001110110000001000100010011101010110011001001111011000101001111110111111110010110000111010110000100011001101001000000001101011100110100000000101110001001100000111100111000101110010011001100110110001110001110101100000111000011011010101001111010001110011110110000001101101010100111101000111001111011000"
constR = constR + constR 
R = "" 
for i in range(len(R1)):
    temp1 = XOR(R1[i],constR[i])
    R += str(temp1)
#print("R = ",R)
DS_R = document_audit[timestamp]['DS*R']
# XOR DS_Binary with R value
DS = ''
for i in range(len(DS_R)):
    temp1 = XOR(DS_R[i],R[i])
    DS += str(temp1)
#print(len(DS))
#print("DS_R =",DS_R)
#print("R =",R)
#print("DS =",DS)
audit_priv = document_audit[timestamp]['PrivKey']
#print(audit_priv)
certid = "DO0000"
with open('./RSAKeyCloud/{}_RSA_pubkey.pem'.format(certid),'w') as file:
    file.write(audit_priv)
f = open('{}_RSA_pubkey.pem'.format(certid),'r')

pubkey = RSA.import_key(f.read())
CT_RSA_Pubkey = PKCS1_OAEP.new(pubkey)
#encrypt MD with RSA -> Get DS
print(hex(int(DS, 2)))
binary_int = int(DS, 2)
# Getting the byte number
#print(binary_int)
byte_number = binary_int.bit_length()
#print(byte_number)
# Getting an array of bytes
binary_array = binary_int.to_bytes(190, "big")
#print("BA: ",binary_array)
DS_text = binary_array.decode('ISO-8859-1')
#DS_byte = DS_text.encode()
#print(len(DS_text)) 
DS_byte = CT_RSA_Pubkey.decrypt(DS_text)
#print(DS_byte)
'''
CT_RSA_Pubkey = PKCS1_OAEP.new(audit_priv)
#encrypt MD with RSA -> Get DS
DS_byte = CT_RSA_Pubkey.decrypt(CT_MD_byte)



#--------------------------------------------------------------
patient = "p0000"
patient= str.encode(patient)
hash_patient = hashlib.sha256(patient).hexdigest()
document_patient = mycol_patient.find_one({'MD_id': hash_patient})
patient_CT = document_patient['CT']
hash_patient_CT = str.encode(patient_CT)
hash_patient_CT = hashlib.sha256(hash_patient_CT).hexdigest()
print(hash_patient_CT)
'''