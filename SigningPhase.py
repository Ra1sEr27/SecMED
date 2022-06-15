import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64, hashlib, random

def XOR (a, b):
    if a != b:
        return 1
    else:
        return 0

def Sign(CT_byte):
    #hash the CT
    CT_MD = hashlib.sha256(CT_byte).hexdigest()
    CT_MD_byte = str.encode(CT_MD)
    #import pubkey
    f = open('RSA_pubkey.pem','r')
    pubkey = RSA.import_key(f.read())
    CT_RSA_Pubkey = PKCS1_OAEP.new(pubkey)
    #encrypt MD with RSA -> Get DS
    DS_byte = CT_RSA_Pubkey.encrypt(CT_MD_byte)
    #print("DSByte: ", DS_byte)
    DS = DS_byte.decode('ISO-8859-1')
    encoded_bytes = DS.encode(encoding='utf-8')
    #Convert DS to binary string
    DS_Binary = ''.join([bin(b)[2:] for b in encoded_bytes])
    print("Binary: ",DS_Binary)
    #generate R value
    R = ""
    for i in range(len(DS_Binary)):
        temp = str(random.randint(0,1))
        R += temp
    print("R: ",R)
    # XOR DS_Binary with R value
    DS_XOR_R = ""
    for i in range(len(DS_Binary)):
        temp1 = XOR(DS_Binary[i],R[i])
        DS_XOR_R += str(temp1)
    print("DS XORed R: ", DS_XOR_R)
    binary_int = int(DS_XOR_R, 2)
    # Getting the byte number
    byte_number = binary_int.bit_length() + 7 // 8
    
    # Getting an array of bytes
    binary_array = binary_int.to_bytes(byte_number, "big")
    print(binary_array)
    # Converting the array into ASCII text
    ascii_text = binary_array.decode('ISO-8859-1')
    #encoded_bytes = DS.encode(encoding='utf-8')
    
    # Getting the ASCII value
    print(ascii_text)
    # return DS

def RSADecryption(data):
    f = open('RSA_privkey.pem','r')
    privkey = RSA.import_key(f.read())
    CT_RSA_Privkey = PKCS1_OAEP.new(privkey)
    MD = CT_RSA_Privkey.decrypt(data)
    print("MD: ",MD)
    return MD

input = str.encode("test")
Sign(input)