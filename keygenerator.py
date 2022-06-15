from cryptography.fernet import Fernet
import rsa
def rsakeygenerator(): #For generating the key for a new section
    (pubkey, privkey) = rsa.newkeys(512, poolsize=8)
    with open('dataowner_rsa_priv_key.txt','wb') as file:
        file.write(privkey)
    with open('dataowner_rsa_pub_key.txt','wb') as file:
        file.write(pubkey)
    return pubkey, privkey
    
def symkeygenerator(pid): #For regenerating the existed section key
    key = Fernet.generate_key()
    with open('{}_key.txt'.format(pid),'wb') as file:
        file.write(key)
    return key
# def re_adminkeygenerator(): #For regenerating the admin section key
#     key = Fernet.generate_key()
#     with open('admin.key','wb') as file:
#         file.write(key)
symkeygenerator("p0000")