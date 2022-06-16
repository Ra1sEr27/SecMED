from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
def rsakeygenerator(): #For generating the key for a new section
    rsa_key = RSA.generate(1024)
    f = open('RSA_privkey.pem','wb')
    f.write(rsa_key.export_key('PEM'))
    f.close()
    f = open('RSA_pubkey.pem','wb')
    f.write(rsa_key.public_key().export_key('PEM'))
    f.close()
    # f = open('mykey.pem','r')
    # key = RSA.import_key(f.read())
    
def symkeygenerator(pid): #For regenerating the existed section key
    key = Fernet.generate_key()
    with open('{}_key.txt'.format(pid),'wb') as file:
        file.write(key)
    return key
# def re_adminkeygenerator(): #For regenerating the admin section key
#     key = Fernet.generate_key()
#     with open('admin.key','wb') as file:
#         file.write(key)
symkeygenerator("test")