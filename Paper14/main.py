from array import array
import json,math, timeit
import random
from sympy import airyaiprime
from sympy.ntheory.factor_ import totient
import linecache
from bplib.bp import BpGroup

G = BpGroup()
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
        return wj,Tj

def challenge(array_blocks,ZqStar):
    # c = array_blocks[random.randint(0,len(array_blocks))]
    # k1 = ZqStar[random.randint(0,len(ZqStar))]
    # k2 = ZqStar[random.randint(0,len(ZqStar))]
    # chal = [c,k1,k2]
    # return chal
    k1 = ('{0:05}'.format(random.randint(1, 1)))
    k2 = ('{0:05}'.format(random.randint(1, 1)))
    chal = [2,k1,k2]
    #print(chal)
    return tuple(chal)

def ProofGen(chal):
    C=[]
    #print(int(chal[0],2))
    P = []
    TBar = []
    FBar = []
    Tj = 1
    Fj = 1
    #print(type(chal[1]))
    #print(int(chal[0],2))
    for i in range(chal[0]):
        ai = totient(int(str(chal[2])+str(i),2))
        #print("ai: ",ai)
        vi = math.pi*int(str(chal[1])+str(i))
        #print("vi: ",vi)
        line = linecache.getline(r"block_tag.txt", math.floor(vi))
        #print(line)
        mvi = line[line.find("<[")+2:line.find("]>")]
        tvi = line[line.find("[")+1:line.find("]")]
        #print(tvi)
        print("mvi: ",mvi)
        print("tvi: ",tvi)

        Tj = Tj* math.pow((int(tvi)),ai)
        #print("TALL: ", TAll)
        Fj += ai*int(mvi)
        TBar.append(Tj)
        FBar.append(Fj)
    P.append(TBar)
    P.append(FBar)
    return P,ai,vi

def verify(wj,PKi,ID,mj,P0,ai,vi):
    g1, g2 = G.gen1(), G.gen2()
    eq1 = G.pair(g1*hash(wj),g2*PKi) + G.pair(g1*(hash(ID)**mj),g2*P0)
    print("eq1: ",eq1)
    eq2 = G.pair(hash(wj)**ai,PKi) + G.pair(hash(ID),P0)
    print("eq2: ",eq2)
    if eq1 == eq2:
        #print("True")
        return True
    #print("False")
    return False


filename = "p01000.json"
prevLeastRuntime = 0
for i1 in range(1000,10001,1000):
    
    numattr = i1
    j = str(i1)
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
    runtimelist = []
    for a in range(10):
        start = timeit.default_timer()
        numblock = i1*10 # 1000 Attributes -> 1000*10 = 10000
        stop = timeit.default_timer()
        runtimemul1 = stop-start
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

        P0 = int(array_blocks[si_index],2)**s
        #print("P0: ",P0)
        start = timeit.default_timer()
        Di = hash(id**s)
        stop = timeit.default_timer()
        runtimeexp1 = stop-start
        #--Generate PKi
        g = random.randint(1,5)
        PKi = g**s
        start = timeit.default_timer()
        wj,Tj = TagGen(filename, array_blocks,Di,mj,s)
        stop = timeit.default_timer()
        runtimeexp2 = stop-start
        
        #--store Di and Tj in log file
        with open('Logfile.json','r') as file:
            doc = file.read()
        doc = json.loads(doc)
        doc[j] = wj
        doc = json.dumps(doc)
        with open('Logfile.json','w') as file:
            file.write(doc)

        #--store block and tag
        with open('block_tag.json','r') as file:
            doc = file.read()
        doc = json.loads(doc)
        doc[Tj] = array_blocks
        doc = json.dumps(doc)
        with open('block_tag.json','w') as file:
            file.write(doc)
        #--Begin challenging
        # chal = challenge(array_blocks,ZqStar)
        # #print(chal)
        # #--Begin ProofGen
        # start = timeit.default_timer()
        # P,ai,vi = ProofGen(chal)
        # stop = timeit.default_timer()
        # runtimemul2 = stop-start
        #--Begin verification
        # with open('Logfile.json','r') as file:
        #     doc = file.read()
        # doc = json.loads(doc)
        # print(type(doc))
        # print(Di)
        # wj = doc[Di]
        # print(wj)
        # start = timeit.default_timer()
        # output = verify(wj,PKi,id,mj,P0,ai,vi)
        # stop = timeit.default_timer()
        # runtimeexp2 = stop-start
        totalruntime = 2*(runtimeexp1+runtimeexp2)
        runtimelist.append(totalruntime)
    runtimelist.sort()
    for i2 in range(len(runtimelist)):
        if runtimelist[i2] > prevLeastRuntime:
            print('Time({}): '.format(i1), runtimelist[i2])
            #print('DSRR1Time({}): '.format(i), runtime_list[i1])
            prevLeastRuntime = runtimelist[i2]
            break
    #print("Time({}): ".format(i1),runtime1+runtime2+runtime3)