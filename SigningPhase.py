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
    #print("len DS_binary: ", len(DS_Binary))
    #print("Binary: ",DS_Binary)
    #generate R value
    R = ""
    for i in range(len(DS_Binary)):
        temp = str(random.randint(0,1))
        R += temp
    #print("len R: ", len(R))
    #print("R: ",R)
    # XOR DS_Binary with R value
    DS_XOR_R_Binary = ""
    for i in range(len(DS_Binary)):
        temp1 = XOR(DS_Binary[i],R[i])
        DS_XOR_R_Binary += str(temp1)
    #print("DS XORed R: ", DS_XOR_R)
    binary_int = int(DS_XOR_R_Binary, 2)
    # Getting the byte number
    byte_number = binary_int.bit_length() + 7 // 8
    # Getting an array of bytes
    binary_array = binary_int.to_bytes(byte_number, "big")
    #print("BA: ",binary_array)

    # Converting the array into ASCII text
    DS_XOR_R_text = binary_array.decode('ISO-8859-1')
    #print("DS*R: ",DS_XOR_R_text)
    #Define constant R
    constR = "01100010100110101111100000111011000000010111011100001010010110001101011000001001101111010101001001100011001001111101010011011111011101110011010000100101111000101000100100101111001010000110010010000110110001111000110010001101111010100010010101110000101000101110100001001011010111100001001110111011101110101111011111011111110010010101010010001101010001000000011001001001111000100100100001001000111011001111001111110100101011111011001101101100110111100111100011100011100011010000010101010011010000011100001011011110011010010001010000010111001010001110011010010000000001001101100010001110111111101100111100000010110000101000011010110010001111000001010011001001001100001101101000101101010010010001101111111011001111111010000011010011101001100001010011111101100011010111101001001100001001100011000001011100010011111010110110100010111011100001100111000101000110110100010111100100111011001101000010100111010100010010011111010110010000111111001010001111111011001110110000001000100010011101010110011001001111011000101001111110111111110010110000111010110000100011001101001000000001101011100110100000000101110001001100000111100111000101110010011001100110110001110001110101100000111000011011010101001111010001110011110110000001101101010100111101000111001111011000"
    constR += constR
    #print("len const R: ",len(constR))
    #Get R1
    R1_Binary = ""
    for i in range(len(R)):
        temp1 = XOR(R[i],constR[i])
        R1_Binary += str(temp1)
    #Transform binary to text
    binary_int = int(R1_Binary, 2)
    # Getting the byte number
    byte_number = binary_int.bit_length() + 7 // 8
    # Getting an array of bytes
    binary_array = binary_int.to_bytes(byte_number, "big")
    R1_text = binary_array.decode('ISO-8859-1')
    #print("R1: ",R1_text)
    return DS_XOR_R_text, R1_text

def RSADecryption(data):
    f = open('RSA_privkey.pem','r')
    privkey = RSA.import_key(f.read())
    CT_RSA_Privkey = PKCS1_OAEP.new(privkey)
    MD = CT_RSA_Privkey.decrypt(data)
    print("MD: ",MD)
    return MD

# input = str.encode("test")
# Sign(input)