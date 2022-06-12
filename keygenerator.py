from cryptography.fernet import Fernet
import rsa
def rsakeygenerator(): #For generating the key for a new section
    (pubkey, privkey) = rsa.newkeys(512, poolsize=8)
    print(pubkey)
    print(privkey)
# def re_staffkeygenerator(target_section): #For regenerating the existed section key
#     key = Fernet.generate_key()
#     with open('section{}-staff.key'.format(target_section),'wb') as file:
#         file.write(key)

# def re_adminkeygenerator(): #For regenerating the admin section key
#     key = Fernet.generate_key()
#     with open('admin.key','wb') as file:
#         file.write(key)
rsakeygenerator()