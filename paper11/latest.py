from array import array
import json,math, timeit
from operator import concat
import random
from decimal import Decimal
from sympy import airyaiprime
from sympy.ntheory.factor_ import totient
import linecache
import bplib
from bplib.bp import BpGroup

G = BpGroup()
print(G)

def gcd(a, b):
     
    if (a == 0):
        return b
    return gcd(b % a, a)
 
# A simple method to evaluate
# Euler Totient Function
def phi(n):
    result = 1
    for i in range(2, n):
        if (gcd(i, n) == 1):
            result+=1
    return result


def challenge(c):
    k1 = ('{0:20}'.format(random.randint(1, 1)))
    k2 = ('{0:20}'.format(random.randint(1, 1)))
    chal = [c,k1,k2]
    #print(chal)
    return tuple(chal)


def ProofGen(c,k1,k2):
    #print(int(chal[0],2))
    TAll = 1
    FAll = 1
    
    #print('c,k1,k2: ',c,k1,k2)
    
    #print(type(chal[1]))
    #print(int(chal[0],2))
    for i in range(1,2,1):
        vi = math.pi*int(concat(str(k1),str(i))) # choosing random index
        ai = phi(int(concat(str(k2),str(i)))) # choose random params
        #print("vi: ",vi)
        #print('vi,ai: ',vi,ai)
        line = linecache.getline(r"block_tag.txt", 1)
        #print(line)
        #print(line)
        mvi = line[line.find("<[")+2:line.find("]>")]
        tvi = line[line.find("[")+1:line.find("]")]
        #print(tvi)
        mvi = int(Decimal(mvi))
        tvi = int(Decimal(tvi))

        #print("mvi :D",mvi)
        #print("tvi :D",tvi)
        TAll = TAll*math.pow((int(tvi)),int(ai))
        #print("TALL: ", TAll)
        FAll += ai*int(mvi)
        #print("FALL: ", FAll)
        i+=1
        P = [FAll, TAll]
    return P,ai,vi

def verify(y,X, g, u, fid, c, k1, k2, FAll, TAll):
    enc_check = hash(math.pow(int(X),int(y)))
    TAll = 1
    FAll = 1
    hashcheck = 1
    print("THIS IS C: ",c)
    for i in range(c):
        
        # MUL COST 1 #
        startMUL1 = timeit.default_timer()
        vi = math.pi*int(concat(str(k1),str(i))) # choosing random index
        stopMUL1 = timeit.default_timer()
        runtimeMUL1 = stopMUL1-startMUL1
        # MUL COST 1 #
        
        ai = phi(int(concat(str(k2),str(i)))) # choose random params
        
        line = linecache.getline(r"block_tag.txt", math.floor(1))
        mvi = line[line.find("<[")+2:line.find("]>")]
        tvi = line[line.find("[")+1:line.find("]")]
        
        # MUL COST 2 #
        startMUL2 = timeit.default_timer()
        TAll = TAll*(Decimal(tvi)+Decimal(ai))
        FAll += ai*int(mvi)
        stopMUL2 = timeit.default_timer()
        runtimeMUL2 = stopMUL2-startMUL2
        # MUL COST 2 #
        
        
        # EXP COST #
        startEXP = timeit.default_timer()
        # hashcheck *= hash(str(enc_check)+str(fid)+str(vi))**ai
        hashcheck = hash(str(enc_check))**ai
        stopEXP = timeit.default_timer()
        runtimeEXP = stopEXP-startEXP
        # EXP COST #
        
        i+=1
        
    # MUL COST 2 #
    startMUL3 = timeit.default_timer()
    b_right = Decimal(hashcheck)*Decimal(math.pow(u,FAll))
    stopMUL3 = timeit.default_timer()
    runtimeMUL3 = stopMUL3-startMUL3
    # MUL COST 3 #
    
    
    # PAIR COST #
    startPair = timeit.default_timer()
    if(TAll == g): 
        b_leftside = True
    else:
        b_leftside = False
    
    if(b_right == X): 
        b_rightside = True
    else:
        b_rightside = False
        
    stopPair = timeit.default_timer()
    runtimePair = stopPair-startPair
    # PAIR COST #
    
    ### CALCULATION OF ALL COSTS ###
    print("Pairing Cost: ", runtimePair)
    print("Exponentiation Cost: ", runtimeEXP)
    print("Multiplication Cost: ", runtimeMUL1+runtimeMUL2+runtimeMUL3)
    ### CALCULATION OF ALL COSTS ###
    
    if(b_leftside == b_rightside):
        return True
    else:
        return False
    


