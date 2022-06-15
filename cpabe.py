import subprocess
#enc the symkey with policy dataowner or medicalstaff
#id = "p0000"
def encrypt(id):
    p = subprocess.call(["cpabe-enc", "pub_key", "{}_key.txt".format(id), "dataowner or medicalstaff"])
#dec the symkey with dataowner's private key
def decrypt(id):
    p = subprocess.call(["cpabe-dec", "pub_key", "dataowner_priv_key", "{}_key.txt.cpabe".format(id)])
#p = subprocess.call(["mv", "{}_key.txt.cpabe".format(id), "{}_key.txt".format(id)])
#decrypt("p0000")