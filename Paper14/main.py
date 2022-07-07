from array import array
import json,math, timeit
import random
from sympy import airyaiprime
from sympy.ntheory.factor_ import totient
import linecache
# def gcd(a, b):
#     if (a == 0):
#         return b
#     return gcd(b % a, a)

# def phi(n):
#     result = 1
#     for i in range(2, n):
#         if (math.gcd(i, n) == 1):
#             result+=1
#     return result

def TagGen(filename, array_blocks,Di,mj,s):
        #Generate wj
        wj = filename + str(len(array_blocks)) + str(j)
        #Calculate Tj
        Tj = (Di**mj) + hash(wj)**s
        return Tj

def challenge(array_blocks,ZqStar):
    c = array_blocks[random.randint(0,len(array_blocks))]
    k1 = ZqStar[random.randint(0,len(ZqStar))]
    k2 = ZqStar[random.randint(0,len(ZqStar))]
    chal = [c,k1,k2]
    return chal

def ProofGen(chal):
    C=[]
    #print(int(chal[0],2))
    TBar = []
    FBar = []
    Tj = 1
    Fj = 1
    print(int(chal[0],2))  
    for i in range(int(chal[0],2)):
        ai = totient(int(str(chal[2])+str( i)))
        print("ai: ",ai)
        vi = math.pi*int(str(chal[1])+str(i))
        print("vi: ",vi)
        line = linecache.getline(r"block_tag.txt", math.floor(vi))
        print(line)
        mvi = line[line.find("<[")+2:line.find("]>")]
        tvi = line[line.find("[")+1:line.find("]")]
        print(tvi)
        #print("mvi ",mvi)
        #print("tvi ",tvi)
        Tj = Tj* math.pow((int(tvi)),ai)
        #print("TALL: ", TAll)
        Fj += ai*int(mvi)
        TBar.append(Tj)
        FBar.append(Fj)
    return TBar,FBar

start = timeit.default_timer()
filename = "p01000.json"
for i in range(1000,1001,1000):
    numattr = i
    j = str(i)
    while(len(j) < 5):
        j = "0"+ j
    with open('./testpatient/p{}.txt'.format(j),'r') as file:
        doc = file.read()

    # filename = "file.txt"
    # with open('file.json','r') as file:
    #     doc = file.read()
    #doc = json.loads(doc)
    id = int(j)
    #doc = json.dumps(doc)
    # with open('file.txt','r') as file:
    #     doc = file.read()
    numblock = i*10 # 1000 Attributes -> 1000*10 = 10000
    array_blocks = []

    #convert doc to byte
    doc_byte = str.encode(doc)
    doc_Binary = ''.join([bin(b)[2:] for b in doc_byte])
    #print(len(doc_Binary))
    lenperblock = math.ceil(len(doc_Binary) / numblock)
    #print(lenperblock)
    temp_doc_Binary = doc_Binary
    #cut part of binary and put into the block
    while(temp_doc_Binary != ""): 
        array_blocks.append(temp_doc_Binary[:lenperblock])
        temp_doc_Binary = temp_doc_Binary[lenperblock:]
    #print(array_blocks)
    #print(len(array_blocks))
    #--pick index of array blocks
    j = random.randint(0,len(array_blocks))
    #pick block at index j
    mj = array_blocks[j]
    mj = int(mj,2)
    # generate Zq*
    ZqStar = []
    k = random.randint(0,len(array_blocks))
    for i in range(k):
        pickchoice = random.randint(0,len(array_blocks)-1)
        ZqStar.append(array_blocks[pickchoice])
    #--Get secert key (Si)
    si_index = random.randint(0,len(ZqStar)-1)
    #print(xi_index)
    si = ZqStar[si_index]
    #print("Si: ",len(si))
    s = int(si,2)
    #print("S: ",s)
    Di = hash(id**s)
    #--Generate PKi
    g = random.randint(1,5)
    PKi = g**s
    Tj = TagGen(filename, array_blocks,Di,mj,s)
    #--store Di and Tj in log file
    with open('Logfile.json','r') as file:
        doc = file.read()
    doc = json.loads(doc)
    doc[Di] = Tj
    #--Begin challenging
    chal = challenge(array_blocks,ZqStar)
    print(chal)
    #--Begin ProofGen
    TBar,Fbar = ProofGen(chal)
    