for i in range(1000,10001,1000):
    filename = "p01000.json"
    x = random.randint(1,1)
    y = random.randint(1,1)
    g = random.randint(1,1)
    u = random.randint(1,1)
    print("======= ",(int(i/10))," =======")
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
    numblock = i*10
    array_blocks = []

    #convert doc to byte
    doc_byte = str.encode(doc)
    doc_byte = (doc_byte[:i]) if len(doc_byte) > i else doc_byte
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
    j = random.randint(0,len(array_blocks))
    #randomly pick 1 block
    mj = array_blocks[j]
    mj = int(mj,2)
    # generate Zq*
    ZqStar = []
    k = random.randint(0,len(array_blocks))
    for i in range(k):
        pickchoice = random.randint(0,len(array_blocks)-1)
        ZqStar.append(array_blocks[pickchoice])
    si_index = random.randint(0,len(ZqStar)-1)
    ii = si_index
    #print("ii ",ii)
    #print(xi_index)
    mi = ZqStar[si_index]
    #print("Si: ",si)
    m = int(mi,2)
    # print("x ",x)
    # print("y ",y)
    # print("g ",g)
    # print("u ",u)
    #x = x/10
    #y = y/5
    #g = g/10
    startX = timeit.default_timer()
    X = Decimal(math.pow(g,x))
    stopX = timeit.default_timer()
    runtimeX = stopX-startX
    #print("Time(EXP X): ",runtimeX)
    
    startY = timeit.default_timer()
    Y = Decimal(math.pow(g,y))
    stopY = timeit.default_timer()
    runtimeY = stopY-startY
    #print("Time(EXP Y): ",runtimeY)
    #print("X ",X)
    #print("Y ",Y)
    fid = "1"
    
    startENC = timeit.default_timer()
    enc = hash(math.pow(Y,x))
    stopENC = timeit.default_timer()
    runtimeENC = stopENC-startENC
    #print("Time(EXP ENC): ",runtimeENC)
    
    # hoho = int(concat(concat(str(enc),str(fid)),str(ii)))
    hoho = int((int(enc)+int(fid)+int(ii)))
    # print("hoho ",hoho)
    #print("mi ",mi)
    gg = True
    while(gg == True):
        if(int(mi) >= 50):
            si_index = random.randint(0,len(ZqStar)-1)
            mi = ZqStar[si_index]
            gg = True
            # print(mi)
        else:
            gg = False
            # print(mi)
    #print('right: ',Decimal(int(u)**int(mi)))
    
    startT = timeit.default_timer()
    Ti = math.pow(hash(hoho)*math.pow(int(u),int(mi)),int(x))
    # print("Ti: ", Ti)
    stopT = timeit.default_timer()
    runtimeT = stopT-startT
    #print("Time(EXP Ti): ",runtimeT)
    # print('rumtime EXP: ', runtimeX+runtimeY+runtimeT+runtimeENC)
    
    txt = (f'[{Ti}]<[{mi}]>')
    with open('block_tag.txt', "a") as tagpair:
        tagpair.write(txt+'\n')
        tagpair.close()
    
    startM = timeit.default_timer()
    mul = math.pow(hash(hoho)*math.pow(int(u),int(mi)),int(x))
    stopM = timeit.default_timer()
    runtimeM = stopM-startM
    # print("Time(MUL): ",runtimeM)
    
    chal = challenge(numblock) # 10000 (10 file) , 20000 (20 files) , 30000 (30 files) , 40000 (40 files) ... 80000 (80 files)
    
    #print('chal: ',chal)
    
    c = chal[0]
    c = int(c/100) # 80000 blocks to 800 blocks (assume that 800 blocks = 800 files)
    k1 = chal[1]
    k2 = chal[2]
    
    #print("here: ",c,k1,k2)
    
    P,ai,vi = ProofGen(c,k1,k2)
    
    #print('P: ',P)
    
    FAll = P[0]
    TAll = P[1]
    
    result = verify(y,X, g, u, fid, c, k1, k2, FAll, TAll)
    
    print(" # of blocks: ",c," result: ", result)
    
    #verify_out = verify(y,X, g, u, fid, c, k1, k2, FAll, TAll)