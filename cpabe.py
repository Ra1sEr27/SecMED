import subprocess
#enc the symkey with policy dataowner or medicalstaff
#id = "p0000"
def encrypt(id):
    p = subprocess.call(["cpabe-enc", "pub_key", "{}_key.txt".format(id), "dataowner or medicalstaff"])
def encrypt_text(id):
    p = subprocess.call(["cpabe-enc", "pub_key", "./testpatient/{}.txt".format(id), "dataowner or medicalstaff"])
#dec the symkey with dataowner's private key
def decrypt(file):
    p = subprocess.call(["cpabe-dec", "pub_key", "DO0000_priv_key", "{}".format(file)])
def keygen(id,policy):
    p = subprocess.call(["cpabe-keygen", "-o", id+"_priv_key","pub_key","cpabe-0.11/master_key", policy])
#p = subprocess.call(["mv", "{}_key.txt.cpabe".format(id), "{}_key.txt".format(id)])
#decrypt("p00011")
encrypt_text("p00010")
# policyarray = ["dataowner","medicalstaff","a","b","c","d","e","f","g","h"]
# inputpolicy = ""
# for i in range(10):
#     policy = policyarray[i]+" "
#     inputpolicy += policy
#     keygen("DO000{}".format(i),"inputpolicy")
#     #print(inputpolicy)
#eygen("DO00000","dataowner")
